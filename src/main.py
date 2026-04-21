import json
from typing import List, Optional


class Product:
    """
    Класс для представления товара.

    Attributes:
        name (str): название товара.
        description (str): описание товара.
        __price (float): приватный атрибут цены товара.
        quantity (int): количество товара на складе.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализирует объект Product.

        Args:
            name (str): название товара.
            description (str): описание товара.
            price (float): цена товара (должна быть положительной).
            quantity (int): количество товара на складе.
        """
        self.name = name
        self.description = description
        self.__price = price  # приватный атрибут цены
        self.quantity = quantity

    @property
    def price(self) -> float:
        """Геттер для приватного атрибута __price.

        Returns:
            float: текущая цена товара.
        """
        return self.__price

    @price.setter
    def price(self, value: float):
        """Сеттер для установки цены с проверкой.

        При снижении цены запрашивает подтверждение пользователя.

        Args:
            value (float): новая цена товара.
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
        else:
            # Проверка, существует ли уже атрибут __price
            if hasattr(self, "_Product__price") and value < self.__price:
                confirmation = input("Цена понижается. Подтвердить (y/n)? ")
                if confirmation.lower() == "y":
                    self.__price = value
            else:
                self.__price = value

    @classmethod
    def new_product(
        cls, product_data: dict, products_list: Optional[List["Product"]] = None
    ) -> "Product":
        name = product_data.get("name", "Без названия")
        description = product_data.get("description", "Без описания")
        price = product_data.get("price", 0.0)
        quantity = product_data.get("quantity", 0)

        # Проверка на дубликаты
        if products_list:
            for existing_product in products_list:
                if existing_product.name == name:
                    # Складываем количества
                    existing_product.quantity += quantity
                    # Выбираем максимальную цену
                    if price > existing_product.price:
                        existing_product.price = price
                    return existing_product

        return cls(name, description, price, quantity)


class Category:
    """
    Класс для представления категории товаров.

    Attributes:
        name (str): название категории.
        description (str): описание категории.
        __products (List[Product]): приватный список товаров в категории.
        category_count (int): общее количество созданных категорий (класс-атрибут).
        product_count (int): общее количество товаров во всех категориях (класс-атрибут).
    """

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: Optional[List[Product]] = None
    ):
        """Инициализирует объект Category.

        Args:
            name (str): название категории.
            description (str): описание категории.
            products (Optional[List[Product]], optional): список товаров в категории.
                Если None, создаётся пустой список.
        """
        if products is None:
            products = []

        self.name = name
        self.description = description
        self.__products = products  # приватный атрибут

        Category.category_count += 1
        Category.product_count += sum(product.quantity for product in products)

    def add_product(self, product: Product):
        """Добавляет продукт в категорию и увеличивает счётчик товаров.

        Args:
            product (Product): объект товара для добавления.
        """
        self.__products.append(product)
        Category.product_count += product.quantity

    @property
    def products(self) -> str:
        """Геттер для получения форматированного списка товаров.

        Returns:
            str: строка с описанием всех товаров в категории в формате:
                  "Название, Цена руб. Остаток: Количество шт.\n"
        """
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    def get_products_list(self) -> List[Product]:
        """Возвращает внутренний список товаров (для тестирования).

        Returns:
            List[Product]: список объектов Product в категории.
        """
        return self.__products


def load_data_from_json(filename: str) -> List[Category]:
    """Загружает данные о категориях и товарах из JSON‑файла и создаёт объекты классов.

    Args:
        filename (str): путь к JSON‑файлу.

    Returns:
        List[Category]: список объектов Category с загруженными данными.

    Raises:
        FileNotFoundError: если файл не найден.
        json.JSONDecodeError: если JSON в файле некорректный.
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
    if "categories" not in data:
        return categories

    for category_data in data["categories"]:
        products: List[Product] = []

        # Проверяем наличие секции "products" и её непустоту
        if "products" in category_data and category_data["products"]:
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

    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print(category1.products)
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print(category1.products)
    print(category1.product_count)

    new_product = Product.new_product(
        {
            "name": "Samsung Galaxy S23 Ultra",
            "description": "256GB, Серый цвет, 200MP камера",
            "price": 180000.0,
            "quantity": 5,
        }
    )
    print(new_product.name)
    print(new_product.description)
    print(new_product.price)
    print(new_product.quantity)

    new_product.price = 800
    print(new_product.price)

    new_product.price = -100
    print(new_product.price)
    new_product.price = 0
    print(new_product.price)
