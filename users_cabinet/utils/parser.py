import os

import requests
from dotenv import load_dotenv


load_dotenv()


def get_json(market_id: int, offset: int, sort_by: str) -> dict:
    return {
        'operationName': 'getMakeSearch',
        'variables': {
            'queryInput': {
                'categoryId': '1',
                'shopId': market_id,
                'showAdultContent': 'NONE',
                'filters': [],
                'sort': sort_by,
                'pagination': {
                    'offset': offset,
                    'limit': 100,
                },
                'correctQuery': False,
                'getFastCategories': True,
            },
        },
        'query': 'query getMakeSearch($queryInput: MakeSearchQueryInput!) {\n  makeSearch(query: $queryInput) {\n    id\n    queryId\n    queryText\n    category {\n      ...CategoryShortFragment\n      __typename\n    }\n    categoryTree {\n      category {\n        ...CategoryFragment\n        __typename\n      }\n      total\n      __typename\n    }\n    items {\n      catalogCard {\n        __typename\n        ...SkuGroupCardFragment\n      }\n      __typename\n    }\n    facets {\n      ...FacetFragment\n      __typename\n    }\n    total\n    mayHaveAdultContent\n    categoryFullMatch\n    offerCategory {\n      title\n      id\n      __typename\n    }\n    correctedQueryText\n    categoryWasPredicted\n    fastCategories {\n      category {\n        ...FastCategoryFragment\n        __typename\n      }\n      total\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment FacetFragment on Facet {\n  filter {\n    id\n    title\n    type\n    measurementUnit\n    description\n    __typename\n  }\n  buckets {\n    filterValue {\n      id\n      description\n      image\n      name\n      __typename\n    }\n    total\n    __typename\n  }\n  range {\n    min\n    max\n    __typename\n  }\n  __typename\n}\n\nfragment CategoryFragment on Category {\n  id\n  icon\n  parent {\n    id\n    __typename\n  }\n  seo {\n    header\n    metaTag\n    __typename\n  }\n  title\n  adult\n  __typename\n}\n\nfragment CategoryShortFragment on Category {\n  id\n  parent {\n    id\n    title\n    __typename\n  }\n  title\n  __typename\n}\n\nfragment FastCategoryFragment on Category {\n  id\n  parent {\n    id\n    title\n    __typename\n  }\n  title\n  seo {\n    header\n    metaTag\n    __typename\n  }\n  __typename\n}\n\nfragment SkuGroupCardFragment on SkuGroupCard {\n  ...DefaultCardFragment\n  photos {\n    key\n    link(trans: PRODUCT_540) {\n      high\n      low\n      __typename\n    }\n    previewLink: link(trans: PRODUCT_240) {\n      high\n      low\n      __typename\n    }\n    __typename\n  }\n  badges {\n    ... on BottomTextBadge {\n      backgroundColor\n      description\n      id\n      link\n      text\n      textColor\n      __typename\n    }\n    __typename\n  }\n  characteristicValues {\n    id\n    value\n    title\n    characteristic {\n      values {\n        id\n        title\n        value\n        __typename\n      }\n      title\n      id\n      __typename\n    }\n    __typename\n  }\n  __typename\n}\n\nfragment DefaultCardFragment on CatalogCard {\n  adult\n  favorite\n  feedbackQuantity\n  id\n  minFullPrice\n  minSellPrice\n  offer {\n    due\n    icon\n    text\n    textColor\n    __typename\n  }\n  badges {\n    backgroundColor\n    text\n    textColor\n    __typename\n  }\n  ordersQuantity\n  productId\n  rating\n  title\n  __typename\n}',
    }


def get_market_id(market: str) -> int | None:
    """Получить market_id"""
    response = requests.get(f'https://api.kazanexpress.ru/api/shop/{market}').json()
    try:
        return response['payload'].get('id')
    except AttributeError:
        return
    except TypeError:
        return


def get_products(market_id: int, offset: int, sort_by: str) -> dict:
    """Получить данные со страницы магазина"""
    headers = {
        'apollographql-client-name': 'web-customers',
        'content-type': 'application/json',
        'x-iid': f'{os.getenv("X-IID")}',
    }

    json_data = get_json(market_id, offset, sort_by)
    response = requests.post('https://graphql.kazanexpress.ru/', headers=headers, json=json_data).json()
    return response


def get_product_id(market: str) -> set | None:
    """Получить уникальные productId"""
    market_id = get_market_id(market)
    product_id = set()
    page_size = 100
    offset = 0
    sort_by = 'BY_PRICE_ASC'

    if market_id:
        data_items = get_products(market_id, offset, sort_by)
        total_items = data_items['data']['makeSearch']['total']  # Получить суммарное количество товаров
        total_pages = (total_items + page_size - 1) // page_size  # Определить общее количество страниц

        for page in range(total_pages):
            if offset >= 10_000:
                sort_by = 'BY_PRICE_DESC'
                offset = 0
            data = get_products(market_id, offset, sort_by)
            offset += 100
            temp_set = {i['catalogCard']['productId'] for i in data['data']['makeSearch']['items']}
            product_id |= temp_set
        return product_id


def get_product_data(product_id: int = 2097581):
    url = f'https://api.kazanexpress.ru/api/v2/product/{product_id}'
    r = requests.get(url).json()
    data = r['payload']['data']
    title = data['title']
    rating = data['rating']
    characteristics = data['characteristics']
    skulist = data['skuList']

    params_list = []

    for i, param in enumerate(characteristics):
        value_list = []
        for j, value in enumerate(param['values']):
            value_dict = {'index': j, 'title': value['title']}
            value_list.append(value_dict)
        param_dict = {i: param['title'], 'values': value_list}
        params_list.append(param_dict)

    print(params_list)


get_product_data()
