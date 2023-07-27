from rest_framework import serializers
from users_cabinet.models import Reviews


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reviews
        fields = ('store', 'product', 'content', 'rating', 'date_create')

