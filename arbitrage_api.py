import requests

API_URL = 'https://api.rr28.xyz/arbitrages/active/'

def get_arbitrage():
    response = requests.get(API_URL)
    print (response.json())

if __name__ == "__main__":
    get_arbitrage()
    