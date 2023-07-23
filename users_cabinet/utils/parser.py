import requests
from loguru import logger
from typing import Generator, Set, Tuple

from users_cabinet.utils.config import headers, query

class ProductId:
    def __init__(self, url: str):
        self.market = url.split('/')[-1]
        self.market_id = None
        self.page_size = 100
        self.offset = 0
        self.product_id = set()
        self.sort = 'BY_PRICE_ASC'

    def get_market_id(self) -> int | None:
        """Получить market_id"""
        response = requests.get(f'https://api.kazanexpress.ru/api/shop/{self.market}').json()
        try:
            self.market_id = response['payload'].get('id')
            return self.market_id
        except AttributeError:
            return
        except TypeError:
            return

    def get_json(self) -> dict:
        """Payload for json"""
        return {
            'operationName': 'getMakeSearch',
            'variables': {
                'queryInput': {
                    'categoryId': '1',
                    'shopId': self.market_id,
                    'showAdultContent': 'NONE',
                    'filters': [],
                    'sort': self.sort,
                    'pagination': {
                        'offset': self.offset,
                        'limit': 100,
                    },
                    'correctQuery': False,
                    'getFastCategories': True,
                },
            },
            'query': f'{query}'
        }

    def get_products(self) -> dict | None:
        """Получить данные со страницы магазина"""
        json_data = self.get_json()
        try:
            response = requests.post('https://graphql.kazanexpress.ru/', headers=headers, json=json_data).json()
            return response
        except Exception as e:
            logger.error(e)

    def get_product_id(self) -> Generator[Set, None, None]:
        """Получить уникальные productId"""
        market_id = self.get_market_id()

        if market_id:
            data_products = self.get_products()
            if data_products:

                total_items = data_products['data']['makeSearch']['total']  # Получить суммарное количество товаров
                total_pages = (total_items + self.page_size - 1) // self.page_size  # Общее количество страниц

                for page in range(total_pages):
                    if self.offset >= 10_000:
                        self.sort = 'BY_PRICE_DESC'
                        self.offset = 0
                    data = self.get_products()
                    self.offset += 100
                    temp_set = {i['catalogCard']['productId'] for i in data['data']['makeSearch']['items']}
                    products_id = temp_set - self.product_id  # Новые товары, не встречавшиеся ранее
                    self.product_id.update(temp_set)  # Обновление множества с уже просмотренными товарами
                    yield products_id
            else:
                logger.error('ошибка получения products')
        else:
            logger.error('ошибка получения marketId')

class ProductSKU:
    def get_product_data(self, product_id: int) -> Generator[Tuple, None, None]:
        """Генератор с данными для каждого SKU"""
        data = self.fetch_product_data(product_id)
        product = data['title']  # название продукта
        rating = data['rating']
        characteristics = data['characteristics']  # может быть пустым
        skulist = data['skuList']  # список SKU
        param_list = self.get_param_list(characteristics)

        for sku in skulist:
            sku_id: int = sku['id']  # уникальный идентификатор
            params_list = sku['characteristics']  # список параметров конкретного SKU
            available_amount = sku['availableAmount']  # доступный остаток
            price = sku['purchasePrice']  # цена
            values = self.get_param_values(param_list, params_list)
            yield sku_id, product, price, available_amount, rating, values

    @staticmethod
    def fetch_product_data(product_id: int) -> dict:
        """Получить данные всех sku для productId"""
        response = requests.get(f'https://api.kazanexpress.ru/api/v2/product/{product_id}').json()
        return response['payload']['data']

    @staticmethod
    def get_param_list(characteristics: dict) -> list:
        """Список доступных параметров в productId"""
        param_list = []
        if characteristics:
            for i, param in enumerate(characteristics):
                value_list = [value['title'] for value in param['values']]
                param_dict = {'charIndex': i, 'title': param['title'], 'values': value_list}
                param_list.append(param_dict)
        return param_list

    @staticmethod
    def get_param_values(param_list: list, params_list: list) -> list:
        """Словарь с параметрами для каждого SKU"""
        values = []
        if param_list:
            for param in params_list:
                char_index = param['charIndex']  # индекс названия параметра
                value_index = param['valueIndex']  # индекс параметра
                current_param: dict = param_list[char_index]  # параметры товара
                value_name = current_param['values'][value_index]  # значение параметра
                values.append(value_name)
        return values
