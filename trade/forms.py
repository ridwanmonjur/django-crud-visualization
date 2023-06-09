from django import forms


class StockForm(forms.Form):
    date = forms.DateField()
    trade_code = forms.CharField(max_length=30)
    high = forms.DecimalField(max_digits=15, decimal_places=2)
    low = forms.DecimalField(max_digits=15, decimal_places=2)
    open = forms.DecimalField(max_digits=15, decimal_places=2)
    close = forms.DecimalField(max_digits=15, decimal_places=2)
    volume = forms.DecimalField(max_digits=15, decimal_places=2)
