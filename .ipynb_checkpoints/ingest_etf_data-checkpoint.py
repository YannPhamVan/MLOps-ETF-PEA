import yfinance as yf
import pandas as pd
import os

def download_etf_data(etf_list, start_date, end_date, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    for etf in etf_list:
        try:
            data = yf.download(etf, start=start_date, end=end_date, interval='1d')
            data.to_parquet(f"{output_dir}/{etf.replace('.','_')}.parquet")
            print(f"{etf} downloaded: {data.shape[0]} rows.")
        except Exception as e:
            print(f"Error downloading {etf}: {e}")

if __name__ == "__main__":
    etf_list = ['EWLD.PA', 'PAEEM.PA', 'ESE.PA', 'CW8.PA']  # Modifiable
    start_date = '2020-07-01'
    end_date = '2025-07-01'
    output_dir = "./data/raw"

    download_etf_data(etf_list, start_date, end_date, output_dir)
