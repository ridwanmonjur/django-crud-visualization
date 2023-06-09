from _decimal import Decimal

from django.core.management.base import BaseCommand
import json

from trade.models import Stock


class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        columns = ['volume', 'high', 'low', 'close', 'open']
        Stock.objects.all().delete()
        with open('./stock_market_data.json', 'r') as file:
            stocks = json.load(file)
            for _index, value in enumerate(stocks):
                for column in columns:
                    stocks[_index][column] = Decimal(stocks[_index][column].replace(',', ''))
                stocks[_index] = Stock(**stocks[_index])
        Stock.objects.bulk_create(stocks)
        self.stdout.write('done.')
