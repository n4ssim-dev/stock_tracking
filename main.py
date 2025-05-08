import requests
import os
from dotenv import load_dotenv

AV_API_KEY = os.getenv('AV_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')

load_dotenv()

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

url = f'{STOCK_ENDPOINT}?function=REALTIME_BULK_QUOTES&symbol=MSFT,AAPL,IBM&apikey={AV_API_KEY}'
response = requests.get(url)
if response.status_code == requests.codes.ok:
    print(response.json())
    data = response.json()["data"]
    stock_fluctuation = {item["symbol"]: float(item["change_percent"]) for item in data}
    pos_stocks = []
    neg_stocks = []
    high_pos = []
    low_neg = []
    prev_value = None

    for stock,value in stock_fluctuation.items():
        if not value > 0:
            neg_stocks.append({stock:value})
        elif value > 0:
            pos_stocks.append({stock: value})
        else:
            pass

    for stock, value in stock_fluctuation.items():
        if prev_value is not None:
            if value > prev_value:
                high_pos.append({stock: value})
            elif value < prev_value:
                low_neg.append({stock: value})

        prev_value = value


    to_send_message = f'Ton action la plus en hausse est {list(high_pos[0].keys())[0]} avec +{list(high_pos[0].values())[0]}% 📈\nTon action la plus en baisse {list(low_neg[0].keys())[0]} avec {list(low_neg[0].values())[0]}% 📉'
    print(to_send_message)
else:
    print("Error: ", response.status_code, response.text)