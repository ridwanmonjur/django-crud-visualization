from django.http import HttpResponse
from django.shortcuts import render, redirect
import json

with open('./stock_market_data.json', 'r') as file:
    stocks = json.load(file)
stocksPaginated = stocks[0:20]


# Create your views here.
def index(request):
    print(stocksPaginated[0])
    return render(request, "trade/index.html", {'stocks': stocksPaginated})


def delete(request, index_delete):
    del stocksPaginated[index_delete]
    return redirect("/")


def add(request):
    if request.method == "POST":
        date = request.POST.get("date")
        high = request.POST.get("high")
        low = request.POST.get("low")
        trade_code = request.POST.get("trade_code")
        open = request.POST.get("open")
        close = request.POST.get("close")
        volume = request.POST.get("volume")
        stocksPaginated.append(
            {'date': date, 'high': high, 'low': low, 'trade_code': trade_code, 'open': open,
             'close': close, 'volume': volume})
        # stocks.append({'date': date, 'high': high, 'low': low, 'trade_code': trade_code, 'open': open,
        #                                          'close': close, 'volume': volume})
        return redirect("/")
    return render(request, "trade/add.html", {})


def update(request, index_update):
    stock = stocks[index_update]
    return render(request, "trade/update.html", {
        'stock': stock, 'stockIndex': index_update
    })


def do_update(request, index_update):
    if request.method == "POST":
        date = request.POST.get("date")
        high = request.POST.get("high")
        low = request.POST.get("low")
        trade_code = request.POST.get("trade_code")
        open = request.POST.get("open")
        close = request.POST.get("close")
        volume = request.POST.get("volume")
        stocksPaginated[index_update] = {'date': date, 'high': high, 'low': low, 'trade_code': trade_code, 'open': open,
                                         'close': close, 'volume': volume}
        print(stocksPaginated[index_update])
        stocks[index_update] = {'date': date, 'high': high, 'low': low, 'trade_code': trade_code, 'open': open,
                                'close': close, 'volume': volume}
    return redirect("/")
