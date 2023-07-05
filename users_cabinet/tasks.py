from celery import shared_task
from .utils.token import get_token
from .utils.reviews import get_reviews
from users.models import Users
from users_cabinet.models import Reviews


@shared_task
def new_token(login: str, password: str) -> str | None:
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
def review_manager(token, user_pk) -> bool:
    reviews = get_reviews(token)
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
def parser_manager(action: str, store_id: str, token: str):
    if action == 'play':
        ...
    else:
        ...
