from rest_framework import serializers
from users_cabinet.models import Reviews, ProductData


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('store', 'product', 'content', 'rating', 'date_create')


class ParserSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductData
        fields = '__all__'

