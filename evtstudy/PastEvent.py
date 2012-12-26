import numpy as np
import pandas as pd
from datetime import datetime

from finance.utils import DateUtils
from finance.utils import DataAccess
from finance.evtstudy.SimpleEvent import SimpleEvent

class PastEvent(SimpleEvent):

    def __init__(self, path='./data'):
        # Utils
        self.da = DataAccess(path)

        # Variables
        self.date = None # Date of the event
        self.symbol = None
        self.field = 'Adj Close'
        self.lookback_days = 20
        self.lookforward_days = 20
        self.estimation_period = 255
        self.market = "SPY"

        # Results
        self.evt_window_data = None
        self.er = None
        self.ar = None
        self.car = None
        self.t_test = None
        self.prob = None


    def run(self):
        dates = DateUtils.nyse_dates_event(self.date,
                            self.lookback_days + self.estimation_period,
                            self.lookforward_days, list=True)
        start_date = dates[0]
        end_date = dates[-1]

        # Data to the General market_return Study
        self.data = self.da.get_data(self.symbol, start_date, end_date, self.field)
        evt_window_dates = dates[- self.lookforward_days - self.lookback_days - 1:]
        self.evt_window_data = self.data[evt_window_dates[0]:dates[-1]]
        self.market = self.da.get_data(self.market, start_date, end_date, self.field)
        # Parameters of the General market_return Study
        self.start_period = dates[0]
        self.end_period = dates[self.estimation_period]
        self.start_window = dates[self.estimation_period]
        self.end_window = dates[-1]

        # Run the Market Return method
        super().market_return()

if __name__ == "__main__":
    pevt = PastEvent('./data')
    pevt.symbol = 'AAPL'
    pevt.market = "^gspc"
    pevt.lookback_days = 10
    pevt.lookforward_days = 10
    pevt.estimation_period = 252
    pevt.date = datetime(2009, 1, 5)
    pevt.run()
    print(pevt.er)