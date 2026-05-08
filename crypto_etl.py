import os
import requests
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import create_engine

def extract_crypto_coins():
    coins_ids = ['btc-bitcoin','eth-ethereum','usdt-tether','bnb-bnb','xrp-xrp','usdc-usdc','sol-solana']

    coin_list = []

    for coin_id in coins_ids:
        url = f"https://api.coinpaprika.com/v1/tickers/{coin_id}?quotes=USD"

        response = requests.get(url)

        if response.status_code == 200:

            data = response.json()

            #print(data)

            df_raw = pd.json_normalize(data)

            coin_list.append(df_raw)

            df_staging = pd.concat(coin_list)

        else:
            print(f"Error getting coin with error: {response.status_code}")

    return df_staging

def transform_crypto_coins(raw_data):
            
    df_staging_coins = raw_data[['name','symbol','total_supply','max_supply','last_updated','quotes.USD.price','quotes.USD.percent_change_24h']]

    df_transformed = df_staging_coins.rename(columns= { 'name': 'coin_name',
                                                        'symbol': 'coin_symbol',
                                                        'quotes.USD.price':'usd_price',
                                                        'quotes.USD.percent_change_24h':'usd_percent_change_24h'})

    df_transformed['usd_price'] = df_transformed['usd_price'].round(2)

    df_transformed['usd_percent_change_24h'] = df_transformed['usd_percent_change_24h'].round(2)

    return df_transformed

def load_crypto_coins(coins): 

    load_dotenv() 

    DB_HOST = os.getenv('DB_HOST')
    DB_NAME = os.getenv('DB_NAME')
    DB_USER = os.getenv('DB_USER')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_PORT = os.getenv('DB_PORT')

    engine = create_engine(f'postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}')

    coins.to_sql('nganga_crypto_prices',engine, if_exists='append',index=False)

extracted_coins = extract_crypto_coins() 

transformed_coins = transform_crypto_coins(extracted_coins)

loaded_coins = load_crypto_coins(transformed_coins)


