from django.http import HttpResponse
from django.shortcuts import render, redirect
import json
from django.contrib import messages
from django.core.paginator import Paginator

perPage = 10
pageNumber = 1
with open('./stock_market_data.json', 'r') as file:
    stocks = json.load(file)
stocksPaginated = Paginator(stocks, perPage)


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
    if 'page' not in request.session:
        request.session['page'] = _pageNumber
        request.session.modified = True
    page = stocksPaginated.get_page(_pageNumber)
    return render(request, "trade/index.html",
                  {'stocks': page})


def delete(request, index_delete):
    del stocks[index_delete]
    messages.success(request, 'Deleted the stocks')
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
        stocks.prepend(
            {'date': date, 'high': high, 'low': low, 'trade_code': trade_code, 'open': open,
             'close': close, 'volume': volume})
        messages.success(request, 'Added the stocks')
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
        stocks[index_update] = {'date': date, 'high': high, 'low': low, 'trade_code': trade_code, 'open': open,
                                'close': close, 'volume': volume}
        messages.success(request, 'Updated the stocks')
    return redirect("/")
