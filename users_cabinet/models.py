from django.db import models

from users.models import Users


class ProductData(models.Model):
    store_name = models.CharField(max_length=50, null=True)
    product = models.CharField(max_length=200, null=True)
    price = models.PositiveIntegerField(default=0)
    sold = models.PositiveIntegerField(default=0)
    stock_balance = models.PositiveIntegerField(null=True)
    url = models.CharField(max_length=100)
    rating = models.FloatField(null=True)
    param1 = models.CharField(max_length=50, null=True)
    param2 = models.CharField(max_length=50, null=True)
    datetime = models.DateField(auto_now_add=True)
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    store = models.ForeignKey('Stores', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'данные'
        verbose_name_plural = 'Детализация по продажам'

    def __str__(self):
        return str(self.store)

class Stores(models.Model):
    store_url = models.CharField(max_length=100, null=True, blank=True)
    action = models.CharField(max_length=5, default='play')
    users = models.ManyToManyField(Users, through='ProductData', related_name='stores')

    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = 'Все магазины'

    def __str__(self):
        return self.store_url


class Reviews(models.Model):
    store = models.CharField(max_length=50)
    product = models.CharField(max_length=200)
    content = models.TextField(blank=True, null=True)
    rating = models.PositiveSmallIntegerField(null=True)
    review_id = models.PositiveIntegerField(null=True)
    date_create = models.DateField(null=True)
    user = models.ForeignKey(to=Users, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.product
