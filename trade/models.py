from django.db import models
from django.db.models import AutoField


# Create your models here.
class Stock(models.Model):
    objects = models.Manager()
    id = AutoField(primary_key=True)
    date = models.DateField()
    trade_code = models.CharField(max_length=30)
    high = models.DecimalField(max_digits=15, decimal_places=2)
    low = models.DecimalField(max_digits=15, decimal_places=2)
    open = models.DecimalField(max_digits=15, decimal_places=2)
    close = models.DecimalField(max_digits=15, decimal_places=2)
    volume = models.DecimalField(max_digits=15, decimal_places=2)
