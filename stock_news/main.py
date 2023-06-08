import requests
import os
from twilio.rest import Client
from time import sleep

# Company details
STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

# api endpoints
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

# api keys
ALPHA_VANTAGE_API_KEY = os.environ.get('ALPHA_VANTAGE_API_KEY')
NEWS_API_KEY = os.environ.get('NEWS_API_KEY')

# Twilio credentials
ACCOUNT_SID = 'AC8b3eba844325028974886915329a3d33'
AUTH_TOKEN = os.environ.get('AUTH_TOKEN')

def message_template(stock_name, percent_change, news_item):
    msg_template = \
        f"""
    {stock_name}: {percent_change}    
    Headline: {news_item.get('title')}.
    Brief: {news_item.get('content')}
    """
    return msg_template


# Function to send sms
def send_sms(message, phone):
    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    message = client.messages \
        .create(
            body=message,
            from_='+14793974417',
            to=phone)
    print(message.status)


stock_price_params = {'function': 'TIME_SERIES_DAILY_ADJUSTED',
                      'symbol': STOCK_NAME,
                      'apikey': ALPHA_VANTAGE_API_KEY}

get_stock_data = requests.get(STOCK_ENDPOINT, params=stock_price_params)
get_stock_data.raise_for_status()
stock_data = get_stock_data.json()

stock_data_vals = [v for (k, v) in stock_data.get('Time Series (Daily)').items()]
close_price_yesterday = float(stock_data_vals[0].get('4. close'))
print(close_price_yesterday)

close_price_day_before = float(stock_data_vals[1].get('4. close'))
print(close_price_day_before)

diff_price = abs(close_price_yesterday - close_price_day_before)

diff_price_percent = round(diff_price / close_price_yesterday * 100, 2)
pc_change = f'🔺{diff_price_percent}%' if close_price_yesterday > close_price_day_before else f'🔻{diff_price_percent}%'
print(pc_change)

news_params = {'q': COMPANY_NAME,
               'from': '2023-05-25',
               'sortBy': 'publishedAt',
               'apiKey': NEWS_API_KEY}

get_company_news = requests.get(NEWS_ENDPOINT, params=news_params)
get_company_news.raise_for_status()
company_news_articles = get_company_news.json().get('articles')[:3]

for news in company_news_articles:
    msg = message_template(STOCK_NAME, pc_change, news)
    send_sms(msg, '+919632728233')
    sleep(5)
