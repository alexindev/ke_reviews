from django.contrib import admin
from .models import Stores, ProductData, Reviews

@admin.register(Stores)
class StoresAdmin(admin.ModelAdmin):
    list_display = ['store_name', 'store_url', 'action']

@admin.register(ProductData)
class ProductDataAdmin(admin.ModelAdmin):
    list_display = ['store', 'product', 'price', 'stock_balance', 'url', 'rating', 'param1', 'param2', 'datetime']

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'product', 'content', 'rating', 'date_create']

