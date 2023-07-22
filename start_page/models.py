from django.db import models

class Services(models.Model):
    name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название продукта')
    price = models.PositiveIntegerField(verbose_name='Цена')
    category = models.ForeignKey(Services, on_delete=models.PROTECT)

    def __str__(self):
        return self.title


