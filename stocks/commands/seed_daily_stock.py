from django.core.management.base import BaseCommand
from django.conf import settings 

import sys
import os

from stocks import models
import pandas as pd

DATA_DIR = os.path.join(settings.BASE_DIR, 'data')

class Command(BaseCommand):

    def _get_files(self):
        pass
    
    def _prepare_data(self, df):
        return df.to_dict(orient=records)

    def _make_model(self, data):
        symbol = models.Symbol.objects.get(bdbid=data.pop('symbol'))
        models.DailyStock.objects.update_or_create(
                        symbol=symbol, **data
                        )
        rep = 'Added symbol: {}, date: {}'.format(symbol.symbol, data['date'])
        self.stdout.write(self.style.SUCCESS(rep))

    def handle(self, *args, **options):
        file_ls = self._get_files():
