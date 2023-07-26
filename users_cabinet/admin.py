from django.contrib import admin
from .models import Stores, ProductData, Reviews, SalesData

@admin.register(Stores)
class StoresAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'id', 'store_url', 'status']

@admin.register(ProductData)
class ProductDataAdmin(admin.ModelAdmin):
    list_display = ['store', 'product', 'price', 'stock_balance', 'url', 'rating', 'param1', 'param2', 'datetime']
    search_fields = ('product', 'price', 'url')

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'product', 'content', 'rating', 'date_create']

@admin.register(SalesData)
class SalesDataAdmin(admin.ModelAdmin):
    list_display = ['sku_id', 'sales_1', 'sales_2', 'sales_3', 'sales_4', 'sales_5', 'sales_6', 'sales_7']