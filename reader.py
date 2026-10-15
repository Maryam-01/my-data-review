import pandas as pd
import os


def read_flavours():
    try:
        flavours = pd.read_csv("raw_data/flavours.csv")
        if flavours.empty:
            print("file is empty")
        else:
            return flavours
    except FileNotFoundError:
        print('CSV file not found')






def read_sales():
    try:
        sales = pd.read_csv("raw_data/sales.csv")
        if sales.empty:
            print('file is empty')
        else:

            return sales
    except FileNotFoundError:
        print("csv is not found")


def read_stores():
    try:

        stores = pd.read_csv("raw_data/stores.csv")
        if stores.empty:
            print("file is empty")
        else:
            return stores
    except FileNotFoundError:
        print("csv is not found")