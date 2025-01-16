from rest_framework import serializers
from tovari.models import Products

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Products
        fields = ['id', 'name', 'slug', 'sell_price', 'quantity', 'description', 'image', 'category']
