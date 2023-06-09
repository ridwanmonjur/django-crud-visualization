import traceback

from django.core.exceptions import ViewDoesNotExist
from django.shortcuts import render, redirect
import json
from django.contrib import messages
from django.core.paginator import Paginator
from decimal import Decimal

from .models import Stock

perPage = 10
pageNumber = 1


# Create your views here.
def index(request):
    _pageNumber = pageNumber
    if request.GET.get('page') is None:
        if 'page' not in request.session:
            pass
        else:
            return redirect("/?page=" + str(request.session['page']))
    else:
        _pageNumber = request.GET.get('page')
        if _pageNumber == "-1": _pageNumber = Stock.objects.count()
    request.session['page'] = _pageNumber
    request.session.modified = True
    try:
        queryset = Stock.objects.all()
        stocks_paginated = Paginator(queryset, perPage)
    except Exception as e:
        messages.error(request, repr(e))
        return redirect("/?page=1")
    page = stocks_paginated.get_page(_pageNumber)
    prev_page = 0
    if page.has_previous():
        prev_page = page.previous_page_number()
    return render(request, "trade/index.html",
                  {'stocks': page, 'prevElementCount': prev_page * perPage})


def delete(request, index_delete):
    try:
        Stock.objects.get(id=index_delete).delete()
        messages.success(request, 'Deleted the stocks')
    except Exception as e:
        messages.error(request, repr(e))
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
        try:
            stocksData = {'date': date, 'high': high, 'low': low, 'trade_code': trade_code, 'open': open,
                          'close': close, 'volume': volume}
            stock = Stock(**stocksData)
            stock.save()
        except Exception as e:
            messages.error(request, repr(e))
            return redirect("/")
        messages.success(request, 'Added the stocks')
        return redirect("/?page=-1")
    return render(request, "trade/add.html", {})


def update(request, id_update):
    try:
        stock = Stock.objects.get(id=id_update)
        if stock is None:
            raise Exception("No Data found")
    except Exception as e:
        messages.error(request, repr(e))
        return redirect("/")
    return render(request, "trade/update.html", {
        'stock': stock, 'stockIndex': id_update
    })


def do_update(request, id_update):
    try:
        if request.method == "POST":
            stock = Stock.objects.get(id=id_update)
            if stock is None:
                raise Exception("No Data found")
            stock.date = request.POST.get("date")
            stock.high = request.POST.get("high")
            stock.low = request.POST.get("low")
            stock.trade_code = request.POST.get("trade_code")
            stock.open = request.POST.get("open")
            stock.close = request.POST.get("close")
            stock.volume = request.POST.get("volume")
            stock.save()
            messages.success(request, f"Updated the stock id: {id_update}")
        else:
            raise ViewDoesNotExist("GET request not allowed!")
    except Exception as e:
        messages.error(request, repr(e))
    return redirect("/")


def seed(request):
    columns = ['volume', 'high', 'low', 'close', 'open']
    Stock.objects.all().delete()
    with open('./stock_market_data.json', 'r') as file:
        stocks = json.load(file)
        for _index, value in enumerate(stocks):
            for column in columns:
                stocks[_index][column] = Decimal(stocks[_index][column].replace(',', ''))
            stocks[_index] = Stock(**stocks[_index])
            print(stocks[_index])
    Stock.objects.bulk_create(stocks)
    return redirect("/?page=1")
