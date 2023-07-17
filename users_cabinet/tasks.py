from datetime import timedelta
from celery import shared_task
from django.utils import timezone

from users.models import Users
from users_cabinet.models import ProductData, Stores, Reviews, SalesData

from users_cabinet.utils.token import get_token
from users_cabinet.utils.reviews import get_review
from users_cabinet.utils.parser import ProductId, ProductSKU


@shared_task
def new_token(login: str, password: str) -> str | None:
    """Новый jwt токен для отзывов"""
    token = get_token(login, password)
    user = Users.objects.get(login_ke=login)
    if token:
        user.login_valid = True
        user.token = token
    else:
        user.login_valid = False
    user.save()
    return token


@shared_task
def get_reviews(token, user_pk) -> bool:
    """Получить отзывы"""
    reviews = get_review(token)
    user = Users.objects.get(pk=user_pk)
    if reviews:
        for review in reviews:
            Reviews.objects.update_or_create(
                review_id=review['review_id'],
                defaults={
                    'store': review['store'],
                    'product': review['product'],
                    'content': review['content'],
                    'rating': review['rating'],
                    'date_create': review['date_create'],
                    'user': user,
                }
            )
        return True
    return False


@shared_task
def daily_parser():
    """Ежедневный сбор данных"""
    urls = Stores.objects.filter(status=True)
    for url in urls:
        product_ids = ProductId(url.store_url)
        sku_data = ProductSKU()
        store = Stores.objects.get(store_url=url.store_url)
        for product_id_set in product_ids.get_product_id():
            for product_id in product_id_set:
                for sku_tuple in sku_data.get_product_data(product_id):
                    sku_id, product_name, price, available, rating, params = sku_tuple[:6]
                    param1 = params[0] if params else None
                    param2 = params[1] if len(params) > 1 else None

                    ProductData.objects.create(
                        sku_id=sku_id,
                        product=product_name,
                        price=price,
                        stock_balance=available,
                        url=f'https://kazanexpress.ru/product/{product_id}',
                        rating=rating if rating else None,
                        param1=param1,
                        param2=param2,
                        user=store.user,
                        store=store
                    )

@shared_task
def update_sales_data():

    # Список с датами на 7 дней сегодняшнего дня
    date_list = [timezone.now() - timedelta(days=i) for i in range(7)]

    sku_id_list = ProductData.objects.values('sku_id').distinct()
    for sku_obj in sku_id_list:
        sku_id = sku_obj['sku_id']

        product = ProductData.objects.filter(sku_id=sku_id, datetime=timezone.now()).first()
        if product:
            current_stock_balance = product.stock_balance
            sales_data, _ = SalesData.objects.update_or_create(sku_id=product)

            for num, date in enumerate(date_list):
                product_data = ProductData.objects.filter(sku_id=sku_id, datetime=date).first()
                if product_data:
                    stock_balance = product_data.stock_balance
                    current_sales = stock_balance - current_stock_balance
                    setattr(sales_data, f'sales_{num + 1}', current_sales)
            sales_data.save()


@shared_task
def parser_manager(status: bool, store_id: int):
    """Переключение статуса магазинов для парсинга"""
    store = Stores.objects.get(id=store_id)
    if status:
        store.status = False
    else:
        store.status = True
    store.save()


@shared_task
def delete_old_data():
    """Удалить старые записи старше 7 дней"""
    data = ProductData.objects.filter(datetime__lt=timezone.now() - timezone.timedelta(days=7))
    data.delete()
