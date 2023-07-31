from django.db import models

from users.models import User


class ProductData(models.Model):
    sku_id = models.PositiveIntegerField()
    product = models.CharField(max_length=200)
    price = models.PositiveIntegerField(default=0)
    stock_balance = models.PositiveIntegerField(null=True)
    url = models.CharField(max_length=100)
    rating = models.FloatField(null=True)
    param1 = models.CharField(max_length=50, null=True, blank=True)
    param2 = models.CharField(max_length=50, null=True, blank=True)
    datetime = models.DateField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    store = models.ForeignKey('Stores', on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'SKU'
        verbose_name_plural = 'Все SKU'

    def __str__(self):
        return str(self.product)


class SalesData(models.Model):
    sku_id = models.ForeignKey(ProductData, on_delete=models.CASCADE)
    sales_1 = models.PositiveSmallIntegerField(null=True)
    sales_2 = models.PositiveSmallIntegerField(null=True)
    sales_3 = models.PositiveSmallIntegerField(null=True)
    sales_4 = models.PositiveSmallIntegerField(null=True)
    sales_5 = models.PositiveSmallIntegerField(null=True)
    sales_6 = models.PositiveSmallIntegerField(null=True)
    sales_7 = models.PositiveSmallIntegerField(null=True)

    class Meta:
        verbose_name = 'продажи'
        verbose_name_plural = 'Продажи'

    def __str__(self):
        return str(self.sku_id)

class Stores(models.Model):
    store_name = models.CharField(max_length=50)
    store_url = models.CharField(max_length=100)
    status = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = 'Все магазины'

    def __str__(self):
        return str(self.store_name)


class Reviews(models.Model):
    store = models.CharField(max_length=50)
    product = models.CharField(max_length=200)
    content = models.TextField(null=True)
    rating = models.PositiveSmallIntegerField(null=True)
    review_id = models.PositiveIntegerField()
    date_create = models.DateField()
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return str(self.product)
