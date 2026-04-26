import json
from typing import List, Optional


class Product:
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
                        existing_product.price = price  # ← Теперь с правильным отступом
                    return existing_product  # ← Возвращаем только найденный продукт

        # Если дубликат не найден, создаём новый продукт
        return cls(name, description, price, quantity)


class Category:
    """
    Класс для представления категории товаров.
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
        self.__products: List['Product'] = []  # Явная аннотация типа

        if products:
            self.__products.extend(products)

        # Сначала увеличиваем счётчик категорий
        Category.category_count += 1

        # Теперь добавляем продукты поочерёдно через add_product, чтобы корректно увеличить product_count
        if products is not None:
            for product in products:
                self.add_product(product)

    def add_product(self, product: Product):
        """
        Добавляет продукт в категорию и увеличивает счётчик товаров на 1.

        Args:
            product (Product): объект продукта для добавления.
        """
        self.__products.append(product)
        Category.product_count += 1  # Прибавляем ровно 1 за каждый добавленный продукт

    @property
    def products(self) -> str:
        """
        Геттер для получения форматированного списка товаров.

        Returns:
            str: форматированная строка с информацией о товарах.
        """
        result = ""
        for product in self.__products:
            result += f"{product.name}, {product.price} руб. Остаток: {product.quantity} шт.\n"
        return result

    def get_products_list(self) -> List[Product]:
        """
        Возвращает внутренний список товаров (для тестирования).

        Returns:
            List[Product]: список объектов Product в категории.
        """
        return self.__products


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
                products.append(product)  # Теперь внутри цикла

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
    print(category1.products)
    print(f"Общее количество категорий: {Category.category_count}")
    print(f"Общее количество товаров во всех категориях: {Category.product_count}")

    # Добавляем новый товар
    product4 = Product('55" QLED 4K', "Фоновая подсветка", 123000.0, 7)
    category1.add_product(product4)
    print("\n=== После добавления телевизора ===")
    print(category1.products)
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

    # Тестируем изменение цены (снижение — должен запросить подтверждение)
    print("\n=== Тестируем снижение цены ===")
    print(f"Текущая цена {result_product.name}: {result_product.price} руб.")
    result_product.price = 170000.0  # Запрос подтверждения в консоли
    print(f"Итоговая цена: {result_product.price} руб.")

    # Тестируем недопустимые значения цены
    print("\n=== Тестируем недопустимые цены ===")
    result_product.price = -100  # Ошибка
    print(f"Цена после попытки установить -100: {result_product.price} руб.")
    result_product.price = 0  # Ошибка
    print(f"Цена после попытки установить 0: {result_product.price} руб.")
