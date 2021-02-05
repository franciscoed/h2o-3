#!/usr/bin/python3
import pandas as pd
import requests
import json
from datetime import datetime, timedelta
import time
import sys
import os

# pylint: disable=unbalanced-tuple-unpacking

if "API_KEY" not in os.environ:
    print("No API key has been found")
    sys.exit(1)

if "STOCK_DIR" not in os.environ:
    STOCK_DIR = "/tmp"
else:
    STOCK_DIR = os.environ["STOCK_DIR"]

api_key = os.environ["API_KEY"]

stocks = (
    "ABEV3.BVMF",
    "AZUL4.BVMF",
    "B3SA3.BVMF",
    "BBAS3.BVMF",
    "BBDC3.BVMF",
    "BBDC4.BVMF",
    "BBSE3.BVMF",
    "BPAC11.BVMF",
    "BRAP4.BVMF",
    "BRDT3.BVMF",
    "BRFS3.BVMF",
    "BRKM5.BVMF",
    "BRML3.BVMF",
    "BTOW3.BVMF",
    "CCRO3.BVMF",
    "CIEL3.BVMF",
    "CMIG4.BVMF",
    "CSAN3.BVMF",
    "CSNA3.BVMF",
    "CVCB3.BVMF",
    "CYRE3.BVMF",
    "ECOR3.BVMF",
    "EGIE3.BVMF",
    "ELET3.BVMF",
    "ELET6.BVMF",
    "EMBR3.BVMF",
    "ENBR3.BVMF",
    "EQTL3.BVMF",
    "FLRY3.BVMF",
    "GGBR4.BVMF",
    "GNDI3.BVMF",
    "GOAU4.BVMF",
    "GOLL4.BVMF",
    "HYPE3.BVMF",
    "IGTA3.BVMF",
    "IRBR3.BVMF",
    "ITSA4.BVMF",
    "ITUB4.BVMF",
    "JBSS3.BVMF",
    "KLBN11.BVMF",
    "KROT3.BVMF",
    "LAME4.BVMF",
    "LREN3.BVMF",
    "MGLU3.BVMF",
    "MRFG3.BVMF",
    "MRVE3.BVMF",
    "MULT3.BVMF",
    "NATU3.BVMF",
    "PCAR4.BVMF",
    "PETR3.BVMF",
    "PETR4.BVMF",
    "QUAL3.BVMF",
    "RADL3.BVMF",
    "RAIL3.BVMF",
    "RENT3.BVMF",
    "SANB11.BVMF",
    "SBSP3.BVMF",
    "SMLS3.BVMF",
    "SUZB3.BVMF",
    "TAEE11.BVMF",
    "TIMP3.BVMF",
    "UGPA3.BVMF",
    "USIM5.BVMF",
    "VALE3.BVMF",
    "VIVT4.BVMF",
    "VVAR3.BVMF",
    "WEGE3.BVMF",
    "YDUQ3.BVMF",
)


def get_stock(symbol):
    date_from = (datetime.now() - timedelta(days=366)).strftime("%Y-%m-%d")
    url = (
        "https://api.marketstack.com/v1/eod?symbols="
        + symbol
        + "&access_key="
        + api_key
        + "&date_from"
        + date_from
        + "&limit=500"
        + "&sort=DESC"
    )
    r = requests.get(url)
    return r.text


def json_to_csv(json_body):
    header = "date,1. open,2. high,3. low,4. close,5. volume\n"
    json_dict = json.loads(json_body)
    csv_body = header
    for i in json_dict["data"]:
        csv_body += (
            i["date"].split("T")[0]
            + ","
            + str(i["open"])
            + ","
            + str(i["high"])
            + ","
            + str(i["low"])
            + ","
            + str(i["close"])
            + ","
            + str(i["volume"])
            + f"\n"
        )
    return csv_body


# Only ping API on weekdays

if datetime.today().weekday() < 5:
    minute_start = datetime.now().minute
    counter = 0
    for i in stocks:
        print("Stock is: " + i)
        print("Counter is: " + str(counter))
        print("Minute start is: " + str(minute_start))
        df = get_stock(i)
        # Make the stock name backwards compatible with World trading data
        csv_body = json_to_csv(df)
        stock_file_name = i.replace(".BVMF", ".SA")
        file_name = STOCK_DIR + "/" + stock_file_name
        output_csv = open(file_name, "w")
        output_csv.write(csv_body)
        output_csv.close()

        counter = counter + 1
        if counter == 4:
            print("Sleeping")
            time.sleep(70)
            minute_start = datetime.now().minute
            counter = 0
else:
    print("Weekend")


# Exit gracefully
sys.exit(0)
