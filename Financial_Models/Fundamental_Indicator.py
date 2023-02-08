import requests
import os
import dotenv
import pandas as pd
import json
import csv


class Fundamental_Indicators:
    def __init__(self, ticker: str) -> None:
        try:
            self._ticker = ticker
            dotenv.load_dotenv()
            self._api_key = os.environ["ALPHA_VANTAGE_API_KEY"]
            self._company_info = self.get_company_info()
        except Exception as e:
            print("Error: ", e)
            return None

    def __str__(self) -> str:
        return f"SecurityDataHandler({self.ticker} {self.api_key})"

    def __repr__(self) -> str:
        return f"SecurityDataHandler({self.ticker}, {self.api_key})"

    @property
    def ticker(self) -> str:
        return self._ticker

    @ticker.setter
    def ticker(self, ticker: str) -> None:
        self._ticker = ticker

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str) -> None:
        self._api_key = api_key

    @property
    def company_info(self) -> dict:
        return self._company_info
    
    @company_info.setter
    def company_info(self, company_info: dict) -> None:
        self._company_info = company_info

    def get_data(self, interval: str = "1min", outputsize: str = "compact") -> pd.DataFrame:
        url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={self.ticker}&interval={interval}&apikey={self._api_key}&outputsize={outputsize}'
        response = requests.get(url)
        data = response.json()
        data = data["Time Series (1min)"]
        data = pd.DataFrame(data).T
        data.index = pd.to_datetime(data.index)
        data = data.astype(float)
        return data

    def get_company_info(self, parameter: str = None, function: str = "OVERVIEW") -> str:
        url = f'https://www.alphavantage.co/query?function={function}&symbol={self.ticker}&apikey={self._api_key}'
        response = requests.get(url)
        data = response.json()
        if parameter is None:
            return data
        return data[parameter]

    def get_full_name(self) -> str:
        return self._company_info["Name"]

    def get_description(self) -> str:
        return self._company_info["Description"]

    def get_exchange(self) -> str:
        return self._company_info["Exchange"]

    def get_country(self) -> str:
        return self._company_info["Country"]

    def get_sector(self) -> str:
        return self._company_info["Sector"]

    def get_industry(self) -> str:
        return self._company_info["Industry"]

    def get_market_cap(self) -> str:
        return self._company_info["MarketCapitalization"]

    def get_ebitda(self) -> str:
        return self._company_info["EBITDA"]

    def get_pe_ratio(self) -> str:
        return self._company_info["PERatio"]

    def get_eps(self) -> str:
        return self._company_info["EPS"]

    def get_peg_ratio(self) -> str:
        return self._company_info["PEGRatio"]

    def get_book_value(self) -> str:
        return self._company_info["BookValue"]

    def get_dividend_per_share(self) -> str:
        return self._company_info["DividendPerShare"]

    def get_dividend_yield(self) -> str:
        return self._company_info["DividendYield"]

    def geT_profit_margin(self) -> str:
        return self._company_info["ProfitMargin"]

    def get_operating_margin(self) -> str:
        return self._company_info["OperatingMarginTTM"]

    def get_return_on_assets(self) -> str:
        return self._company_info["ReturnOnAssetsTTM"]

    def get_return_on_equity(self) -> str:
        return self._company_info["ReturnOnEquityTTM"]

    def get_revenue(self) -> str:
        return self._company_info["RevenueTTM"]

    def get_gross_profit(self) -> str:
        return self._company_info["GrossProfitTTM"]

    def get_quarterly_earning_growth(self) -> str:
        return self._company_info["QuarterlyEarningsGrowthYOY"]

    def get_quarterly_revenue_growth(self) -> str:
        return self._company_info["QuarterlyRevenueGrowthYOY"]

    def get_analyst_target_price(self) -> str:
        return self._company_info["AnalystTargetPrice"]

    def get_trailing_pe(self) -> str:
        return self._company_info["TrailingPE"]

    def get_forward_pe(self) -> str:
        return self._company_info["ForwardPE"]

    def get_price_to_sales_ratio(self) -> str:
        return self._company_info["PriceToSalesRatioTTM"]

    def get_price_to_book_ratio(self) -> str:
        return self._company_info["PriceToBookRatio"]

    def get_beta(self) -> str:
        return self._company_info["Beta"]

    def get_52_week_high(self) -> str:
        return self._company_info["52WeekHigh"]

    def get_52_week_low(self) -> str:
        return  self._company_info["52WeekLow"]

    def get_50_day_moving_average(self) -> str:
        return self.get_company_info(parameter="50DayMovingAverage")

    def get_200_day_moving_average(self) -> str:
        return self.get_company_info(parameter="200DayMovingAverage")

    def get_share_outstanding(self) -> str:
        return self.get_company_info(parameter="SharesOutstanding")

    def get_dividend_date(self) -> str:
        return self.get_company_info(parameter="DividendDate")

    def get_ex_dividend_date(self) -> str:
        return self.get_company_info(parameter="ExDividendDate")

    def get_income_statement(self):
        return self.get_company_info(function="INCOME_STATEMENT")

    def get_balance_sheet(self):
        return self.get_company_info(function="BALANCE_SHEET")

    def get_cash_flow(self):
        return self.get_company_info(function="CASH_FLOW")

    def get_earnings(self):
        """
            Get the earnings for a company.
            - returns:
                - dict: The earnings for the company.
        """
        return self.get_company_info(function="EARNINGS")

    def get_earnings_calendar(self, horizon: str = "3month") -> dict | None:
        """
            Get the earnings calendar for a company for a given horizon. 
            - params: 
                - horizon (str): The horizon for which to get the earnings calendar. 
                    - 3month: 3 months
                    - 6month: 6 months
                    - 12month: 12 months
            - returns: 
                - dict: The earnings calendar for the company.
        """
        url = f'https://www.alphavantage.co/query?function=EARNINGS_CALENDAR&symbol={self.ticker}&horizon={horizon}&apikey={self.api_key}'
        with requests.Session() as s:
            download = s.get(url)
            decoded_content = download.content.decode('utf-8')
            cr = csv.reader(decoded_content.splitlines(), delimiter=',')
            my_list = list(cr)
            if len(my_list) > 1:
                return my_list
        return None

    def convert_to_dataframe(self, data: dict) -> pd.DataFrame:
        """
            Convert a dictionary to a pandas dataframe.
            - params:
                - data (dict): The data to convert.
            - returns:
                - pd.DataFrame: The converted data.
        """
        return pd.DataFrame(data)

    def download_historical_data(self, outputsize: str = "full", datatype: str = "pd.DataFrame") -> pd.DataFrame | None:
        """
            Download the historical data for a company.
            - params:
                - outputsize (str): The size of the data to download. 
                    - full: Full data
                    - compact: Compact data
                - datatype (str): The datatype to return. 
                    - pd.DataFrame: pandas dataframe
                    - dict: dictionary
            - returns:
                - pd.DataFrame: The downloaded data.
        """
        url = f"https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={self.ticker}&interval=1min&apikey={self.api_key}&outputsize={outputsize}"
        r = requests.get(url)
        data = r.json()
        if datatype == "pd.DataFrame":
            return pd.DataFrame(data["Time Series (1min)"]).T
        

    def convert_timeframe(self,file_name: str, data: pd.DataFrame, timeframe: str = "1min") -> pd.DataFrame:
        """
            Convert the timeframe of the data.
            - params:
                - data (pd.DataFrame): The data to convert.
                - timeframe (str): The timeframe to convert to.
                    - 1min: 1 minute
                    - 5min: 5 minutes
                    - 15min: 15 minutes
                    - 30min: 30 minutes
                    - 60min: 60 minutes
                    - 2h: 120 minutes
                    - 4h: 240 minutes
                    - 1d: Daily 1440 minutes
                    - 1w: Weekly 7200 minutes
                    - 1m: Monthly 40320 minutes
            - returns:
                - pd.DataFrame: The converted data.
        """
        new_timeframe=  0
        if timeframe == "5min":
            new_timeframe = 5
        if timeframe == "15min":
            new_timeframe = 15
        if timeframe == "30min":
            new_timeframe = 30
        if timeframe == "60min":
            new_timeframe = 60
        if timeframe == "2h":
            new_timeframe = 120
        if timeframe == "4h":
            new_timeframe = 240
        if timeframe == "1d":
            new_timeframe = 1440
        if timeframe == "1w":
            new_timeframe = 1440 * 5
        if timeframe == "1m":
            new_timeframe = 1440 * 28
        
        return data.resample(new_timeframe).agg(
            {
                "open": "first",
                "high": "max",
                "low": "min",
                "close": "last",
                "volume": "sum",
            }
        ).to_excel(file_name)
