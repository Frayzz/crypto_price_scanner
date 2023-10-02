import asyncio
import requests

class Exchange:
    def __init__(self, name, url):
        self.name = name
        self.url = url
        self.prices = {}

    async def fetch_price(self, ticker1, ticker2):
        response = requests.get(url=self.url, params={'symbol': f'{ticker1}_{ticker2}'})
        if response.ok:
            response_json = response.json()
            try:
                last_price = response_json['data'][0]['last']
                print(f"{ticker1}-{ticker2} price is {last_price} {self.name}")
                await asyncio.sleep(3)
                self.prices[ticker1] = last_price
            except:
                print(f"{ticker1} не найден")

async def main():
    exchanges = [
        Exchange("MEXC", 'http://mexc.com/open/api/v2/market/ticker'),
        Exchange("BINANCE", 'https://api.binance.com/api/v3/ticker/price'),
        Exchange("KUKOIN", 'https://api.kucoin.com/api/v1/market/orderbook/level1'),
        Exchange("BYBIT", 'https://api.bybit.com/spot/v3/public/quote/ticker/bookTicker')
    ]

    coin_array = ['BTC', 'IGU', 'ADA', 'SHIB', 'DOGI']

    for i in coin_array:
        ticker1 = i
        ticker2 = 'USDT'
        tasks = [exchange.fetch_price(ticker1, ticker2) for exchange in exchanges]
        await asyncio.gather(*tasks)

        print({exchange.name: exchange.prices for exchange in exchanges})
        
        if len(exchanges) >= 2:
            max_val = max(exchange.prices.get(ticker1, 0) for exchange in exchanges)
            min_val = min(exchange.prices.get(ticker1, float('inf')) for exchange in exchanges)

            if max_val > 0 and min_val < float('inf'):
                max_exchange = [exchange for exchange in exchanges if exchange.prices.get(ticker1, 0) == max_val][0]
                min_exchange = [exchange for exchange in exchanges if exchange.prices.get(ticker1, float('inf')) == min_val][0]

                max_price = max_exchange.prices[ticker1]
                min_price = min_exchange.prices[ticker1]

                print(max_price)
                print(f"Max value: {max_exchange.name}")
                print(min_price)
                print(f"Min value: {min_exchange.name}")

                percentage_change = ((max_price / min_price) - 1) * 100
                print(f"{percentage_change}%")

asyncio.run(main())
