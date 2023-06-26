from celery import shared_task
from .utils.token import get_token
from users.models import Users


@shared_task
def new_token(login, password) -> bool:
    token = get_token(login, password)
    if token:
        user = Users.objects.get(login_ke=login)
        user.token = token
        user.save()
        return True
    return False
