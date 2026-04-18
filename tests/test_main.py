import json
from unittest.mock import mock_open, patch

import pytest

from src.main import Category, Product, load_data_from_json


@pytest.fixture
def sample_product() -> Product:
    """
    Фикстура для создания тестового объекта Product.

    Returns:
        Product: объект товара для тестирования.
    """
    return Product("Смартфон", "Современный смартфон", 29999.99, 10)


@pytest.fixture
def sample_category() -> Category:
    """
    Фикстура для создания тестового объекта Category с двумя товарами.

    Returns:
        Category: объект категории для тестирования.
    """
    products = [
        Product("Смартфон", "Современный смартфон", 29999.99, 10),
        Product("Ноутбук", "Мощный ноутбук", 59999.99, 5),
    ]
    return Category("Электроника", "Электронные устройства", products)


def test_product_initialization(sample_product: Product) -> None:
    """
    Проверяет корректность инициализации объекта Product.

    Args:
        sample_product (Product): тестовый объект Product из фикстуры.
    """
    assert sample_product.name == "Смартфон"
    assert sample_product.description == "Современный смартфон"
    assert sample_product.price == 29999.99
    assert sample_product.quantity == 10


def test_category_initialization(sample_category: Category) -> None:
    """
    Проверяет корректность инициализации объекта Category.

    Args:
        sample_category (Category): тестовый объект Category из фикстуры.
    """
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Электронные устройства"
    # Явно проверяем, что products не None, и берём длину
    assert isinstance(sample_category.products, list)
    assert len(sample_category.products) == 2
    assert isinstance(sample_category.products[0], Product)


def test_category_counts() -> None:
    """
    Проверяет корректность подсчёта количества категорий и товаров.

    Проверяет:
        - увеличение category_count при создании новой категории;
        - суммирование product_count на основе количества товаров (quantity).
    """
    # Сбрасываем счётчики для чистоты теста
    Category.category_count = 0
    Category.product_count = 0

    product1 = Product("Товар 1", "Описание 1", 100.0, 5)  # 5 штук
    product2 = Product("Товар 2", "Описание 2", 200.0, 3)  # 3 штуки

    # Создаём категории — это увеличивает счётчики
    category1 = Category("Категория 1", "Описание категории 1", [product1])
    assert Category.category_count == 1
    assert Category.product_count == 5  # 5 штук товара 1

    category2 = Category("Категория 2", "Описание категории 2", [product2])
    assert Category.category_count == 2
    assert Category.product_count == 8  # 5 + 3 = 8 штук всего

    # Явно указываем, что переменные используются (чтобы убрать предупреждения)
    _ = category1
    _ = category2


def test_category_with_none_products():
    """
    Проверяет создание категории с products=None.

    Убеждается, что:
        - products инициализируется как пустой список;
        - счётчики обновляются корректно.
    """
    category = Category("Пустая", "Без товаров", None)
    assert category.name == "Пустая"
    assert isinstance(category.products, list)
    assert len(category.products) == 0
    assert Category.category_count >= 1
    assert Category.product_count >= 0


def test_product_with_zero_quantity():
    """
    Проверяет инициализацию товара с нулевым количеством.

    Убеждается, что товар с quantity=0 создаётся корректно.
    """
    product = Product("Товар", "Описание", 100.0, 0)
    assert product.quantity == 0


def test_product_with_negative_price():
    """
    Проверяет инициализацию товара с отрицательной ценой.

    Убеждается, что товар с отрицательной ценой создаётся корректно.
    """
    product = Product("Товар", "Описание", -50.0, 5)
    assert product.price == -50.0


def test_load_data_from_json_valid():
    """
    Проверяет загрузку данных из корректного JSON‑файла.

    Создаёт моковый JSON с одной категорией и одним товаром,
    убеждается, что данные корректно загружаются и преобразуются в объекты.
    """
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
    assert len(categories[0].products) == 1
    assert isinstance(categories[0].products[0], Product)
    assert categories[0].products[0].name == "Смартфон 1"


def test_load_data_from_json_file_not_found():
    """
    Проверяет обработку ошибки 'файл не найден'.

    Убеждается, что функция вызывает FileNotFoundError при попытке
    загрузить несуществующий файл.
    """
    with pytest.raises(FileNotFoundError):
        load_data_from_json("nonexistent.json")


def test_load_data_from_json_invalid_json():
    """
    Проверяет обработку некорректного JSON.

    Создаёт моковый файл с некорректным JSON,
    убеждается, что функция вызывает JSONDecodeError.
    """
    # Используем заведомо некорректный JSON:
    # - незакрытая строка
    # - отсутствует кавычка
    # - лишний запятый
    invalid_json = '{"name": "Test", "value": }'  # Некорректный JSON: отсутствует значение после ":"

    with patch("builtins.open", mock_open(read_data=invalid_json)):
        with pytest.raises(json.JSONDecodeError):
            load_data_from_json("invalid.json")


def test_load_data_from_json_empty_file():
    """
    Проверяет обработку пустого JSON‑файла.

    Создаёт моковый пустой JSON, убеждается, что функция возвращает
    пустой список категорий без ошибок.
    """
    with patch("builtins.open", mock_open(read_data="{}")):
        categories = load_data_from_json("empty.json")
    assert len(categories) == 0


def test_load_data_from_json_missing_categories():
    """
    Проверяет обработку JSON без секции 'categories'.

    Создаёт моковый JSON без ключа 'categories', убеждается,
    что функция возвращает пустой список без ошибок.
    """
    with patch("builtins.open", mock_open(read_data='{"other": "data"}')):
        categories = load_data_from_json("no_categories.json")
    assert len(categories) == 0
