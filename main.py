import requests
from dotenv import load_dotenv
import os
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from alpha_vantage.timeseries import TimeSeries
from dash import html, dcc, dash
from dash.dependencies import Output, Input
import dash_bootstrap_components as dbc
import yfinance as yf
import time


def create_card(title, content, color, icon, footer) -> dbc.Card | None:
    try:
        card = dbc.CarD([
            dbc.CardHeader([
                html.Img(src=icon, className="card-icon"),
                html.H2(title),
            ], style={"display": "flex", "align-items": "center"}),
            dbc.CardBody(
                [
                    content
                ]
            ),
            dbc.CardFooter(
                [
                    footer
                ]
            )
        ])
        return card
    except:
        return None


load_dotenv()
api_key = os.getenv("API_KEY")


fontawesome_icons = {
    'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
    'rel': 'stylesheet',
    'integrity': 'sha384-500 BUHEmvpQ+1IW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
    'crossorigin': 'anonymous'
}

custom_css = {
    "href": "./assets/style.css",
    "rel": "stylesheet",
}


app = dash.Dash(__name__, external_stylesheets=[
                dbc.themes.COSMO, fontawesome_icons, custom_css])

server = app.server

# stock name to show in the graph
STOCK_NAME = "Stock Name"

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand(html.H1("Findash"), href="#"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("HOME", href="/")),
                    dbc.NavItem(dbc.NavLink("ABOUT US", href="/about")),
                    dbc.NavItem(dbc.NavLink("CONTACT US", href="/contact")),
                ],
                className="ml-auto",
                navbar=True,
            ),
        ],
        fluid=True,
    ),
    color="light",
    light=True,
    dark=False,
    sticky="top",
    class_name="py-3 px-5"
)

stock_symbol_input = dbc.Col([
    dbc.Label("Stock Symbol", html_for="stock-symbol"),
    dbc.Input(
        type="text",
        id="stock-symbol",
        placeholder="Enter stock symbol",
        className="mb-3",
        value="MSFT"
    ),

], width=6)

interval_input = dbc.Col(
    [
        dbc.Label("Interval", html_for="interval"),
        dbc.Select(
            id="interval",
            options=[
                {"label": "1 min", "value": "1m"},
                {"label": "5 min", "value": "5m"},
                {"label": "15 min", "value": "15m"},
                {"label": "30 min", "value": "30m"},
                {"label": "60 min", "value": "1h"},
                {"label": "Daily", "value": "1d"},
                {"label": "Weekly", "value": "1wk"},
                {"label": "Monthly", "value": "1mo"},
            ],
            value="1h"
        )
    ],
    width=3,
)

period_input = dbc.Col(
    [
        dbc.Label("Period", html_for="period"),
        dbc.Select(
            id="period",
            options=[
                {"label": "1 day", "value": "1d"},
                {"label": "5 days", "value": "5d"},
                {"label": "1 month", "value": "1mo"},
                {"label": "3 months", "value": "3mo"},
                {"label": "6 months", "value": "6mo"},
                {"label": "1 year", "value": "1y"},
                {"label": "2 years", "value": "2y"},
                {"label": "5 years", "value": "5y"},
                {"label": "10 years", "value": "10y"},
                {"label": "Year today", "value": "ytd"},
                {"label": "Max", "value": "max"},
            ],
            value="1mo"
        )
    ], width=3,)


chart_type_input = dbc.Col(
    [
        dbc.Label("Chart Type", html_for="chart-type"),
        dbc.RadioItems(
            id="chart-type",
            options=[
                {"label": "Line", "value": "line"},
                {"label": "Candlestick", "value": "candlestick"},
                {"label": "OHLC", "value": "ohlc"},
            ],
            value="line",
            style={"display": "inline-block", "margin-left": "10px"}
        )
    ])

submit_button = dbc.Col([
    dbc.Button("Submit", id="submit-button", color="primary")
])


app.layout = html.Div([
    # Container for the navbar
    dbc.Container([
        dbc.Row([
            navbar
        ])
    ]),
    # Container for the inputs and submit button
    dbc.Container([
        dbc.Row([
            stock_symbol_input,
            interval_input,
            period_input,

        ], className="mt-5"),
        dbc.Row([
            chart_type_input,
            submit_button
        ])
    ]),
    # Container for the stock name and logo + favorite star
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Img(
                    src="https://img.icons8.com/ios/50/000000/stock-market.png", id="stock-icon"),
                html.H1(
                    id="stock-name", style={"text-align": "center", "display": "inline-block"}),
                html.I("★", className="favorite-star tooltip",
                       style={"font-size": "30px", "color": "rgb(255, 215, 0)"}),

            ], style={"display": "flex", "align-items": "center"}, width=10)
        ]),
    ]),
    # Container for the graph
    dbc.Container([
        dbc.Row([
            dbc.Col([
                  dcc.Graph(id="stock-graph")
                  ], width=12)
        ])
    ]),
    # Container for the fundamental and technical data
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        [
                            html.H3("Fundamental data", style={
                                    "margin-left": "30px"})
                        ],
                        style={"display": "flex", "align-items": "center"}
                    ),
                    dbc.CardBody([
                        html.Ul([], id="stock-info")
                    ]),
                    dbc.CardFooter("Stock Info")
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([

                        html.H3("Technical Data", style={
                                "margin-left": "30px"})
                    ], style={"display": "flex", "align-items": "center"}),
                    dbc.CardBody([
                        html.Ul([], id="company-technical-data")
                    ]),
                    dbc.CardFooter("Company's technical data")
                ])
            ], width=6),
        ])
    ], className="mt-5 my-5"),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader([
                        html.Img(
                            src="https://img.icons8.com/ios/50/000000/news.png", id="news-icon"),
                        html.H3("Company's news", style={
                                "margin-left": "30px"})
                    ], style={"display": "flex", "align-items": "center"}),
                    dbc.CardBody([
                        html.Ul([], id="company-news")
                    ]),
                    dbc.CardFooter("company's news")
                ])
            ], width=12)
        ])
    ]),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Stock Recommendations"),
                    dbc.CardBody([
                        dcc.Graph(id="stock-recommendation")
                    ]),
                    dbc.CardFooter("Stock Recommendation")
                ])
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Company's upcoming events"),
                    dbc.CardBody([
                        dbc.Table([
                            html.Thead([
                                html.Tr([
                                    html.Th("Event"),
                                    html.Th("Date"),
                                    html.Th("Time"),
                                    html.Th("Impact"),
                                    html.Th("More Info"),
                                ])
                            ]),
                            html.Tbody([
                                html.Tr([
                                    html.Td("Event"),
                                    html.Td("Date"),
                                    html.Td("Time"),
                                    html.Td("Impact"),
                                    html.Td("More Info"),
                                ])
                            ]),
                        ]),
                        dbc.CardFooter("company's news")
                    ])
                ]),
            ], width=6),
        ]),
    ], className="mt-5 my-5"),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Economic Calendar"),
                    dbc.CardBody([
                        dbc.Table([
                            html.Thead([
                                html.Tr([
                                    html.Th("Country"),
                                    html.Th("Event"),
                                    html.Th("Date"),
                                    html.Th("Time"),
                                    html.Th("Impact"),
                                    html.Th("More Info"),
                                ]),
                            ]),
                            html.Tbody([
                                html.Tr([
                                    html.Td("Country"),
                                    html.Td("Event"),
                                    html.Td("Date"),
                                    html.Td("Time"),
                                    html.Td("Impact"),
                                    html.Td("More Info"),
                                ]),
                            ]),
                        ]),
                        dbc.CardFooter("Economic Calendar")
                    ])
                ])
            ], width=12),
        ])
    ], className="mt-5 my-5"),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Market's indicators"),
                    dbc.CardBody([
                        dbc.Table([
                            html.Thead([
                                html.Tr([
                                    html.Th("Name"),
                                    html.Th("Current"),
                                    html.Th("Forecast"),
                                    html.Th("Upcoming"),
                                ])
                            ]),
                            html.Tbody([
                                html.Tr([
                                    html.Td("Name"),
                                    html.Td("Current"),
                                    html.Td("Forecast"),
                                    html.Td("Upcoming"),
                                ])
                            ])
                        ])
                    ])
                ])
            ], width=6),

            dbc.Col([
                    dbc.Card([
                        dbc.CardHeader("Economic News"),
                        dbc.CardBody([
                            "Economic News"
                        ]),
                        dbc.CardFooter("Economic News")
                    ])

                    ], width=6),
        ])
    ], className="mt-5 my-5"),
    html.Hr(),
    dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Footer([
                    html.P("All rights reserved © 2020"),
                    html.P([
                        "Made By Habib"
                    ]),
                    dbc.Nav([
                        dbc.NavItem(dbc.NavLink(
                            html.P("Gtihub"), href="https://github.com/Habib97SE")),
                        dbc.NavItem(dbc.NavLink(
                            html.P("LinkedIn"), href="https://www.linkedin.com/in/habiballah-hezarehee/")),

                    ], className="ml-auto")
                ], className="center")
            ], width=8, className="center col-lg-3 mg-auto")
        ])
    ], className="mt-5 my-5 center"),
])


def plot_candlestick(data: pd.DataFrame) -> go.Figure:
    """
        Plot candlestick chart
        - Params:
            - data: dataframe
        - Returns:
            - candlestick chart
    """
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                                         open=data['Open'],
                                         high=data['High'],
                                         low=data['Low'],
                                         close=data['Close'])])
    fig.update_layout(
        title="Candlestick Chart",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False
    )
    return fig


def plot_line_chart(data: pd.DataFrame) -> go.Figure:
    """
        Plot line chart
        - Params:
            - data: dataframe
        - Returns:
            - line chart
    """
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data.index, y=data['Close'],
                             mode='lines', name='Close'))

    fig.update_layout(
        title="Line Chart",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False
    )
    return fig


def plot_chart(data: pd.DataFrame, chart_type: str) -> go.Figure:
    """
        Plot chart
        - Params:
            - data: dataframe
            - chart_type: chart type
        - Returns:
            - chart
    """
    if chart_type == "line":
        return plot_line_chart(data)
    chart_types = {
        "candlestick": go.Candlestick,
        "ohlc": go.Ohlc,
    }
    fig = go.Figure(data=[chart_types[chart_type](x=data.index,
                                                  open=data['Open'],
                                                  high=data['High'],
                                                  low=data['Low'],
                                                  close=data['Close'])])
    fig.update_layout(
        title="Candlestick Chart",
        yaxis_title="Stock Price (USD)",
        xaxis_rangeslider_visible=False,
    )
    return fig


def get_stock_tricker(company_name):
    """
        Get stock ticker from company name
        - Params:
            - company_name: company name
        - Returns:
            - stock ticker
    """
    yfinance = "https://query2.finance.yahoo.com/v1/finance/search"
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    params = {"q": company_name, "quotes_count": 1, "country": "United States"}

    res = requests.get(url=yfinance, params=params,
                       headers={'User-Agent': user_agent})
    data = res.json()

    company_code = data['quotes'][0]['symbol']
    return company_code


def get_stock_data(symbol, interval, period=None) -> pd.DataFrame | None:
    """
        Get stock data from Alpha Vantage API
        - Params:
            - symbol: stock symbol (e.g. AAPL)
            - interval: time interval [1m, 5m, 15m, 30m, 1h, 1d, 1wk, 1mo]
            - period: time period [1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max]
        - Returns:
            - data: stock data
    """
    periods = {
        "1m": "1d",
        "5m": "5d",
        "15m": "1mo",
        "30m": "1mo",
        "1h": "1mo",
        "1d": "1y",
        "1wk": "2y",
        "1mo": "5y"
    }
    period = period if period else periods[interval]
    stock_data = yf.download(symbol, interval=interval,
                             period=period)
    if stock_data.empty:
        symbol = get_stock_tricker(symbol)
        stock_data = yf.download(symbol, interval=interval, period=period)
        if stock_data.empty:
            return None
    return stock_data


def get_stock_overview(symbol):
    """
        Get stock overview from Alpha Vantage API
        - Params:
            - symbol: stock symbol
        - Returns:
            - data: stock overview
    """
    ts = TimeSeries(key=api_key, output_format='pandas')
    data, meta = ts.get_quote_endpoint(symbol=symbol)
    return data


def build_li_item(name, value):
    """
        Build li item for stock overview
    """
    return html.Li([name, html.Strong(value)])


def get_recommendations(ticker) -> px.pie:
    """
        This method will return the pie chart with recommendations for a given stock
        - Params:
            - ticker: stock ticker  
        - Returns:
            - pie chart with recommendations
    """
    try:
        df_recommendations = yf.Ticker(ticker).recommendations
        df_recommendations = df_recommendations.reset_index()

        buy = df_recommendations[df_recommendations['To Grade']
                                 == 'Buy'].count()
        hold = df_recommendations[df_recommendations['To Grade'] == 'Hold'].count(
        )
        sell = df_recommendations[df_recommendations['To Grade'] == 'Sell'].count(
        )
        fig = px.pie(names=['Buy', 'Hold', 'Sell'], values=[
                     buy['To Grade'], hold['To Grade'], sell['To Grade']], title=f'Recommendations for {format(ticker)}')
        return fig
    except:
        return None


def get_info(ticker: str):
    """
        This method will return the info about the company
        - Params:
            - ticker: stock ticker
        - Returns:
            - info about the company
    """
    while True:
        try:
            return yf.Ticker(ticker)
        except:
            time.sleep(5)
            continue


"""
    Show chart with stock data
"""


@ app.callback(
    Output("stock-graph", "figure"),
    Input("stock-symbol", "value"),
    Input("interval", "value"),
    Input("period", "value"),
    Input("chart-type", "value")
)
def update_graph(symbol, interval, period, chart_type):
    """
        Update graph with new data
    """
    data = get_stock_data(symbol, interval, period)

    if data is None:
        fig = go.Figure()
        fig.update_layout(
            xaxis_title="Wrong input, try again",
            font=dict(
                family="Courier New, monospace",
                size=38,
                color="#7f7f7f"
            )
        )
    return plot_chart(data, chart_type)


"""
    Show the company's key data in a list format
    This list include data like Company's name, sector, dividend and other important data
"""


@ app.callback(
    Output("stock-info", "children"),
    Input("stock-symbol", "value"),
)
def update_fundamental_info(symbol):
    """
        Get stocks info and update stock-info list with new data from yfinance
    """
    stock_info = get_info(symbol)
    return [
        build_li_item("Company Name: ", stock_info.info['longName']),
        build_li_item("Industry: ", stock_info.info['industry']),
        build_li_item("Sector: ", stock_info.info['sector']),
        build_li_item("Market Cap: ", stock_info.fast_info['market_cap']),
        build_li_item("Country: ", stock_info.info['country']),
        build_li_item("Dividend Yield: ", stock_info.info['dividendYield']),
        build_li_item("Dividend Rate: ", stock_info.info['dividendRate']),
        build_li_item("EPS: ", stock_info.info['trailingEps']),
        build_li_item("PE Ratio: ", stock_info.info['trailingPE']),
        build_li_item("Operating Margin: ",
                      stock_info.info['operatingMargins']),
        build_li_item("Profit Margin: ", stock_info.info['profitMargins']),
        build_li_item("Price to Book: ", stock_info.info['priceToBook']),
        build_li_item("Price to Sales: ",
                      stock_info.info['priceToSalesTrailing12Months']),
        build_li_item("Price to Earnings: ", stock_info.info['trailingPE']),
        build_li_item("Forward Price to Earnings: ",
                      stock_info.info['forwardPE']),
        build_li_item("PEG Ratio: ", stock_info.info['pegRatio']),
        build_li_item("Beta: ", stock_info.info['beta']),
        build_li_item("Revenue Growth: ", stock_info.info['revenueGrowth']),
        build_li_item("Earnings Growth: ", stock_info.info['earningsGrowth']),
    ]


"""
    Show the company's logo based on the symbol
"""


@ app.callback(
    Output("stock-icon", "src"),
    Input("stock-symbol", "value"),
)
def update_icon(symbol):
    """
        Get stock icon from yfinance
    """
    stock = get_info(symbol)
    return stock.info['logo_url']


"""
    Show the company's name based on the symbol
"""


@ app.callback(
    Output("stock-name", "children"),
    Input("stock-symbol", "value"),
)
def update_name(symbol):
    # Get companys full name based on  symbol  from yfiance api
    stock = get_info(symbol)
    return stock.info['longName']


"""
    Add Company's news to the news section
"""


@ app.callback(
    Output("company-news", "children"),
    Input("stock-symbol", "value"),
)
def update_news(symbol):
    stock_news = yf.Ticker(symbol)
    return [html.Li([html.A(news['title'], href=news['link'])]) for news in stock_news.news]


@app.callback(
    Output("stock-recommendation", "figure"),
    Input("stock-symbol", "value"),
)
def update_sentiment(symbol):
    return get_recommendations(symbol)


def main():
    app.run_server(debug=True)


if __name__ == "__main__":
    main()
