import json
from typing import List


class ZeroQuantityError(Exception):
    """Исключение для товаров с нулевым или отрицательным количеством."""

    pass


class Product:
    product_count = 0

    def __init__(self, name: str, description: str, price: float, quantity: int):
        if not name or not name.strip():
            raise ValueError("Имя товара не может быть пустым")
        self.name = name.strip()
        self.description = description
        self.price = price
        if quantity <= 0:
            raise ZeroQuantityError(
                "Товар с нулевым или отрицательным количеством не может быть добавлен"
            )
        self._quantity = quantity

        # Увеличиваем счётчик при создании продукта
        Product.product_count += 1

    @property
    def name(self) -> str:
        """Геттер для имени товара."""
        return self._name

    @name.setter
    def name(self, value: str):
        """Сеттер для имени товара с валидацией."""
        if not value or not value.strip():
            raise ValueError("Имя товара не может быть пустым")
        self._name = value.strip()

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float):
        if value < 0:
            print("Цена не должна быть нулевая или отрицательная")
            raise ValueError("Цена не должна быть нулевая или отрицательная")
        self._price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int):
        if value <= 0:
            raise ZeroQuantityError(
                "Товар с нулевым или отрицательным количеством не может быть добавлен"
            )
        self._quantity = value

    def __add__(self, other: "Product") -> "Product":
        if not isinstance(other, Product):
            raise TypeError("Можно складывать только товары одного типа")

        total_qty = self.quantity + other.quantity
        new_price = (
            self.price * self.quantity + other.price * other.quantity
        ) / total_qty

        # Создаем новый объект с усредненной ценой и суммарным количеством
        # Имя и описание берем от первого, так как это агрегированный товар
        return Product(
            f"Агрегат: {self.name}/{other.name}",
            f"{self.description} + {other.description}",
            new_price,
            total_qty,
        )

    def __str__(self):
        return f"{self.name}, {self.price} руб., {self.quantity} шт."

    def __repr__(self):
        return f"Product('{self.name}', {self.price}, {self.quantity})"


class Smartphone(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        performance: str,
        model: str,
        memory: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.performance: str = performance
        self.model: str = model
        self.memory: str = memory
        self.color: str = color

    def __add__(self, other: Product) -> Product:
        if not isinstance(other, Smartphone):
            raise TypeError("Можно складывать только смартфоны")

        total_qty = self.quantity + other.quantity
        new_price = (
            self.price * self.quantity + other.price * other.quantity
        ) / total_qty

        return Smartphone(
            f"Агрегат: {self.name}/{other.name}",
            f"{self.description} + {other.description}",
            new_price,
            total_qty,
            self.performance,
            self.model,
            self.memory,
            self.color,
        )

    def __str__(self):
        return f"{self.name} ({self.model}, {self.memory}, {self.color}), {self.price} руб., {self.quantity} шт."


class LawnGrass(Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other: Product) -> Product:
        if not isinstance(other, LawnGrass):
            raise TypeError("Можно складывать только газонную траву")

        total_qty = self.quantity + other.quantity
        new_price = (
            self.price * self.quantity + other.price * other.quantity
        ) / total_qty

        return LawnGrass(
            f"Агрегат: {self.name}/{other.name}",
            f"{self.description} + {other.description}",
            new_price,
            total_qty,
            self.country,
            self.germination_period,
            self.color,
        )

    def __str__(self):
        return f"{self.name} ({self.country}, {self.germination_period}, {self.color}), {self.price} руб., {self.quantity} шт."


class Category:
    def __init__(self, name: str, description: str = ""):
        if not name or not name.strip():
            raise ValueError("Название категории не может быть пустым")
        self.name = name
        self.description = description
        self._products: List[Product] = []

    def add_product(self, product: Product):
        if not isinstance(product, Product):
            raise TypeError("Можно добавлять только объекты Product")
        # Теперь безопасно обращаться к атрибутам
        print(f"Попытка добавить товар: {product.name}")
        self._products.append(product)

    def average_price(self) -> float:
        if not self._products:
            return 0.0

        total_cost = sum(p.price * p.quantity for p in self._products)
        total_qty = sum(p.quantity for p in self._products)

        return total_cost / total_qty if total_qty > 0 else 0.0

    def __len__(self):
        return len(self._products)

    def __iter__(self):
        return iter(self._products)

    def __getitem__(self, index: int) -> Product:
        return self._products[index]

    def __str__(self):
        return f"{self.name}, количество товаров: {len(self._products)} шт."

    def __repr__(self):
        return f"Category('{self.name}', '{self.description}', {len(self)} products)"

    @classmethod
    def load_data_from_json(cls, file_path: str) -> "Category":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError as e:
            raise e
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл не найден: {file_path}")

        categories_data = data.get("categories", [])

        if not categories_data:
            return cls("Пустая категория", "Нет данных")

        cat_data = categories_data[0]

        category = cls(
            cat_data.get("name", "Без имени"), cat_data.get("description", "")
        )

        products_data = cat_data.get("products", [])

        # ✅ ДОБАВЛЕНА ЭТА СТРОКА: явно говорим, что product может быть любым Product
        product: Product

        for product_data in products_data:
            product_type = product_data.get("product_type")
            if product_type == "smartphone":
                product = Smartphone(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    quantity=product_data["quantity"],
                    performance=product_data.get("performance", ""),
                    # Добавил дефолтные значения, чтобы mypy не ругался на None
                    model=product_data.get("model", ""),
                    memory=product_data.get("memory", ""),
                    color=product_data.get("color", ""),
                )
            elif product_type == "lawngrass":
                product = LawnGrass(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    quantity=product_data["quantity"],
                    country=product_data.get("country", ""),
                    germination_period=product_data.get("germination_period", ""),
                    color=product_data.get("color", ""),
                )
            else:
                product = Product(
                    name=product_data["name"],
                    description=product_data["description"],
                    price=product_data["price"],
                    quantity=product_data["quantity"],
                )
            category.add_product(product)

        return category


class Order:
    def __init__(self, product: Product, quantity: int):
        if quantity < 0:
            raise ValueError("Количество товара в заказе не может быть отрицательным")
        if quantity == 0:
            raise ValueError("Количество товара в заказе не может быть нулевым")
        if quantity > product.quantity:
            raise ValueError("Недостаточно товара на складе")

        self.product = product
        self.quantity = quantity

    @property
    def total_cost(self):
        return self.product.price * self.quantity


if __name__ == "__main__":  # pragma: no cover
    # Блок main для ручного тестирования
    try:
        # Тест валидации количества
        invalid_product = Product("Бракованный товар", "Описание", 100.0, 0)
    except ZeroQuantityError as e:
        print(f"Поймана ожидаемая ошибка: {e}")

    # Создание товаров
    product1 = Product("Samsung Galaxy S23 Ultra", "256GB, Серый цвет", 180000.0, 5)
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)

    category1 = Category("Смартфоны", "Категория смартфонов")
    category1.add_product(product1)
    category1.add_product(product2)

    print(
        f"Средний ценник в категории 'Смартфоны': {category1.average_price():.2f} руб."
    )
    print(f"Строковое представление категории: {category1}")

    # Тест сложения смартфонов — только смартфоны!
    smartphone1: Smartphone = Smartphone(
        "iPhone", "Смартфон", 1000.0, 2, "высокая", "15 Pro", "256GB", "серый"
    )
    smartphone2: Smartphone = Smartphone(
        "Galaxy", "Смартфон", 900.0, 3, "высокая", "S23", "512GB", "чёрный"
    )
    result_smartphone: Product = smartphone1 + smartphone2  # результат — Product
    print(f"Результат сложения смартфонов: {result_smartphone}")

    # Тест сложения газонной травы — только газонная трава!
    grass1: LawnGrass = LawnGrass(
        "Газон 1", "Трава", 500.0, 10, "Россия", "14 дней", "зелёный"
    )
    grass2: LawnGrass = LawnGrass(
        "Газон 2", "Трава премиум", 600.0, 15, "Россия", "21 день", "тёмно‑зелёный"
    )
    result_grass: Product = grass1 + grass2  # результат — Product
    print(f"Результат сложения газонной травы: {result_grass}")

    # Тест заказа
    try:
        order = Order(product1, 2)
        print(f"Стоимость заказа: {order.total_cost} руб.")
    except ValueError as e:
        print(f"Ошибка при создании заказа: {e}")

    # Демонстрация работы с коллекцией разных продуктов
    print("\n--- Демонстрация коллекции разных продуктов ---")
    products: list[Product] = [smartphone1, grass1, product1]

    for product in products:
        print(f"{product.name}, {product.price} руб., {product.quantity} шт.")

        # Если нужен доступ к специфичным атрибутам — проверяем тип
        if isinstance(product, Smartphone):
            print(f"  Модель: {product.model}, Память: {product.memory}")
        elif isinstance(product, LawnGrass):
            print(f"  Страна: {product.country}, Цвет: {product.color}")
