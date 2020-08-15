from django.db import models

# Create your models here.

class Symbol(models.Model):
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['symbol'], name='unique_symbol')
        ]

        indexes = [
            models.Index(fields=['symbol']),
        ]
    
    symbol = models.CharField(max_length=5, blank=True, primary_key=True)

class DailyStock(models.Model):

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['symbol', 'date'], name='unique__symbol_date'),    
        ]

        indexes = [
            models.Index(fields=['symbol', 'date']),
        ]

    symbol = models.ForeignKey(Symbol, on_delete=models.CASCADE, null=False, related_name='daily_stock', db_column='symbol')
    date = models.DateField(blank=True, null=True)
    close_last = models.FloatField(blank=True, null=True)
    volume = models.FloatField(blank=True, null=True)
    open_price = models.FloatField(blank=True, null=True)
    high = models.FloatField(blank=True, null=True)
    low = models.FloatField(blank=True, null=True)

    def __str__(self):
        return '<DailyStock: symbol: {}, date: {}, high: {}, low: {}, open: {}>'.format(
            self.symbol,self.date, self.high, self.low, self.open)