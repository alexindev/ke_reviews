from django.contrib import admin
from .models import Stores, ProductData, Reviews

@admin.register(Stores)
class StoresAdmin(admin.ModelAdmin):
    list_display = ['store_url']

@admin.register(ProductData)
class UserStoresAdmin(admin.ModelAdmin):
    list_display = ['store', 'product', 'price', 'stock_balance', 'url', 'rating', 'datetime']

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'product', 'content', 'rating', 'date_create']

