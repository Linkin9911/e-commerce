import json
from unittest.mock import mock_open, patch

import pytest

from src.main import Category, Product, load_data_from_json


@pytest.fixture(autouse=True)
def reset_category_counters():
    """Автоматически сбрасывает счётчики категорий и товаров перед каждым тестом."""
    Category.category_count = 0
    Category.product_count = 0
    yield


@pytest.fixture
def sample_product() -> Product:
    """Фикстура для создания тестового объекта Product."""
    return Product("Смартфон", "Современный смартфон", 29999.99, 10)


@pytest.fixture
def sample_category() -> Category:
    """Фикстура для создания тестового объекта Category с двумя товарами."""
    products = [
        Product("Смартфон", "Современный смартфон", 29999.99, 10),
        Product("Ноутбук", "Мощный ноутбук", 59999.99, 5),
    ]
    return Category("Электроника", "Электронные устройства", products)


# --- Тесты для Product ---


def test_product_initialization(sample_product: Product) -> None:
    """Проверяет корректность инициализации объекта Product."""
    assert sample_product.name == "Смартфон"
    assert sample_product.description == "Современный смартфон"
    assert sample_product.price == 29999.99
    assert sample_product.quantity == 10


def test_product_price_setter_negative_value(sample_product: Product):
    """Проверяет поведение сеттера price при установке отрицательной цены."""
    with patch("builtins.print") as mock_print:
        sample_product.price = -100.0
        mock_print.assert_called_with("Цена не должна быть нулевая или отрицательная")
    assert sample_product.price == 29999.99  # цена не изменилась


def test_product_price_setter_zero_value(sample_product: Product):
    """Проверяет поведение сеттера price при установке нулевой цены."""
    with patch("builtins.print") as mock_print:
        sample_product.price = 0.0
        mock_print.assert_called_with("Цена не должна быть нулевая или отрицательная")
    assert sample_product.price == 29999.99  # цена не изменилась


@patch("builtins.input", return_value="y")
def test_product_price_setter_confirmation_yes(mock_input, sample_product: Product):
    """Проверяет подтверждение снижения цены (пользователь ввёл 'y')."""
    sample_product.price = 25000.0  # снижаем цену
    assert sample_product.price == 25000.0


@patch("builtins.input", return_value="n")
def test_product_price_setter_confirmation_no(mock_input, sample_product: Product):
    """Проверяет отказ от снижения цены (пользователь ввёл 'n')."""
    initial_price = sample_product.price
    sample_product.price = 25000.0  # пытаемся снизить цену
    assert sample_product.price == initial_price  # цена осталась прежней


# --- Тесты для Category ---


def test_category_initialization(sample_category: Category) -> None:
    """Проверяет корректность инициализации объекта Category."""
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Электронные устройства"
    products_list = sample_category.get_products_list()
    assert isinstance(products_list, list)
    assert len(products_list) == 2
    assert isinstance(products_list[0], Product)
    products_output = sample_category.products
    assert "Смартфон" in products_output
    assert "Ноутбук" in products_output


def test_add_product(sample_category: Category):
    """Проверяет добавление продукта в категорию."""
    initial_product_count = Category.product_count
    new_product = Product("Планшет", "Новый планшет", 45000.0, 3)
    sample_category.add_product(new_product)
    products_list = sample_category.get_products_list()
    assert new_product in products_list
    assert Category.product_count == initial_product_count + 1
    assert "Планшет" in sample_category.products


def test_products_getter_formatting(sample_category: Category):
    """Проверяет форматирование вывода геттера products."""
    products_output = sample_category.products
    expected_lines = [
        "Смартфон, 29999.99 руб. Остаток: 10 шт.",
        "Ноутбук, 59999.99 руб. Остаток: 5 шт.",
    ]
    for expected_line in expected_lines:
        assert expected_line in products_output


# --- Тесты для new_product ---


def test_new_product_no_existing_list():
    """Проверяет создание нового продукта без списка существующих товаров."""
    product_data = {
        "name": "Новый товар",
        "description": "Описание",
        "price": 1000.0,
        "quantity": 2,
    }
    product = Product.new_product(product_data)
    assert isinstance(product, Product)
    assert product.name == "Новый товар"
    assert product.quantity == 2


def test_new_product_duplicate_existing():
    """Проверяет обработку дубликата товара в new_product."""
    existing_product = Product("Смартфон", "Описание", 30000.0, 5)
    products_list = [existing_product]
    duplicate_data = {
        "name": "Смартфон",
        "description": "Новое описание",
        "price": 35000.0,
        "quantity": 3,
    }
    result = Product.new_product(duplicate_data, products_list)
    assert result is existing_product
    assert existing_product.quantity == 8
    assert existing_product.price == 35000.0


def test_new_product_duplicate_lower_price():
    """Проверяет обновление дубликата с более низкой ценой (цена не должна измениться)."""
    existing_product = Product("Смартфон", "Описание", 30000.0, 5)
    products_list = [existing_product]
    duplicate_data = {
        "name": "Смартфон",
        "description": "Новое описание",
        "price": 25000.0,
        "quantity": 3,
    }
    result = Product.new_product(duplicate_data, products_list)
    assert result is existing_product
    assert existing_product.quantity == 8
    assert existing_product.price == 30000.0  # цена осталась прежней


# --- Тесты для load_data_from_json ---


def test_load_data_from_json_valid():
    """Проверяет загрузку данных из корректного JSON‑файла."""
    mock_json = """{
      "categories": [
        {
          "name": "Смартфоны",
          "description": "Мобильные устройства",
          "products": [
            {
              "name": "Смартфон 1",
              "description": "Описание 1",
              "price": 30000.0,
              "quantity": 5
            }
          ]
        }
      ]
    }"""
    with patch("builtins.open", mock_open(read_data=mock_json)):
        categories = load_data_from_json("test.json")
    assert len(categories) == 1
    assert categories[0].name == "Смартфоны"
    products_list = categories[0].get_products_list()
    assert isinstance(products_list, list)
    assert len(products_list) == 1
    assert products_list[0].name == "Смартфон 1"


def test_load_data_from_json_file_not_found():
    """Проверяет обработку ошибки 'файл не найден'."""
    with pytest.raises(FileNotFoundError, match="Файл nonexistent.json не найден."):
        load_data_from_json("nonexistent.json")


def test_load_data_from_json_invalid_json():
    """Проверяет обработку некорректного JSON."""
    invalid_json = '{"name": "Test", "value": }'  # Синтаксическая ошибка

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        with pytest.raises(json.JSONDecodeError):
            load_data_from_json("invalid.json")


def test_load_data_from_json_empty_file():
    """Проверяет обработку пустого JSON‑файла."""
    with patch("builtins.open", mock_open(read_data="{}")):
        categories = load_data_from_json("empty.json")
    assert len(categories) == 0
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_load_data_from_json_missing_categories():
    """Проверяет обработку JSON без секции 'categories'."""
    mock_json = '{"other_data": "some_value"}'
    with patch("builtins.open", mock_open(read_data=mock_json)):
        categories = load_data_from_json("no_categories.json")
    assert len(categories) == 0
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_load_data_from_json_empty_categories():
    """Проверяет обработку JSON с пустой секцией 'categories'."""
    mock_json = '{"categories": []}'
    with patch("builtins.open", mock_open(read_data=mock_json)):
        categories = load_data_from_json("empty_categories.json")
    assert len(categories) == 0
    assert Category.category_count == 0
    assert Category.product_count == 0


def test_load_data_from_json_category_without_products():
    """Проверяет загрузку категории без товаров."""
    mock_json = """{
          "categories": [
            {
              "name": "Пустая категория",
              "description": "Категория без товаров",
              "products": []
            }
          ]
        }"""
    with patch("builtins.open", mock_open(read_data=mock_json)):
        categories = load_data_from_json("category_no_products.json")
    assert len(categories) == 1
    assert categories[0].name == "Пустая категория"
    assert len(categories[0].get_products_list()) == 0
    assert Category.category_count == 1
    assert Category.product_count == 0


def test_load_data_from_json_multiple_categories():
    """Проверяет загрузку нескольких категорий с товарами."""
    mock_json = """{
          "categories": [
            {
              "name": "Смартфоны",
              "description": "Мобильные устройства",
              "products": [
                {
                  "name": "Смартфон 1",
                  "description": "Описание 1",
                  "price": 30000.0,
                  "quantity": 5
                },
                {
                  "name": "Смартфон 2",
                  "description": "Описание 2",
                  "price": 40000.0,
                  "quantity": 3
                }
              ]
            },
            {
              "name": "Ноутбуки",
              "description": "Портативные компьютеры",
              "products": [
                {
                  "name": "Ноутбук 1",
                  "description": "Описание ноутбука",
                  "price": 80000.0,
                  "quantity": 2
                }
              ]
            }
          ]
        }"""
    with patch("builtins.open", mock_open(read_data=mock_json)):
        categories = load_data_from_json("multiple_categories.json")
    assert len(categories) == 2
    assert categories[0].name == "Смартфоны"
    assert categories[1].name == "Ноутбуки"
    assert len(categories[0].get_products_list()) == 2
    assert len(categories[1].get_products_list()) == 1
    # Проверяем счётчики
    assert Category.category_count == 2
    assert Category.product_count == 3  # 2 смартфона + 1 ноутбук


def test_load_data_from_json_product_with_missing_fields():
    """Проверяет загрузку продуктов с отсутствующими полями."""
    mock_json = """{
      "categories": [
        {
          "name": "Тестовая категория",
          "description": "Категория с неполными данными",
          "products": [
            {
              "name": "Продукт без описания",
              "price": 1000.0,
              "quantity": 1
            },
            {
              "name": "Продукт без цены",
              "description": "Есть описание",
              "quantity": 2
            }
          ]
        }
      ]
    }"""

    with patch("builtins.open", mock_open(read_data=mock_json)):
        categories = load_data_from_json("incomplete_data.json")

    category = categories[0]
    products = category.get_products_list()

    # Проверяем, что загрузились оба продукта
    assert len(products) == 2

    # Проверяем первый продукт (без описания)
    product1 = products[0]
    assert product1.name == "Продукт без описания"
    assert product1.description == "Без описания"  # Значение по умолчанию
    assert product1.price == 1000.0
    assert product1.quantity == 1

    # Проверяем второй продукт (без цены)
    product2 = products[1]
    assert product2.name == "Продукт без цены"
    assert product2.description == "Есть описание"
    assert product2.price == 0.0  # Значение по умолчанию
    assert product2.quantity == 2
