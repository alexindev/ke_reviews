from django.db import models
from django.db.models import CharField, PositiveIntegerField, FloatField, DateField, ForeignKey, TextField, SmallIntegerField

from users.models import Users

class UserStores(models.Model):
    store = CharField(max_length=50)
    product = CharField(max_length=200)
    price = PositiveIntegerField()
    sale_count = PositiveIntegerField(default=0)
    stock_balance = PositiveIntegerField(default=0)
    url = CharField(max_length=100)
    rating = FloatField(default=0)
    param1 = CharField(max_length=50, blank=True)
    param2 = CharField(max_length=50, blank=True)
    datetime = DateField(auto_now_add=True)
    user = ForeignKey(to=Users, on_delete=models.CASCADE)


class Reviews(models.Model):
    store = CharField(max_length=50)
    product = CharField(max_length=200)
    review = TextField(blank=True)
    stars = SmallIntegerField()
    url = CharField(max_length=100)
    user = ForeignKey(to=Users, on_delete=models.CASCADE)

