import os
import dotenv
import requests


class Technical_Indicators:
    def __init__(self) -> None:
        try:
            dotenv.load_dotenv()
            self._api_key = os.getenv("ALPHA_VANTAGE_API_KEY")
        except Exception as e:
            print(e)
            return None

    @property
    def api_key(self) -> str:
        return self._api_key

    @api_key.setter
    def api_key(self, api_key: str) -> None:
        self._api_key = api_key

    def __str__(self) -> str:
        return f"api_key: {self._api_key}"

    def __repr__(self) -> str:
        return f"Technical_Indicators(api_key={self._api_key})"

    def get_moving_average(self, ticker: str, moving_average_type: str = "SMA", interval: str = "1min", time_period: int = 10, series_type: str = "close") -> dict | None:
        """
            Learn more about different moving averages at: https://www.investopedia.com/terms/m/movingaverage.asp
            Get the moving average for a given interval.
            - params:
                - ticker (str): The ticker for which to get the moving average.
                - moving_average_type (str): The moving average type for which to get the moving average.
                    - SMA: simple moving average
                    - EMA: exponential moving average
                    - WMA: weighted moving average
                    - DEMA: double exponential moving average
                    - TEMA: triple exponential moving average
                    - TRIMA: triangular moving average
                    - KAMA: Kaufman adaptive moving average
                    - MAMA: MESA adaptive moving average
                    - T3: triple exponential moving average (T3)
                - interval (str): The interval for which to get the moving average.
                    - daily: daily
                    - weekly: weekly
                    - monthly: monthly
                - time_period (int): The time period for which to get the moving average.
                - series_type (str): The series type for which to get the moving average.
                    - open: open
                    - high: high
                    - low: low
                    - close: close
            - returns:
                - dict: The moving average for the given interval.
        """
        url = f"https://www.alphavantage.co/query?function={moving_average_type}&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}"
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None

    def get_macd(self, ticker: str, interval: str = "1min", series_type: str = "close") -> dict | None:
        """
            Learn more about MACD at: https://www.investopedia.com/terms/m/macd.asp
            Get the moving average convergence divergence (MACD) for a given interval.
            - params:
                - ticker (str): The ticker for which to get the moving average convergence divergence (MACD).
                - interval (str): The interval for which to get the moving average convergence divergence (MACD).
                    - daily: daily
                    - weekly: weekly
                    - monthly: monthly
                - series_type (str): The series type for which to get the moving average convergence divergence (MACD).
                    - open: open
                    - high: high
                    - low: low
                    - close: close
            - returns:
                - dict: The moving average convergence divergence (MACD) for the given interval.
        """
        url = f"https://www.alphavantage.co/query?function=MACD&symbol={ticker}&interval={interval}&series_type={series_type}&apikey={self.api_key}"
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None

    def get_stoch(self, ticker: str, interval: str = "1min", series_type: str = "close") -> dict | None:
        """
            Learn more about stochastic oscillator at: https://www.investopedia.com/terms/s/stochasticoscillator.asp
            Get the stochastic oscillator for a given interval.
            - params:
                - ticker (str): The ticker for which to get the stochastic oscillator.
                - interval (str): The interval for which to get the stochastic oscillator.
                    - daily: daily
                    - weekly: weekly
                    - monthly: monthly
                - series_type (str): The series type for which to get the stochastic oscillator.
                    - open: open
                    - high: high
                    - low: low
                    - close: close
            - returns:
                - dict: The stochastic oscillator for the given interval.
        """
        url = f"https://www.alphavantage.co/query?function=STOCH&symbol={ticker}&interval={interval}&series_type={series_type}&apikey={self.api_key}"
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None

    def get_rsi(self, ticker: str, interval: str = "1min", time_period: int = 10, series_type: str = "close") -> dict | None:
        """
            Learn more about relative strength index (RSI) at: https://www.investopedia.com/terms/r/rsi.asp
            Get the relative strength index (RSI) for a given interval.
            - params:
                - ticker (str): The ticker for which to get the relative strength index (RSI).
                - interval (str): The interval for which to get the relative strength index (RSI).
                    - daily: daily
                    - weekly: weekly
                    - monthly: monthly
                - time_period (int): The time period for which to get the relative strength index (RSI).
                - series_type (str): The series type for which to get the relative strength index (RSI).
                    - open: open
                    - high: high
                    - low: low
                    - close: close
            - returns:
                - dict: The relative strength index (RSI) for the given interval.
        """
        url = f"https://www.alphavantage.co/query?function=RSI&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}"
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None

    def get_bolinger_bands(self, ticker, interval: str = "1min", time_period: int = 10, series_type: str = "close") -> dict | None:
        """
            Learn more about bolinger bands at: https://www.investopedia.com/terms/b/bollingerbands.asp
            Get the bolinger bands for a given interval.
            - params:
                - ticker (str): The ticker for which to get the bolinger bands.
                - interval (str): The interval for which to get the bolinger bands.
                    - daily: daily
                    - weekly: weekly
                    - monthly: monthly
                - time_period (int): The time period for which to get the bolinger bands.
                - series_type (str): The series type for which to get the bolinger bands.
                    - open: open
                    - high: high
                    - low: low
                    - close: close
            - returns:
                - dict: The bolinger bands for the given interval.
        """
        url = f"https://www.alphavantage.co/query?function=BBANDS&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}"
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None

    def get_atr(self, ticker: str, interval: str = "1min", time_period: int = 10, series_type: str = "close") -> dict | None:
        """
            Learn more about average true range (ATR) at: https://www.investopedia.com/terms/a/atr.asp \n
            Get the average true range (ATR) for a given interval.
            - params:
                - ticker (str): The ticker for which to get the average true range (ATR).
                - interval (str): The interval for which to get the average true range (ATR).
                    - daily: daily
                    - weekly: weekly
                    - monthly: monthly
                - time_period (int): The time period for which to get the average true range (ATR).
                - series_type (str): The series type for which to get the average true range (ATR).
                    - open: open
                    - high: high
                    - low: low
                    - close: close
            - returns:
                - dict: The average true range (ATR) for the given interval.
        """
        url = f"https://www.alphavantage.co/query?function=ATR&symbol={ticker}&interval={interval}&time_period={time_period}&series_type={series_type}&apikey={self.api_key}"
        r = requests.get(url)
        return requests.get(url).json() if r.status_code == 200 else None
