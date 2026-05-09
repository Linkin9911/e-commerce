import json
from typing import List, Optional


class CategoryIterator:
    """Итератор для перебора товаров в категории."""

    def __init__(self, category: "Category"):
        self._products = category.get_products_list()
        self._index = 0

    def __iter__(self) -> "CategoryIterator":
        return self

    def __next__(self) -> "Product":
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product


class Product:
    """Класс для представления продукта в магазине."""

    def __init__(self, name: str, description: str, price: float, quantity: int):
        self.name = name
        self.description = description
        self.__price = price
        self.quantity = quantity

    @property
    def price(self) -> float:
        return self.__price

    @price.setter
    def price(self, value: float):
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
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

        if products_list:
            for existing_product in products_list:
                if existing_product.name == name:
                    existing_product.quantity += quantity
                    if price > existing_product.price:
                        existing_product.price = price
            return existing_product

        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """Сложение товаров только одного типа."""
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать товары разных типов")
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """Класс для представления смартфонов."""

    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        efficiency: str,
        model: str,
        memory: str,
        color: str,
    ):
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other: Product) -> float:
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать смартфоны с другими типами товаров")
        return super().__add__(other)

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.model}, {self.memory}, {self.color}), "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )


class LawnGrass(Product):
    """Класс для представления газонной травы."""

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

    def __add__(self, other: Product) -> float:
        if type(self) is not type(other):
            raise TypeError("Нельзя складывать газонную траву с другими типами товаров")
        return super().__add__(other)

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.country}, {self.germination_period}, {self.color}), "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )


class Category:
    """Класс для представления категории товаров."""

    category_count: int = 0
    product_count: int = 0

    def __init__(
        self, name: str, description: str, products: Optional[List[Product]] = None
    ):
        if not name:
            raise ValueError("Название категории не может быть пустым")
        self.name = name
        self.description = description
        self.__products: List[Product] = []

        if products:
            for product in products:
                self.add_product(product)
        Category.category_count += 1

    def add_product(self, product: Product):
        """Добавляет продукт в категорию."""
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты класса Product или его наследников"
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[str]:
        return [str(product) for product in self.__products]

    @property
    def products_list(self) -> List[Product]:
        return self.__products

    def get_products_list(self) -> List[Product]:
        return self.__products

    def __str__(self) -> str:
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> CategoryIterator:
        return CategoryIterator(self)


def load_data_from_json(filename: str) -> List[Category]:
    """Загружает данные о категориях и товарах из JSON файла."""
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
    if "categories" not in data or not data["categories"]:
        return categories

    for category_data in data["categories"]:
        products: List[Product] = []
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
    """
    Демонстрационный блок для тестирования функциональности классов Product и Category.
    Включает проверку новых методов: __str__, __add__ и итератора.
    """
    # Создаём товары
    product1 = Product(
        "Samsung Galaxy S23 Ultra", "256GB, Серый цвет, 200MP камера", 180000.0, 5
    )
    product2 = Product("Iphone 15", "512GB, Gray space", 210000.0, 8)
    product3 = Product("Xiaomi Redmi Note 11", "1024GB, Синий", 31000.0, 14)

    # Создаём категорию с тремя товарами
    category1 = Category(
        "Смартфоны",
        "Смартфоны, как средство не только коммуникации, но и получения дополнительных функций для удобства жизни",
        [product1, product2, product3],
    )

    print("=== Изначальные товары в категории ===")
    print([str(p) for p in category1.get_products_list()])
    print(f"Общее количество категорий: {Category.category_count}")
    print(f"Общее количество товаров во всех категориях: {Category.product_count}")

    print(f"Строковое представление категории: {str(category1)}")

    # Добавляем новый товар
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print("\n=== После добавления телевизора ===")
    print(f"Строковое представление категории: {str(category1)}")
    print(f"Общее количество товаров: {Category.product_count}")

    # Демонстрируем работу new_product с дубликатом
    print("\n=== Тестируем new_product с дубликатом ===")
    duplicate_data = {
        "name": "Samsung Galaxy S23 Ultra",
        "description": "Дубликат с увеличенным количеством",
        "price": 190000.0,  # выше текущей цены — должна обновиться
        "quantity": 2,
    }
    result_product = Product.new_product(duplicate_data, category1.get_products_list())
    print(f"Товар найден и обновлён: {result_product.name}")
    print(f"Новое количество: {result_product.quantity} шт.")  # 5 + 2 = 7
    print(f"Новая цена: {result_product.price} руб.")  # 190 000 руб. (выше старой)

    # Тестируем строковое представление продуктов
    print("\n=== Строковое представление отдельных продуктов ===")
    for product in [product1, product2, product3, product4]:
        print(str(product))

    # Тестируем сложение продуктов
    print("\n=== Тестирование сложения продуктов (__add__) ===")
    total_value = product1 + product2
    print(f"{product1.name} + {product2.name}: {total_value} руб.")
    total_value_2 = product3 + product4
    print(f"{product3.name} + {product4.name}: {total_value_2} руб.")

    # Тестируем итератор
    print("\n=== Итерация по товарам категории ===")
    print("Перебираем все товары в категории 'Смартфоны':")
    for idx, product in enumerate(category1, 1):
        print(f"{idx}. {product}")

    # Тестируем изменение цены (снижение — должен запросить подтверждение)
    print("\n=== Тестируем снижение цены ===")
    print(f"Текущая цена {result_product.name}: {result_product.price} руб.")
    result_product.price = 170000.0  # Запрос подтверждения в консоли
    print(f"Итоговая цена: {result_product.price} руб.")

    # Тестируем недопустимые значения цены
    print("\n=== Тестируем недопустимые цены ===")
    result_product.price = -100  # Ошибка
    print(f"Цена после попытки установить -100: {result_product.price} руб.")
