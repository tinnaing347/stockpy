#stockpy
REST API for NASDAQ.
Bare minimum three tables for now.
- Symbol
- RealTimeStock
- DailyStock 

To populate RealTimeStock, `finnhub-python` is used. [Link](https://github.com/Finnhub-Stock-API/finnhub-python). Timescale hasn't been determined yet. Probably should automate this.
To populate DailyStock, data downloaded directly from historical data from [NASDAQ](https://www.nasdaq.com/) is used.
Data are placed in `data` folder at root directory and saved as `{symbol}.csv`.