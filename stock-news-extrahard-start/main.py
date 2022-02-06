import requests
from twilio.rest import Client
from datetime import datetime

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"
stock_endpoint = "https://www.alphavantage.co/query"
new_endpoint = "https://newsapi.org/v2/everything"
stock_api_key = "VDHHHEY15ZFAZTYT"
new_api_key = "17336b4300984e0091071e4ea222e9ec"
account_sid = "AC4b8e29a556acf61eaa57b428f44d0805"
auth_token = "e811c0c1cb79ed5e8331a735857c2896"
parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "interval": "60min",
    "apikey": stock_api_key,
}
today = datetime.now().date()
new_parameters = {
    "q":COMPANY_NAME,
    "sortBy": "popularity",
    "apiKey": new_api_key,
    "from": today,
}

stock_response = requests.get(url=stock_endpoint, params=parameters)
stock_response.raise_for_status()
stock_data = stock_response.json()
daily_data = stock_data["Time Series (Daily)"]
price_list = [daily_data[key]["4. close"] for (key, value) in daily_data.items()]

yesterdays_price = float(price_list[0])
day_before_yesterdays_price = float(price_list[1])
difference = yesterdays_price - day_before_yesterdays_price

average_price = (yesterdays_price + day_before_yesterdays_price)/2
percent_difference = round((difference / average_price) * 100)
print(percent_difference)
up_down = None
if percent_difference > 1:
    up_down = "🔺"
else:
    up_down = "🔻"

if abs(percent_difference) >= 0:
    new_response = requests.get(url=new_endpoint, params=new_parameters)
    new_response.raise_for_status()
    news_data = new_response.json()
    new_article = news_data['articles'][:3]
    article_list = [f"{STOCK}: {up_down}{percent_difference}%\nHeadline: {article['title']}\nNews: {article['description']}" for article in new_article]

    client = Client(account_sid, auth_token)
    for each_article in article_list:
        message = client.messages \
            .create(
            body=each_article,
            from_='+19106019171',
            to='6825533300'
        )

