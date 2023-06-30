from django.contrib import admin
from .models import Stores, UserStores, Reviews

@admin.register(Stores)
class StoresAdmin(admin.ModelAdmin):
    list_display = ['store_url']

@admin.register(UserStores)
class UserStoresAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'product', ]

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ['user', 'store', 'product', 'content', 'rating', 'date_create']

