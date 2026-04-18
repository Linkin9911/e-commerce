import json
from typing import List, Optional


class Product:
    """
    Класс для представления товара.

    Attributes:
        name (str): название товара.
        description (str): описание товара.
        price (float): цена товара.
        quantity (int): количество товара на складе.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализирует объект Product.

        Args:
            name (str): название товара.
            description (str): описание товара.
            price (float): цена товара.
            quantity (int): количество товара на складе.
        """
        self.name = name
        self.description = description
        self.price = price
        self.quantity = quantity


class Category:
    """
    Класс для представления категории товаров.

    Attributes:
        name (str): название категории.
        description (str): описание категории.
        products (List[Product]): список товаров в категории.

    Class Attributes:
        category_count (int): общее количество созданных категорий.
        product_count (int): общее количество товаров во всех категориях.
    """

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: Optional[List[Product]] = None
    ):
        """
        Инициализирует объект Category.

        Args:
            name (str): название категории.
            description (str): описание категории.
            products (Optional[List[Product]], optional): список товаров в категории. По умолчанию — пустой список.
        """
        if products is None:
            products = []

        self.name = name
        self.description = description
        self.products = products

        # Увеличиваем счётчик категорий
        Category.category_count += 1
        # Увеличиваем счётчик товаров на сумму количеств всех товаров в текущей категории
        Category.product_count += sum(product.quantity for product in products)


def load_data_from_json(filename: str) -> List[Category]:
    """
    Загружает данные о категориях и товарах из JSON‑файла и создаёт объекты классов.

    Args:
        filename (str): путь к JSON‑файлу.

    Returns:
        List[Category]: список объектов Category, созданных на основе данных из файла.

    Raises:
        FileNotFoundError: если файл не найден.
        json.JSONDecodeError: если файл содержит некорректный JSON.
        KeyError: если в JSON отсутствуют ожидаемые ключи.
    """
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
    except FileNotFoundError:
        raise FileNotFoundError(f"Файл {filename} не найден.")
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(
            f"Некорректный JSON в файле {filename}: {e}", e.doc, e.pos
        )

    categories: List[Category] = []

    # Безопасная обработка отсутствия ключа 'categories'
    if "categories" not in data:
        return categories

    for category_data in data["categories"]:
        products: List[Product] = []
        # Безопасная обработка отсутствия ключа 'products'
        if "products" in category_data:
            for product_data in category_data["products"]:
                product = Product(
                    name=product_data.get("name", "Без названия"),
                    description=product_data.get("description", "Без описания"),
                    price=product_data.get("price", 0.0),
                    quantity=product_data.get("quantity", 0),
                )
                products.append(product)

        category = Category(
            name=category_data.get("name", "Без названия"),
            description=category_data.get("description", "Без описания"),
            products=products,
        )
        categories.append(category)

    return categories


if __name__ == "__main__":  # pragma: no cover
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    print(product1.name)
    print(product1.description)
    print(product1.price)
    print(product1.quantity)

    print(product2.name)
    print(product2.description)
    print(product2.price)
    print(product2.quantity)

    print(product3.name)
    print(product3.description)
    print(product3.price)
    print(product3.quantity)

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.name == "Смартфоны")
    print(category1.description)
    print(len(category1.products))
    print(Category.category_count)
    print(Category.product_count)

    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category2 = Category(
        "Телевизоры",
        "Современный телевизор, который позволяет наслаждаться просмотром, станет вашим другом и помощником",
        [product4],
    )

    print(category2.name)
    print(category2.description)
    print(len(category2.products))
    print(category2.products)

    print(Category.category_count)
    print(Category.product_count)
