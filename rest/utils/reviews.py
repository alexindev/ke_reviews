import datetime
import requests


def get_review(token: str) -> list | bool:
    headers = {
        'accept': 'application/json',
        'authorization': f'Bearer {token}',
    }

    reviews_list = []
    count_list = []
    page = 0
    work = True
    try:
        while work:
            for data in get_data(page, headers).get('payload'):
                timestamp_create = data['dateCreated'] / 1000
                review = {
                    'store': data['shop']['title'],
                    'product': data['product']['productTitle'],
                    'rating': data['rating'],
                    'review_id': data['reviewId'],
                    'content': data['content'],
                    'date_create': datetime.datetime.fromtimestamp(timestamp_create).strftime('%Y-%m-%d'),
                }
                reviews_list.append(review)
                count_list.append(data)
            page += 1
            if len(count_list) % 100 != 0:
                work = False
        return reviews_list
    except TypeError:
        return False


def get_data(page: int, headers: dict):
    params = {
        'page': f'{page}',
        'filter': 'NO_REPLY',
        'size': '100',
    }

    return requests.get(
        'https://api.business.kazanexpress.ru/api/seller/product-reviews',
        params=params,
        headers=headers,
    ).json()
