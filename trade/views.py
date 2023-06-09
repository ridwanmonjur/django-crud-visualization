import traceback

from django.core.exceptions import ViewDoesNotExist, ValidationError
from django.db.models import Count
from django.shortcuts import render, redirect
import json
from django.contrib import messages
from django.core.paginator import Paginator
from decimal import Decimal
from django.http import JsonResponse
from django.shortcuts import render
from .models import Stock
from .serializers import StockSerializer

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
        queryset = Stock.objects.get_queryset().order_by('id')
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
        try:
            serializer = StockSerializer(data=request.POST)
            if serializer.is_valid():
                serializer.save()
            else:
                raise ValidationError(serializer.errors, code="invalid")
        except Exception as e:
            messages.error(request, repr(e))
            return redirect("/")
        messages.success(request, 'Added the stocks' + repr(serializer.data))
        return redirect("/?page=-1")
    return render(request, "trade/add.html", {})


def update(request, id_update):
    try:
        stock = Stock.objects.get(id=id_update)
        return render(request, "trade/update.html", {
            'stock': stock, 'stockIndex': id_update
        })
    except Exception as e:
        messages.error(request, repr(e))
        return redirect("/")


def get_chart_page(request):
    try:
        trade_codes_number = Stock.objects.values('trade_code').annotate(Count('id')).order_by()
        return render(request, "trade/chart.html", {'trade_codes_number': trade_codes_number})
    except Exception as e:
        messages.error(request, repr(e))
        return redirect("/")


def get_chart(request):
    try:
        code = 'APOLOISPAT'
        if request.GET.get('code') is not None:
            code = request.GET.get('code')
        stocks = Stock.objects.filter(trade_code=code).order_by('date')
        close = []
        date = []
        volume = []
        for stock in stocks:
            close.append(stock.close)
            date.append(stock.date)
            volume.append(stock.volume)
        return JsonResponse({'close': close, 'date': date, 'volume': volume})
    except Exception as e:
        messages.error(request, repr(e))
        return redirect("/")


def do_update(request, id_update):
    try:
        if request.method == "POST":
            stock = Stock.objects.get(id=id_update)
            serializer = StockSerializer(data=request.POST)
            if serializer.is_valid():
                stock = Stock(**serializer.data, id=stock.id)
                stock.save()
            else:
                raise ValidationError(serializer.errors, code="invalid")
            messages.success(request, f"Updated the stock id: " + str(stock.id))
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
    Stock.objects.bulk_create(stocks)
    return redirect("/?page=1")
