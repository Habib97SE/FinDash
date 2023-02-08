from Financial_Models.Economic_Calendar import Economic_Calendar
from Financial_Models.Technical_Indicator import Technical_Indicators
from Financial_Models.Fundamental_Indicator import Fundamental_Indicators


def main():
    economic_calendar = Economic_Calendar()
    technical_indicators = Technical_Indicators()
    fundamental_indicators = Fundamental_Indicators("AAPL")

    company_info = fundamental_indicators.company_info['Description']

    print(company_info)



if __name__ == "__main__":
    main()
