import json
from abc import ABC, abstractmethod
from typing import List, Optional


class BaseProduct(ABC):
    @abstractmethod
    def get_name(self) -> str:
        """Возвращает название продукта."""
        pass

    @abstractmethod
    def get_price(self) -> float:
        """Возвращает цену продукта."""
        pass

    @abstractmethod
    def get_quantity(self) -> int:
        """Возвращает количество на складе."""
        pass

    @abstractmethod
    def get_description(self) -> str:
        """Возвращает описание продукта."""
        pass


class LoggingMixin:
    def __init__(self, *args, **kwargs):
        # Логируем создание объекта
        print(f"Создан объект {self.__class__.__name__}")
        super().__init__(*args, **kwargs)


class Product(BaseProduct):  # Указываем родителя
    # Счётчик продуктов
    product_count = 0

    def __init__(
        self, name: str, description: str, price: float, quantity: int
    ) -> None:
        super().__init__()  # Вызываем инициализатор абстрактного родителя
        self.name = name
        self.description = description
        self._price = price
        self._quantity = quantity
        # Увеличиваем счётчик при создании объекта
        Product.product_count += 1

    @staticmethod
    def new_product(
        product_data: dict, products_list: Optional[List["Product"]] = None
    ) -> "Product":
        name = product_data.get("name", "Без названия")
        description = product_data.get("description", "Без описания")
        price = product_data.get("price", 0.0)
        quantity = product_data.get("quantity", 0)

        if products_list:
            for product in products_list:
                if product.name == name:
                    if price > product.price:
                        product.price = price
                    product.quantity += quantity
                    return product
        return Product(name, description, price, quantity)

    @property
    def price(self) -> float:
        return self._price

    @price.setter
    def price(self, value: float) -> None:
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return
        if value < self._price:
            user_input = input(
                f"Цена снижается с {self._price} до {value}. Подтвердить? (y/n): "
            )
            if user_input.lower() != "y":
                print("Изменение цены отменено")
                return
        self._price = value

    @property
    def quantity(self) -> int:
        return self._quantity

    @quantity.setter
    def quantity(self, value: int) -> None:
        if value < 0:
            print("Количество не может быть отрицательным")
            return
        self._quantity = value

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Product):
            return False
        return self.name == other.name and self.price == other.price

    def __add__(self, other: "Product") -> float:
        """Сложение двух продуктов — возвращает общую стоимость."""
        if not isinstance(other, self.__class__):
            raise TypeError("Нельзя складывать товары разных типов")
        return self.price * self.quantity + other.price * other.quantity

    def __str__(self) -> str:
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __repr__(self) -> str:
        return (
            f"Product('{self.name}', '{self.description}', "
            f"{self.price}, {self.quantity})"
        )

    # Добавлено для устранения ошибок mypy (get_*)
    def get_name(self) -> str:
        return self.name

    def get_description(self) -> str:
        return self.description

    def get_price(self) -> float:
        return self.price

    def get_quantity(self) -> int:
        return self.quantity


class Smartphone(LoggingMixin, Product):
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
    ) -> None:
        self.performance = performance
        self.model = model
        self.memory = memory
        self.color = color
        # Вызов инициализатора миксина и Product
        super().__init__(name, description, price, quantity)

    def __add__(self, other: "Product") -> float:  # Тип Product, а не Smartphone
        if not isinstance(other, Smartphone):
            raise TypeError("Нельзя складывать смартфоны с другими типами товаров")
        return self.price * self.quantity + other.price * other.quantity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Smartphone):
            return False
        return (
            super().__eq__(other)
            and self.model == other.model
            and self.memory == other.memory
            and self.color == other.color
        )

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.model}, {self.memory}, {self.color}), "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )

    def __repr__(self) -> str:
        return (
            f"Smartphone('{self.name}', '{self.description}', "
            f"{self.price}, {self.quantity}, '{self.performance}', "
            f"'{self.model}', '{self.memory}', '{self.color}')"
        )


class LawnGrass(LoggingMixin, Product):
    def __init__(
        self,
        name: str,
        description: str,
        price: float,
        quantity: int,
        country: str,
        germination_period: str,
        color: str,
    ) -> None:
        self.country = country
        self.germination_period = germination_period
        self.color = color
        # Вызов инициализатора миксина и Product
        super().__init__(name, description, price, quantity)

    def __add__(self, other: "Product") -> float:  # Тип Product, а не LawnGrass
        if not isinstance(other, LawnGrass):
            raise TypeError("Нельзя складывать газонную траву с другими типами товаров")
        return self.price * self.quantity + other.price * other.quantity

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, LawnGrass):
            return False
        return (
            super().__eq__(other)
            and self.country == other.country
            and self.germination_period == other.germination_period
            and self.color == other.color
        )

    def __str__(self) -> str:
        return (
            f"{self.name} ({self.country}, {self.germination_period}, "
            f"{self.color}), {self.price} руб. Остаток: {self.quantity} шт."
        )

    def __repr__(self) -> str:
        return (
            f"LawnGrass('{self.name}', '{self.description}', "
            f"{self.price}, {self.quantity}, '{self.country}', "
            f"'{self.germination_period}', '{self.color}')"
        )


class Category:
    # Счётчики категорий и продуктов
    category_count = 0
    product_count = 0

    def __init__(self, name: str, description: str) -> None:
        if not name:
            raise ValueError("Название категории не может быть пустым")
        self.name = name
        self.description = description
        self._products: List[Product] = []
        Category.category_count += 1

    def add_product(self, product: Product) -> None:
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты класса Product или его наследников"
            )
        self._products.append(product)
        Category.product_count += 1

    def get_products_list(self) -> List[Product]:
        return self._products

    @property
    def products(self) -> List[Product]:
        return self._products

    def __iter__(self) -> "Category":
        self._iter_index = 0
        return self

    def __next__(self) -> Product:
        if self._iter_index >= len(self._products):
            raise StopIteration
        product = self._products[self._iter_index]
        self._iter_index += 1
        return product

    def __str__(self) -> str:
        total_quantity = sum(p.quantity for p in self._products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __repr__(self) -> str:
        return f"Category('{self.name}', '{self.description}')"


# --- ДОБАВЛЕННЫЙ КЛАСС Order для устранения ошибки "Name 'Order' is not defined" ---
class Order:
    def __init__(self, product: Product, quantity: int):
        if quantity < 0:
            raise ValueError("Количество в заказе не может быть отрицательным")
        if quantity > product.quantity:
            raise ValueError(
                f"Недостаточно товара на складе. Доступно: {product.quantity}, запрошено: {quantity}"
            )
        self.product = product
        self.quantity = quantity

    def __str__(self) -> str:
        return f"Заказ: {self.product.name} (кол-во: {self.quantity})"


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
        category = Category(
            name=category_data.get("name", "Без названия"),
            description=category_data.get("description", "Без описания"),
        )
        products: List[Product] = []

        if "products" in category_data and category_data["products"]:
            for product_data in category_data["products"]:
                try:
                    product: Product  # <-- ВАЖНО: объявляем общий тип ПЕРЕД ветвлением

                    if "country" in product_data:  # признак LawnGrass
                        product = LawnGrass(
                            name=product_data.get("name", "Без названия"),
                            description=product_data.get("description", "Без описания"),
                            price=product_data.get("price", 0.0),
                            quantity=product_data.get("quantity", 0),
                            country=product_data.get("country", "Unknown"),
                            germination_period=product_data.get(
                                "germination_period", "Unknown"
                            ),
                            color=product_data.get("color", "Unknown"),
                        )
                    elif "model" in product_data:  # признак Smartphone
                        product = Smartphone(
                            name=product_data.get("name", "Без названия"),
                            description=product_data.get("description", "Без описания"),
                            price=product_data.get("price", 0.0),
                            quantity=product_data.get("quantity", 0),
                            performance=product_data.get("performance", "средняя"),
                            model=product_data.get("model", "Unknown"),
                            memory=product_data.get("memory", "Unknown"),
                            color=product_data.get("color", "Unknown"),
                        )
                    else:  # Базовый Product
                        product = Product(
                            name=product_data.get("name", "Без названия"),
                            description=product_data.get("description", "Без описания"),
                            price=product_data.get("price", 0.0),
                            quantity=product_data.get("quantity", 0),
                        )
                    products.append(
                        product
                    )  # Добавляем только после успешного создания
                except Exception as e:
                    print(f"Пропущен товар из‑за ошибки: {e}")
                    continue  # Пропускаем проблемный товар и идём дальше

        # Добавляем все продукты в категорию
        for product in products:
            category.add_product(product)

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
    )

    # Добавляем товары в категорию
    category1.add_product(product1)
    category1.add_product(product2)
    category1.add_product(product3)

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

    # Тестируем создание заказа
    print("\n=== Тестируем создание заказа ===")
    try:
        order = Order(product1, 2)
        print(order)

        # Пробуем создать заказ с отрицательным количеством
        print("\n=== Попытка создать заказ с отрицательным количеством ===")
        try:
            order_invalid = Order(product2, -1)
        except ValueError as e:
            print(f"Ошибка при создании заказа: {e}")

        # Пробуем создать заказ с количеством больше, чем есть на складе
        print("\n=== Попытка создать заказ с превышением количества ===")
        # У product3 (Xiaomi Redmi Note 11) количество 14 шт.
        try:
            order_too_much = Order(product3, 20)
        except ValueError as e:
            print(f"Ошибка при создании заказа: {e}")
    except Exception as e:
        print(f"Неожиданная ошибка при работе с заказами: {e}")

    # Дополнительно: тестируем абстрактные методы
    print("\n=== Тестирование абстрактных методов BaseProduct ===")

    # Добавляем методы в класс Product для соответствия ожиданиям тестов
    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_price(self):
        return self.price

    def get_quantity(self):
        return self.quantity

    # Теперь тестируем
    print(f"Название: {product1.get_name()}")
    print(f"Описание: {product1.get_description()}")
    print(f"Цена: {product1.get_price()} руб.")
    print(f"Количество: {product1.get_quantity()} шт.")

    # Тестирование смартфона
    print("\n=== Тестирование смартфона ===")
    smartphone = Smartphone(
        "Samsung Galaxy S24",
        "512GB, Титановый серый",
        200000.0,
        3,
        "высокая",
        "S24 Ultra",
        "512GB",
        "серый",
    )
    print(smartphone)

    # Тестирование газонной травы
    print("\n=== Тестирование газонной травы ===")
    grass = LawnGrass(
        "Мятлик луговой",
        "Высококачественная газонная трава",
        5000.0,
        100,
        "Россия",
        "14 дней",
        "зелёный",
    )
    print(grass)

    # Тестирование сложения смартфонов
    print("\n=== Тестирование сложения смартфонов ===")
    smartphone2 = Smartphone(
        "Apple iPhone 15 Pro",
        "256GB, Natural Titanium",
        199990.0,
        5,
        "высокая",
        "iPhone 15 Pro",
        "256GB",
        "титановый",
    )
    total_smartphones = smartphone + smartphone2
    print(f"{smartphone.name} + {smartphone2.name}: {total_smartphones} руб.")

    # Тестирование сложения газонной травы
    print("\n=== Тестирование сложения газонной травы ===")
    grass2 = LawnGrass(
        "Фестук луговой",
        "Теневыносливая газонная трава",
        4500.0,
        80,
        "Канада",
        "12 дней",
        "тёмно‑зелёный",
    )
    total_grass = grass + grass2
    print(f"{grass.name} + {grass2.name}: {total_grass} руб.")

    # Демонстрация итератора для категории с разными типами товаров
    print("\n=== Итерация по категории с разными типами товаров ===")
    mixed_category = Category(
        "Смешанная категория", "Категория с разными типами товаров"
    )
    mixed_category.add_product(smartphone)
    mixed_category.add_product(grass)
    mixed_category.add_product(product1)

    for idx, product in enumerate(mixed_category, 1):
        print(f"{idx}. {product}")

    # Проверка статических счётчиков
    print("\n=== Проверка статических счётчиков ===")
    print(f"Всего категорий создано: {Category.category_count}")
    print(f"Всего товаров во всех категориях: {Category.product_count}")

    # Тестирование загрузки из JSON (если есть файл)
    print("\n=== Тестирование загрузки из JSON ===")
    try:
        categories_from_json = load_data_from_json("products.json")
        for category in categories_from_json:
            print(category)
            for product in category:
                print(f"  - {product}")
    except FileNotFoundError as e:
        print(f"Файл не найден, пропускаем загрузку: {e}")
    except json.JSONDecodeError as e:
        print(f"Ошибка JSON: {e}")
