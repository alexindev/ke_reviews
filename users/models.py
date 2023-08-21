from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, CharField, BooleanField


class User(AbstractUser):
    image = ImageField(upload_to='user_pic', default='default.png')
    login_ke = CharField(max_length=50, null=True, blank=True)
    pass_ke = CharField(max_length=50, null=True, blank=True)
    token = CharField(max_length=100, null=True, blank=True)
    token_valid = BooleanField(default=True)
    login_valid = BooleanField(default=True)

