import requests
from loguru import logger


def get_store(url: str) -> bool:
    try:
        store = url.strip().split('/')[-1]
        response = requests.get(f'https://api.kazanexpress.ru/api/shop/{store}').json()
        store_id = response.get('payload').get('id')
        return True if store_id else False
    except AttributeError:
        return False
    except Exception as e:
        logger.error(e)
        return False
