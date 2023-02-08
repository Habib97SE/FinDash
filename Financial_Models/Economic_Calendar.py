import requests
import pandas as pd
import os
import dotenv
import json


class Economic_Calendar:
    def __init__(self) -> None:
        try:
            dotenv.load_dotenv()
            self._api_key = os.environ["ALPHA_VANTAGE_API_KEY"]
            self.BASE_URL = "https://www.alphavantage.co/query?"
            self.functions = {
                "Real GDP": "REAL_GDP",
                "Real GDP per capita": "REAL_GDP_PER_CAPITA",
                "Consumer Price Index": "CPI",
                "Retail Sales": "RETAIL_SALES",
                "Unemployment Rate": "UNEMPLOYMENT",
                "Nonfarm Payroll": "NONFARM_PAYROLL"
            }
        except Exception as e:
            print("Error: ", e)
            return None

    def __str__(self) -> str:
        return f"api_key: {self._api_key}"

    def __repr__(self) -> str:
        return f"Economic_Calendar(api_key={self._api_key})"

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str) -> None:
        self._api_key = api_key

    @property
    def functions(self) -> dict:
        return self._functions

    @functions.setter
    def functions(self, functions: dict) -> None:
        self._functions = functions

    def filter_period(self, data: pd.DataFrame, from_period: str, to_period: str, output_format: str) -> dict | pd.DataFrame | None:
        """
            This method will filter out the data for given period and reutrn the data.
            - params:
                - data (pd.DataFrame): The data to filter.
                - from_period (str): The start date.
                - to_period (str): The end date.
                - output_format (str): The output format for the data.
                    - dataframe: dataframe
                    - dict: dict
            - returns:
                - dict | pd.DataFrame: The filtered data.
        """
        if output_format == "dataframe":
            return data.loc[(data["date"] >= from_period) & (data["date"] <= to_period)]
        elif output_format == "dict":
            return data.loc[(data["date"] >= from_period) & (data["date"] <= to_period)].to_dict()
        else:
            return None

    def get_real_gdp(self, interval="annual") -> dict | None:
        """
            Get the real GDP for a given interval. 
            - params: 
                - interval (str): The interval for which to get the real GDP. 
                    - annual: annual
                    - quarterly: quarterly
            - returns: 
                - dict: The real GDP for the given interval.
        """
        url = f'{self.BASE_URL}function={self.functions["Real GDP"]}&interval={interval}&apikey={self.api_key}'
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None

    def get_gdp_per_capita(self):
        url = f'{self.BASE_URL}function={self._functions["Real GDP per capita"]}A&apikey={self.api_key}'
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None

    def get_cpi(self, interval: str = "monthly") -> dict | None:
        """
            Get the consumer price index for a given interval. 
            - params: 
                - interval (str): The interval for which to get the consumer price index. 
                    - monthly: monthly
                    - semiannual: semiannual
            - returns: 
                - dict: The consumer price index for the given interval.
        """
        url = f'{self.BASE_URL}function={self._functions["Consumer Price Index"]}&interval={interval}&apikey={self.api_key}'
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None

    def get_retail_sales(self) -> dict:
        """
            Get the retail sales.
            - returns:
                - dict: The retail sales.
        """
        url = f'{self.BASE_URL}function={self._functions["Retail Sales"]}&apikey={self.api_key}'
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None

    def get_unemployment_rate(self) -> dict | None:
        """
            Get the unemployment rate.
            - returns:
                - dict: The unemployment rate.
        """
        url = f"{self.BASE_URL}function={self._functions['Unemployment Rate']}&apikey={self.api_key}"
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None

    def get_nonfarm_payroll(self) -> dict | None:
        url = f"{self.BASE_URL}function={self._functions['Nonfarm Payroll']}&apikey={self.api_key}"
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None
