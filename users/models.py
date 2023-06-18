from django.contrib.auth.models import AbstractUser
from django.db.models import ImageField, CharField

class Users(AbstractUser):
    image = ImageField(upload_to='user_pic', blank=True)
    login_ke = CharField(max_length=50, blank=True)
    pass_ke = CharField(max_length=50, blank=True)
