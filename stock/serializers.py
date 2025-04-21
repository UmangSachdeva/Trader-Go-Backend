from rest_framework import serializers
from .models import Wishlist
from .utils.stock_trader import get_ticker_details
from .api_exception import ValidationError


class WishlistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'
        extra_kwargs = {
            'company_name': {'required': False},
            'current_price': {'required': False},
            'user': {'required': False},
            'price_wishlisted': {'required': False},
            'icon': {'required': False}
        }

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        return ret

    def validate(self, validated_data):
        request = self.context.get('request')

        return validated_data

    def create(self, validated_data):

        request = self.context.get('request')

        stock_info = get_ticker_details(
            {'GET': {"symbol": request.data.get("symbol")}})

        user = request.user

        validated_data['user'] = user
        validated_data['current_price'] = stock_info.get('current_price')
        validated_data['company_name'] = stock_info.get('name')
        validated_data['price_wishlisted'] = stock_info.get('current_price')
        validated_data['symbol'] = request.data.get("symbol")

        wishlist = Wishlist.objects.create(
            **validated_data
        )

        wishlist.save()

        return wishlist
