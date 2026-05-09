import json
from unittest.mock import mock_open, patch

import pytest

from src.main import Category, LawnGrass, Product, Smartphone, load_data_from_json


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


@pytest.fixture
def sample_smartphone() -> Smartphone:
    """Фикстура для создания тестового объекта Smartphone."""
    return Smartphone(
        "iPhone 15",
        "Флагманский смартфон Apple",
        120000.0,
        5,
        "высокая",
        "15 Pro",
        "256GB",
        "чёрный",
    )


@pytest.fixture
def sample_lawn_grass() -> LawnGrass:
    """Фикстура для создания тестового объекта LawnGrass."""
    return LawnGrass(
        "Газонная трава Премиум",
        "Высококачественная газонная трава",
        2000.0,
        20,
        "Россия",
        "14 дней",
        "ярко‑зелёный",
    )


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


# --- Тесты для Smartphone ---


def test_smartphone_initialization(sample_smartphone: Smartphone):
    """Проверяет корректность инициализации объекта Smartphone."""
    assert sample_smartphone.name == "iPhone 15"
    assert sample_smartphone.model == "15 Pro"
    assert sample_smartphone.memory == "256GB"
    assert sample_smartphone.color == "чёрный"


def test_lawn_grass_initialization(sample_lawn_grass: LawnGrass):
    """Проверяет корректность инициализации объекта LawnGrass."""
    assert sample_lawn_grass.name == "Газонная трава Премиум"
    assert sample_lawn_grass.country == "Россия"
    assert sample_lawn_grass.germination_period == "14 дней"
    assert sample_lawn_grass.color == "ярко‑зелёный"


def test_smartphone_str_representation(sample_smartphone: Smartphone):
    """Проверяет строковое представление объекта Smartphone."""
    expected = "iPhone 15 (15 Pro, 256GB, чёрный), 120000.0 руб. Остаток: 5 шт."
    assert str(sample_smartphone) == expected


def test_lawn_grass_str_representation(sample_lawn_grass: LawnGrass):
    """Проверяет строковое представление объекта LawnGrass."""
    expected = "Газонная трава Премиум (Россия, 14 дней, ярко‑зелёный), 2000.0 руб. Остаток: 20 шт."
    assert str(sample_lawn_grass) == expected


def test_smartphone_addition(sample_smartphone: Smartphone):
    """Проверяет сложение двух объектов Smartphone."""
    phone2 = Smartphone(
        "Samsung S23",
        "Флагман Samsung",
        110000.0,
        3,
        "высокая",
        "S23",
        "128GB",
        "белый",
    )
    total_value = sample_smartphone + phone2
    expected_value = (120000.0 * 5) + (110000.0 * 3)  # 600 000 + 330 000
    assert total_value == expected_value


def test_lawn_grass_addition(sample_lawn_grass: LawnGrass):
    """Проверяет сложение двух объектов LawnGrass."""
    grass2 = LawnGrass(
        "Газонная трава Стандарт",
        "Обычная газонная трава",
        1500.0,
        10,
        "Россия",
        "21 день",
        "зелёный",
    )
    total_value = sample_lawn_grass + grass2
    expected_value = (2000.0 * 20) + (1500.0 * 10)  # 40 000 + 15 000
    assert total_value == expected_value


def test_smartphone_addition_different_type(
    sample_smartphone: Smartphone, sample_lawn_grass: LawnGrass
):
    """Проверяет, что нельзя складывать смартфон с газонной травой."""
    with pytest.raises(TypeError) as exc_info:
        sample_smartphone + sample_lawn_grass
    assert "Нельзя складывать смартфоны с другими типами товаров" in str(exc_info.value)


def test_lawn_grass_addition_different_type(
    sample_lawn_grass: LawnGrass, sample_smartphone: Smartphone
):
    """Проверяет, что нельзя складывать газонную траву со смартфоном."""
    with pytest.raises(TypeError) as exc_info:
        sample_lawn_grass + sample_smartphone
    assert "Нельзя складывать газонную траву с другими типами товаров" in str(
        exc_info.value
    )


# --- Тесты для Category ---


def test_category_initialization(sample_category: Category):
    """Проверяет корректность инициализации объекта Category."""
    assert sample_category.name == "Электроника"
    assert sample_category.description == "Электронные устройства"
    assert len(sample_category.get_products_list()) == 2
    assert Category.category_count == 1
    assert Category.product_count == 2


def test_category_add_product(sample_category: Category, sample_smartphone: Smartphone):
    """Проверяет добавление продукта в категорию."""
    sample_category.add_product(sample_smartphone)
    assert len(sample_category.get_products_list()) == 3
    assert Category.product_count == 3


def test_category_add_invalid_product(sample_category: Category):
    """Проверяет обработку попытки добавления объекта не‑продукта в категорию."""
    with pytest.raises(TypeError) as exc_info:
        sample_category.add_product("Не продукт")  # type: ignore[arg-type]
    assert "Можно добавлять только объекты класса Product или его наследников" in str(
        exc_info.value
    )


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
        "quantity": 5,
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
    mock_open(read_data="""
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
        """),
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
    with patch("builtins.open", mock_open(read_data="некорректный json {")):
        with pytest.raises(json.JSONDecodeError):
            load_data_from_json("invalid.json")


def test_category_empty_name():
    """Проверяет инициализацию категории с пустым названием (должно вызвать исключение)."""
    with pytest.raises(ValueError) as exc_info:
        Category("", "Описание пустой категории")
    assert "Название категории не может быть пустым" in str(exc_info.value)
