from rest_framework import serializers

from trade.models import Stock


class StockSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stock
        exclude = ('id',)
