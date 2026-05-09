import json
from typing import List, Optional


class CategoryIterator:
    """
    Итератор для перебора товаров в категории.
    Позволяет использовать цикл for для обхода всех продуктов в категории.
    """

    def __init__(self, category: "Category"):
        """
        Инициализирует итератор для указанной категории.

        Args:
            category (Category): категория, товары которой нужно перебирать.
        """
        self._products = category.get_products_list()
        self._index = 0

    def __iter__(self) -> "CategoryIterator":
        """
        Возвращает сам итератор (требуется для протокола итерации).

        Returns:
            CategoryIterator: сам объект итератора.
        """
        return self

    def __next__(self) -> "Product":
        """
        Возвращает следующий товар в категории.

        Raises:
            StopIteration: когда все товары перебраны.

        Returns:
            Product: следующий объект Product в категории.
        """
        if self._index >= len(self._products):
            raise StopIteration
        product = self._products[self._index]
        self._index += 1
        return product


class Product:
    """
    Класс для представления продукта в магазине.
    Содержит информацию о названии, описании, цене и количестве товара.
    """

    def __init__(self, name: str, description: str, price: float, quantity: int):
        """
        Инициализирует объект Product.

        Args:
            name (str): название продукта.
            description (str): описание продукта.
            price (float): цена продукта, должна быть положительной.
            quantity (int): количество продукта, должно быть неотрицательным.
        """
        self.name = name
        self.description = description
        self.__price = price  # Приватный атрибут для цены
        self.quantity = quantity

    @property
    def price(self) -> float:
        """
        Геттер для приватного атрибута __price.

        Returns:
            float: текущая цена товара.
        """
        return self.__price

    @price.setter
    def price(self, value: float):
        """
        Сеттер для установки цены с проверкой.

        При снижении цены запрашивает подтверждение пользователя.

        Args:
            value (float): новая цена товара, должна быть положительной.

        Raises:
            ValueError: если новая цена отрицательная или нулевая.
        """
        if value <= 0:
            print("Цена не должна быть нулевая или отрицательная")
            return

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
        """
        Создаёт новый продукт или обновляет существующий при обнаружении дубликата.

        Если продукт с таким же именем уже есть в списке, увеличивает его количество
        и устанавливает максимальную цену.

        Args:
            product_data (dict): словарь с данными продукта, должен содержать ключи:
                - 'name' (str): название продукта;
                - 'description' (str): описание продукта;
                - 'price' (float): цена продукта;
                - 'quantity' (int): количество продукта.
            products_list (Optional[List[Product]]): список существующих продуктов
                для проверки на дубликаты.

        Returns:
            Product: новый объект Product или обновлённый существующий.
        """
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
            return existing_product  # Возвращаем только найденный продукт

        # Если дубликат не найден, создаём новый продукт
        return cls(name, description, price, quantity)

    def __str__(self) -> str:
        """
        Возвращает строковое представление продукта.

        Формат: "Название продукта, X руб. Остаток: X шт."

        Returns:
            str: форматированная строка с информацией о продукте.
        """
        return f"{self.name}, {self.price} руб. Остаток: {self.quantity} шт."

    def __add__(self, other: "Product") -> float:
        """
        Реализует сложение двух продуктов.

        Возвращает сумму произведений цены на количество для обоих объектов.

        Пример: a + b = a.price * a.quantity + b.price * b.quantity

        Args:
            other (Product): другой объект Product для сложения.

        Returns:
            float: общая стоимость всех товаров на складе для двух продуктов.
        """
        return self.price * self.quantity + other.price * other.quantity


class Smartphone(Product):
    """
    Класс для представления смартфонов.
    Наследует от Product, добавляет специфические атрибуты.
    """

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
        """
        Инициализирует объект Smartphone.

        Args:
            name (str): название смартфона.
            description (str): описание смартфона.
            price (float): цена смартфона.
            quantity (int): количество смартфонов.
            efficiency (str): производительность (например, «высокая»).
            model (str): модель смартфона.
            memory (str): объём памяти (например, «256 GB»).
            color (str): цвет смартфона.
        """
        super().__init__(name, description, price, quantity)
        self.efficiency = efficiency
        self.model = model
        self.memory = memory
        self.color = color

    def __add__(self, other: Product) -> float:  # ИЗМЕНЕНО: теперь принимает Product
        """
        Сложение двух смартфонов. Разрешено только для объектов одного типа.

        Returns:
            float: общая стоимость всех смартфонов на складе для двух объектов.
        Raises:
            TypeError: если пытаются сложить смартфоны с другими типами товаров.
        """
        if not isinstance(other, Smartphone):
            raise TypeError("Нельзя складывать смартфоны с другими типами товаров")
        return super().__add__(other)  # Используем реализацию родителя

    def __str__(self) -> str:
        """Возвращает строковое представление смартфона."""
        return (
            f"{self.name} ({self.model}, {self.memory}, {self.color}), "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )


class LawnGrass(Product):
    """
    Класс для представления газонной травы.
    Наследует от Product, добавляет специфические атрибуты.
    """

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
        """
        Инициализирует объект LawnGrass.

        Args:
            name (str): название газонной травы.
            description (str): описание газонной травы.
            price (float): цена газонной травы.
            quantity (int): количество газонной травы.
            country (str): страна‑производитель.
            germination_period (str): срок прорастания (например, «14 дней»).
            color (str): цвет травы.
        """
        super().__init__(name, description, price, quantity)
        self.country = country
        self.germination_period = germination_period
        self.color = color

    def __add__(self, other: Product) -> float:
        """
        Сложение двух газонных трав. Разрешено только для объектов одного типа.

        Returns:
            float: общая стоимость всей газонной травы на складе для двух объектов.
        Raises:
            TypeError: если пытаются сложить газонную траву с другими типами товаров.
        """
        if not isinstance(other, LawnGrass):
            raise TypeError("Нельзя складывать газонную траву с другими типами товаров")
        return super().__add__(other)  # Используем реализацию родителя

    def __str__(self) -> str:
        """Возвращает строковое представление газонной травы."""
        return (
            f"{self.name} ({self.country}, {self.germination_period}, {self.color}), "
            f"{self.price} руб. Остаток: {self.quantity} шт."
        )


class Category:
    """
    Класс для представления категории товаров.
    Содержит список продуктов и информацию о категории.
    """

    category_count: int = 0
    product_count: int = 0  # Общий счётчик всех товаров во всех категориях

    def __init__(
        self, name: str, description: str, products: Optional[List[Product]] = None
    ):
        """
        Инициализирует объект Category.

        Args:
            name (str): название категории, не может быть пустым.
            description (str): описание категории.
            products (Optional[List[Product]]): список продуктов для добавления в категорию.

        Raises:
            ValueError: если название категории пустое.
        """
        if not name:
            raise ValueError("Название категории не может быть пустым")

        self.name = name
        self.description = description
        self.__products: List[Product] = []  # Явная аннотация типа

        if products:
            # Добавляем продукты поочерёдно через add_product, чтобы корректно увеличить product_count
            for product in products:
                self.add_product(product)

        # Увеличиваем счётчик категорий
        Category.category_count += 1

    def add_product(self, product: Product):
        """
        Добавляет продукт в категорию и увеличивает счётчик товаров на 1.

        Args:
            product (Product): объект продукта для добавления.

        Raises:
            TypeError: если добавляемый объект не является экземпляром Product или его наследником.
        """
        if not isinstance(product, Product):
            raise TypeError(
                "Можно добавлять только объекты класса Product или его наследников"
            )
        self.__products.append(product)
        Category.product_count += 1

    @property
    def products(self) -> List[str]:
        """
        Геттер для получения строковых представлений товаров.

        Returns:
            List[str]: список строковых представлений продуктов в категории.
        """
        return [str(product) for product in self.__products]

    @property
    def products_list(self) -> List[Product]:
        """
        Геттер для получения внутреннего списка товаров (для обратной совместимости).

        Returns:
            List[Product]: список объектов Product в категории.
        """
        return self.__products

    def get_products_list(self) -> List[Product]:
        """
        Возвращает внутренний список товаров (для тестирования).

        Returns:
            List[Product]: список объектов Product в категории.
        """
        return self.__products

    def __str__(self) -> str:
        """
        Возвращает строковое представление категории.

        Формат: "Название категории, количество продуктов: X шт.",
        где X — сумма остатков всех продуктов в категории.

        Returns:
            str: форматированная строка с информацией о категории.
        """
        total_quantity = sum(product.quantity for product in self.__products)
        return f"{self.name}, количество продуктов: {total_quantity} шт."

    def __iter__(self) -> CategoryIterator:
        """
        Позволяет использовать категорию в цикле for для перебора товаров.

        Пример: for product in category: print(product)

        Returns:
            CategoryIterator: итератор по товарам категории.
        """
        return CategoryIterator(self)


def load_data_from_json(filename: str) -> List[Category]:
    """
    Загружает данные о категориях и товарах из JSON‑файла.

    Args:
        filename (str): путь к JSON‑файлу с данными.
    Returns:
        List[Category]: список объектов Category с загруженными данными.
    Raises:
        FileNotFoundError: если файл не найден.
        json.JSONDecodeError: если JSON в файле некорректен.
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
    if "categories" not in data or not data["categories"]:
        return categories

    for category_data in data["categories"]:
        products: List[Product] = []

        # Если есть секция products и она не пустая
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
