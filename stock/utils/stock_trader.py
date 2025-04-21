import requests
from bs4 import BeautifulSoup
import os
from datetime import date, timedelta
import base64
from urllib.parse import urlparse, parse_qs
from rest_framework.request import Request
# from dateutil.relativedelta import relativedelta

API_KEY = os.environ.get('AG_API_KEY')
POLYGON_API_KEY = os.environ.get('POLYGON_API_KEY')


def get_ticker_info(req):
    print(req)
    if (req.get("method") == 'GET'):
        query_string = req.get("GET")
        symbol = query_string.get('q')
    else:
        query_string = req
        symbol = query_string.get('symbol')

    # print(query_string)

    page = requests.get(f"https://www.google.com/finance/quote/{symbol}")
    soup = BeautifulSoup(page.content, 'html.parser')

    stock_symbols = soup.find('ul', class_='sbnBtf').find_all('li')

    stock_info = []
    for symbol in stock_symbols:

        stock_name = symbol.find('div', class_='COaKTb').get_text()
        stock_company_name = symbol.find('div', class_='ZvmM7').get_text()
        current_price = symbol.find('div', class_='YMlKec').get_text()

        if current_price[0] != '$':
            continue

        stock_info.append(
            {'symbol': stock_name, 'description': stock_company_name, 'current_price': current_price})

    return stock_info


def get_trade_info(req):
    query_string = req.GET
    symbol = query_string.get("symbol")
    yesterday = date.today() - timedelta(days=1)
    end = yesterday.strftime("%Y-%m-%d")
    if query_string.get('time') == '1month':
        start = yesterday - timedelta(days=40)
    # start: today - relativedelta(years=1)

    url = f"https://api.polygon.io/v2/aggs/ticker/{
        symbol}/range/1/day/{start}/{end}?adjusted=true&sort=asc&apiKey={POLYGON_API_KEY}"

    res = requests.get(url)
    data = res.json()

    return data


def get_ticker_details(req):

    if isinstance(req, Request):
        query_string = req.GET
    else:
        query_string = req.get('GET')
    symbol = query_string.get('symbol')

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:132.0) Gecko/20100101 Firefox/132.0'}

    page = requests.get(
        f"https://finance.yahoo.com/quote/{symbol}", headers=headers)

    print(page)
    soup = BeautifulSoup(page.content, 'html.parser')

    fin_streamer = soup.find('div', class_="price").find_all('fin-streamer')
    header = soup.find('div', class_='top').find('h1')

    current_price = 0
    name = header.get_text()
    price_change_amount = 0
    price_change_percent = 0

    for fin in fin_streamer:
        if 'livePrice' in fin.get('class'):
            current_price = float(fin.find('span').get_text())
        if fin.get('data-field') == 'regularMarketChange':
            price_change_amount = float(fin.get('data-value'))
        if fin.get('data-field') == 'regularMarketChangePercent':
            price_change_percent = float(fin.get('data-value'))

    return {
        'name': name,
        "current_price": current_price,
        "price_change_amount": price_change_amount,
        "price_change_percent": price_change_percent
    }


# def get_ticker_details(req):
#     query_string = req.GET
#     symbol = query_string.get('symbol')

#     url = f'https://api.polygon.io/v3/reference/tickers/{symbol}?apiKey={
#         POLYGON_API_KEY}'

#     res = requests.get(url)
#     data = res.json()

#     return data['results']


def get_ticker_picture(req):
    query_string = req.GET
    symbol = query_string.get("symbol")

    url = f"https://api.polygon.io/v3/reference/tickers/{
        symbol}?apiKey={POLYGON_API_KEY}"

    res = requests.get(url)
    data = res.json()

    try:
        image_url = data['results']['branding']['icon_url']
        image_response = requests.get(image_url + f"?apikey={POLYGON_API_KEY}")
        image_data = image_response.content

        return image_data
    except KeyError:
        # returning a default image if no image found
        default_image_url = "https://img.icons8.com/?size=100&id=gZjuzZtAaWv6&format=png&color=000000"
        default_image_response = requests.get(default_image_url)
        default_image_data = default_image_response.content

        return default_image_data


def get_stock_details(req):
    query_string = req.GET
    symbol = query_string.get('q')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36'}
    page = requests.get(
        f"https://finance.yahoo.com/quote/{symbol}", headers=headers)
    soup = BeautifulSoup(page.content, 'html.parser')

    # # print(page.content)

    stock_symbols = soup.find_all(
        attrs={'data-testid': 'quote-statistics'})[0].find('ul').find_all('li')

    # print(stock_symbols)

    stock_info = []
    for symbol in stock_symbols:
        print(symbol.find('span', class_="label"))
        # message = symbol.find('span').find(
        # 'div', class_ = 'EY8ABd-OWXEXe-TAWMXe').get_text()
        label = symbol.find('span', class_="label").get_text()
        if symbol.find('span', class_='value').find('fin-streamer') != None:
            value = symbol.find('span', class_='value').find(
                'fin-streamer').get('data-value')
        else:
            value = symbol.find('span', class_='value').get_text()

        # stock_info.append(
        #     {'label': label, 'value': value, 'message': message})
        stock_info.append({'label': label, 'value': value})

    return stock_info
