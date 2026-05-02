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


def test_product_str_representation(sample_product: Product):
    """Проверяет строковое представление объекта Product."""
    expected = "Смартфон, 29999.99 руб. Остаток: 10 шт."
    assert str(sample_product) == expected

def test_product_addition(sample_product: Product):
    """Проверяет сложение двух объектов Product."""
    product2 = Product("Наушники", "Беспроводные", 5000.0, 3)
    total_value = sample_product + product2
    expected_value = (29999.99 * 10) + (5000.0 * 3)  # 299 999,9 + 15 000
    assert total_value == expected_value

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
    original_price = sample_product.price
    sample_product.price = 25000.0  # пытаемся снизить цену
    assert sample_product.price == original_price  # цена осталась прежней

# --- Тесты для Category ---

def test_category_initialization(sample_category: Category):
    """Проверяет корректность инициализации объекта Category."""
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Электронные устройства"
    assert len(sample_category.get_products_list()) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2

def test_category_add_product(sample_category: Category):
    """Проверяет добавление продукта в категорию."""
    new_product = Product("Планшет", "10-дюймовый экран", 45000.0, 3)
    sample_category.add_product(new_product)
    assert len(sample_category.get_products_list()) == 3
    assert Category.product_count == 3

def test_category_str_representation(sample_category: Category):
    """Проверяет строковое представление объекта Category."""
    total_quantity = sum(p.quantity for p in sample_category.get_products_list())
    expected = f"Электроника, количество продуктов: {total_quantity} шт."
    assert str(sample_category) == expected

def test_category_iterator(sample_category: Category):
    """Проверяет работу итератора для категории."""
    products = list(sample_category)
    assert len(products) == 2
    # Проверяем, что итератор возвращает правильные объекты
    assert isinstance(products[0], Product)
    assert isinstance(products[1], Product)

def test_category_products_property(sample_category: Category):
    """Проверяет геттер products."""
    products_str = sample_category.products
    assert len(products_str) == 2
    assert all(isinstance(p, str) for p in products_str)

# --- Тесты для Product.new_product ---

def test_new_product_create_new():
    """Проверяет создание нового продукта через new_product."""
    product_data = {
        "name": "Телевизор",
        "description": "4K UHD",
        "price": 80000.0,
        "quantity": 5
    }
    new_product = Product.new_product(product_data)
    assert new_product.name == "Телевизор"
    assert new_product.price == 80000.0
    assert new_product.quantity == 5

def test_new_product_update_existing():
    """Проверяет обновление существующего продукта через new_product."""
    # Создаём существующий продукт
    existing_product = Product("Смартфон", "Обновлённая модель", 35000.0, 5)
    products_list = [existing_product]

    # Данные для обновления (с большим количеством и ценой)
    update_data = {
        "name": "Смартфон",
        "description": "Дубликат с увеличенным количеством",
        "price": 40000.0,  # выше текущей цены
        "quantity": 3,
    }

    updated_product = Product.new_product(update_data, products_list)
    assert updated_product is existing_product  # это тот же объект
    assert updated_product.quantity == 8  # 5 + 3
    assert updated_product.price == 40000.0  # обновилась до максимальной

# --- Тесты для load_data_from_json ---


@patch("builtins.open", mock_open(read_data='{"categories": []}'))
def test_load_data_empty_categories():
    """Проверяет загрузку данных с пустым списком категорий."""
    categories = load_data_from_json("test.json")
    assert len(categories) == 0

@patch(
    "builtins.open",
    mock_open(
        read_data='''
        {
            "categories": [
                {
                    "name": "Электроника",
            "description": "Электронные устройства",
            "products": [
                {
                    "name": "Смартфон",
            "description": "Современный смартфон",
            "price": 29999.99,
            "quantity": 10
                }
            ]
        }
            ]
        }
        '''
    )
)
def test_load_data_single_category():
    """Проверяет загрузку данных с одной категорией и одним продуктом."""
    categories = load_data_from_json("test.json")
    assert len(categories) == 1
    category = categories[0]
    assert category.name == "Электроника"
    assert len(category.get_products_list()) == 1
    product = category.get_products_list()[0]
    assert product.name == "Смартфон"
    assert product.price == 29999.99
    assert product.quantity == 10

def test_load_data_file_not_found():
    """Проверяет обработку ошибки отсутствия файла."""
    with pytest.raises(FileNotFoundError):
        load_data_from_json("nonexistent.json")

def test_load_data_invalid_json():
    """Проверяет обработку некорректного JSON."""
    with patch(
        "builtins.open",
        mock_open(read_data="некорректный json {")
    ):
        with pytest.raises(json.JSONDecodeError):
            load_data_from_json("invalid.json")

def test_category_empty_name():
    """Проверяет инициализацию категории с пустым названием (должно вызвать исключение)."""
    with pytest.raises(ValueError) as exc_info:
        Category("", "Описание пустой категории")
    assert str(exc_info.value) == "Название категории не может быть пустым"


def test_category_multiple_products():
    """Проверяет корректность работы с несколькими продуктами в категории."""
    products = [
        Product("Смартфон 1", "Модель A", 30000.0, 5),
        Product("Смартфон 2", "Модель B", 40000.0, 3),
        Product("Смартфон 3", "Модель C", 25000.0, 8),
    ]
    category = Category("Смартфоны", "Различные модели смартфонов", products)

    assert len(category.get_products_list()) == 3
    assert Category.product_count == 3

    # Проверяем общее количество товаров в категории
    total_quantity = sum(p.quantity for p in category.get_products_list())
    assert total_quantity == 16

def test_product_new_product_with_missing_fields():
    """Проверяет создание продукта с отсутствующими полями (используются значения по умолчанию)."""
    product_data = {
        "name": "Тестовый продукт",
        # Отсутствуют description, price, quantity
    }
    new_product = Product.new_product(product_data)
    assert new_product.name == "Тестовый продукт"
    assert new_product.description == "Без описания"
    assert new_product.price == 0.0
    assert new_product.quantity == 0

def test_category_iterator_empty_category():
    """Проверяет работу итератора для пустой категории."""
    empty_category = Category("Пустая категория", "Категория без товаров")
    iterator = iter(empty_category)

    with pytest.raises(StopIteration):
        next(iterator)

def test_load_data_from_json_with_multiple_categories():
    """Проверяет загрузку данных с несколькими категориями и товарами."""
    json_data = '''
    {
        "categories": [
            {
                "name": "Электроника",
                "description": "Электронные устройства",
                "products": [
                    {
                        "name": "Смартфон",
                        "description": "Современный смартфон",
                        "price": 29999.99,
                        "quantity": 10
            },
            {
                "name": "Ноутбук",
                "description": "Мощный ноутбук",
                "price": 59999.99,
                "quantity": 5
            }
        ]
            },
            {
                "name": "Бытовая техника",
                "description": "Устройства для дома",
                "products": [
            {
                "name": "Холодильник",
                "description": "Двухкамерный",
                "price": 45000.0,
                "quantity": 3
            }
        ]
            }
        ]
    }
    '''

    with patch("builtins.open", mock_open(read_data=json_data)):
        categories = load_data_from_json("test.json")

    assert len(categories) == 2

    # Первая категория
    electronics = categories[0]
    assert electronics.name == "Электроника"
    assert len(electronics.get_products_list()) == 2

    # Вторая категория
    appliances = categories[1]
    assert appliances.name == "Бытовая техника"
    assert len(appliances.get_products_list()) == 1

def test_product_addition_with_zero_quantity():
    """Проверяет сложение продуктов, один из которых имеет нулевое количество."""
    product1 = Product("Товар 1", "Описание 1", 100.0, 5)
    product2 = Product("Товар 2", "Описание 2", 200.0, 0)  # нулевое количество

    total_value = product1 + product2
    expected_value = (100.0 * 5) + (200.0 * 0)  # 500 + 0
    assert total_value == expected_value

def test_category_str_representation_with_no_products():
    """Проверяет строковое представление категории без товаров."""
    empty_category = Category("Пустая", "Категория без товаров")
    expected = "Пустая, количество продуктов: 0 шт."
    assert str(empty_category) == expected

# --- Дополнительные тесты для edge cases ---

def test_product_price_setter_same_price():
    """Проверяет установку цены, равной текущей (не должно запрашивать подтверждение)."""
    product = Product("Тест", "Описание", 1000.0, 5)

    with patch("builtins.input") as mock_input:
        product.price = 1000.0  # та же цена
        mock_input.assert_not_called()  # подтверждение не запрашивается
    assert product.price == 1000.0

def test_new_product_with_none_products_list():
    """Проверяет new_product с products_list=None (должно создать новый продукт)."""
    product_data = {
        "name": "Новый товар",
        "description": "Без дубликатов",
        "price": 1500.0,
        "quantity": 2
    }

    new_product = Product.new_product(product_data, None)
    assert isinstance(new_product, Product)
    assert new_product.name == "Новый товар"
    assert new_product.quantity == 2
