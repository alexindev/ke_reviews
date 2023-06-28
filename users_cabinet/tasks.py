from celery import shared_task
from .utils.token import get_token
from users.models import Users


@shared_task
def new_token(login, password) -> str | None:
    token = get_token(login, password)
    user = Users.objects.get(login_ke=login)
    if token:
        user.login_valid = True
        user.token = token
    else:
        user.login_valid = False
    user.save()
    return token
