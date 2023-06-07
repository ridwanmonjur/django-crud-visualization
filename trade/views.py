from django.http import HttpResponse
from django.shortcuts import render
import json

with open('./stock_market_data.json', 'r') as file:
    trades = json.load(file)


# Create your views here.
def index(request):
    return render(request, "trade/index.html", {'trades': trades})
