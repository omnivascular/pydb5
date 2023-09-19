import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pydb.settings")
django.setup()

import csv
from csv_diff import load_csv, compare
from datetime import datetime, date, time
from dateutil.parser import parse
from pydb4.models import Vendor, Product
from django.db.models import Q
from django.core.serializers import serialize
from django.contrib.auth.models import User
import json
import time
import os
import csv
import pandas as pd
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import date, datetime, timedelta
import time


# from .pydb import settings

# settings.configure()

file = r"C:\Users\omniv\OneDrive\Documents\pydb4\pydb\inventory.csv"
file_barcodes = r"C:\Users\omniv\OneDrive\Documents\pydb4\pydb\inventory-barcodes.csv"

vendor_details = {
    1: ["Boston Scientific", "BSCI"],
    2: ["Abbott", "ABBT"],
    3: ["ev3/Covidien/Medtronic", "MTRNC"],
    4: ["COOK Medical", "COOK"],
    5: ["Terumo", "TRMO"],
    6: ["Coulmed", "COULMD"],
    7: ["Medline", "MEDLNE"],
    8: ["Bard Peripheral Vascular", "BARD"],
}


def construct_search_query(queries):
    if len(queries) == 1:
        return queries[0]  # Base case: return the single query

    # Recursive case: combine the first query with the result of the recursive call
    return Q(queries[0]) | construct_search_query(queries[1:])


# this other construct query function now finds the presence of 2+ items together
def construct_search_query2(queries):
    if len(queries) == 1:
        return queries[0]  # Base case: return the single query

    # Recursive case: combine the first query with the result of the recursive call
    return Q(queries[0]) & construct_search_query(queries[1:])


def convert_date_to_db_format(date_str):
    date = datetime.strptime(date_str, "%m-%d-%Y")
    return date.strftime("%Y-%m-%d")


def convert_date_to_display_format(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%m-%d-%Y")


def convert_date_to_search_format(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date


def test_format(date_str):
    date_object = datetime.strptime(date_str, "%m-%d-%Y")
    formatted_date = date_object.strftime("%Y-%m-%d")
    date = datetime.strptime(formatted_date, "%Y-%m-%d")
    return date


def csv_from_api_current_inventory():
    SPREADSHEET_ID = (
        "1RxgAXxiuERj1QF3xrMXSP5Ed-9PYglHBnoaWb7q62AY"  # Copy_Current_Inventory sheet
    )
    RANGE_NAME = "Sheet1"
    CSV_FILE = f"current-inventory-asof-{datetime.now().date().strftime('%m-%d-%Y--%H_%M_%S')}.csv"
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    service = build("sheets", "v4", credentials=creds)
    result = (
        service.spreadsheets()
        .values()
        .get(spreadsheetId=SPREADSHEET_ID, range=RANGE_NAME)
        .execute()
    )
    values = result.get("values", [])
    try:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerows(values)
            print("CSV successfully created of current inventory!")
            return CSV_FILE
    except:
        return None


# csv_from_api_current_inventory() # works alh


def db_new_from_products_csv(file):
    print("Starting update to Database:")
    Product.objects.all().delete()
    print("All older Products deleted, updating from current inventory...")
    with open(file, "r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        for index, row in enumerate(reader, start=1):
            for row in reader:
                product = row["Product Name"].strip()
                ref_id = row["reference_id"].strip()
                expiry = row["expiry_date"].strip()
                lot_number = row["Lot_Number"].strip()
                company = row["Vendor"].strip()
                ref_id_lot_number_expiry_date = row["ref_id_lot_number_expiry_date"]
                size = row["Product Size"].strip()
                quantity = row["Quantity"].strip()
                barcode = row["Barcode"].strip()
                row_number = index
                for id, val in vendor_details.items():
                    # print(val[0], type(val[0]), row_number)
                    # print(
                    #     f"Val[0]: {val[0]}, Company: {company}, Match: {val[0].strip().lower() in company}"
                    # )
                    # if id == 1:
                    #     print(val, val[0], company)
                    try:
                        if company.lower() == val[0].lower():
                            vendor = Vendor.objects.get(id=int(id))
                            break
                    except:
                        raise TypeError("Vendor not found for company: " + company)
                product = Product(
                    name=product,
                    reference_id=ref_id,
                    expiry_date=test_format(expiry),
                    lot_number=lot_number,
                    ref_id_lot_number_expiry_date=ref_id_lot_number_expiry_date,
                    barcode=barcode,
                    size=size,
                    quantity_on_hand=quantity,
                    vendor=vendor,
                    employee=User.objects.get(id=1),
                )
                product.save()
                print(f"Product {product} added to DB successfully.")
    print("Database update complete, now based on current inventory.")


# db_new_from_products_csv(
#     r"C:\Users\omniv\OneDrive\Documents\pydb4\pydb\current-inventory-asof-09-14-2023--00_00_00.csv"
# )

#----- run below if need to update entire inventory based on CSV on sheets
# db_new_from_products_csv(csv_from_api_current_inventory())


