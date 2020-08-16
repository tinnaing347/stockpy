from django.core.management.base import BaseCommand
from django.conf import settings 

import sys
import os

from stocks import models
import pandas as pd
from typing import Dict, List
from numpy import dtype

DATA_DIR = os.path.join(settings.BASE_DIR, 'data')

class DailyStocksError(Exception):
    """ Thrown if an agency fixture does not have data associated with it"""

class Command(BaseCommand):
    """read {symbol}.csv files downloaded from https://www.nasdaq.com/market-activity/funds-and-etfs/{symbol}/historical
        and placed in data directory and write to Symbol model and DailyStock model."""

    def _get_file_ls(self, symbols: str=None):
        f = []
        for filenames in os.listdir(DATA_DIR):
            if filenames == '.gitkeep':
                continue
            symbol = filenames.split('.')[0]
            if symbols:
                if symbol in symbols:
                    f.append({symbol: os.path.join(DATA_DIR, filenames)})
                continue
            f.append({symbol: os.path.join(DATA_DIR, filenames)})
        return f
    
    def _get_and_prepare_data(self, file_: Dict):
        symbol = list(file_.keys())[0]
        df = pd.read_csv(file_[symbol])

        #need to remove space from columns names and rename them
        df.rename(columns={'Date': 'date', ' Close/Last': 'close_last', ' Volume': 'volume',
                            ' High': 'high', ' Low': 'low', ' Open': 'open_price'}, inplace=True)
        df['date'] = pd.to_datetime(df['date'])
        str_cols = self._return_str_dtypes(df.dtypes.to_dict()) #only a few columns but i will rather not use apply if not necessary; so many rows....let's blame nasdaq developers for not being consistent i suppose
        #convert string price into float
        for i in str_cols:
            df[i] = df[i].apply(lambda x: float(x.split('$')[-1])) #this will work for now
        return symbol.upper(), df.to_dict(orient='records')
    
    def _return_str_dtypes(self, dtype_dict: Dict):
        str_cols = []
        for k,v in dtype_dict.items():
            if v == dtype('O'):
                str_cols.append(k)
        return str_cols

    def _get_or_create_symbol(self, symbol: str):
        symbol_query = models.Symbol.objects.filter(symbol=symbol)
        if symbol_query:
            self.stdout.write(self.style.SUCCESS('Found symbol: {}'.format(symbol)))
            return symbol_query[0]
        symbol = models.Symbol(symbol=symbol)
        symbol.save()
        self.stdout.write(self.style.SUCCESS('Created symbol: {}'.format(symbol.symbol)))
        return symbol

    def _make_stock_model(self, symbol_obj, data: List):
        for rec in data:
            try:
                models.DailyStock.objects.update_or_create(symbol=symbol_obj, **rec)
                rep = 'Added daily stock data for symbol: {}, date: {}'.format(symbol_obj.symbol, rec['date'])
                self.stdout.write(self.style.SUCCESS(rep))
            except DailyStocksError as err:
                self.stdout.write(self.style.FAILURE(str(err)))

    
    def add_arguments(self, parser):
        parser.add_argument('--symbols', 
            action='store', 
            type=str, 
            const=None, 
            help='Comma seperated string of symbols (i.e MSFT,SPY). If none are supplied, will run fixtures for all symbols found in data dir.', 
        )

    def handle(self, *args, **options):
        file_ls = self._get_file_ls(options['symbols'])
        for file_ in file_ls:
            symbol, data = self._get_and_prepare_data(file_)
            symbol_obj = self._get_or_create_symbol(symbol)
            self._make_stock_model(symbol_obj, data)