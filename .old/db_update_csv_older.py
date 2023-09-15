import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pydb.settings")
django.setup()

import csv
from datetime import datetime
from dateutil.parser import parse
from pydb4.models import Vendor, Product
from django.db.models import Q

# from .pydb import settings

# settings.configure()

# file = r"C:\Users\omniv\OneDrive\Documents\pydb4\pydb\inventory.csv"
file = r"C:\Users\omniv\OneDrive\Documents\pydb4\pydb\inventory-barcodes.csv"

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


def convert_date_to_db_format(date_str):
    date = datetime.strptime(date_str, "%m-%d-%Y")
    return date.strftime("%Y-%m-%d")


def convert_date_to_display_format(date_str):
    date = datetime.strptime(date_str, "%Y-%m-%d")
    return date.strftime("%m-%d-%Y")


"""
    name = models.CharField(max_length=300)
    reference_id = models.CharField(max_length=100)
    expiry_date = models.DateField(auto_now=False, auto_now_add=False)
    ref_id_expiry_date = models.CharField(max_length=250, unique=True)
    is_purchased = models.BooleanField(default=True)
    size = models.CharField(max_length=60, default="N/A")
    quantity_on_hand = models.IntegerField(default=1)
    quantity_on_order = models.IntegerField(default=0)
    last_modified = models.DateField(auto_now=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)
"""

# Only populating products table, as vendors already created (only 6 distinct vendors currently)
# if __name__ == "main":
print("Starting app to update DB...")
with open(file, "r", encoding="utf-8", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    # next(reader)
    for index, row in enumerate(reader, start=1):
        # for row in reader:
        row_number = index
        # print(f"At this row: {row_number}, for item: {row}")
        name = row["product"]
        reference_id = row["reference_id"]
        expiry_date = convert_date_to_db_format(row["expiry_date"])
        size = row["size"]
        quantity_on_hand = int(row["quantity"])
        company = str(row["company"]).strip().lower()
        # print(company)
        # print(type(company))
        # print(name)
        for id, val in vendor_details.items():
            # print(val[0], type(val[0]), row_number)
            # print(
            #     f"Val[0]: {val[0]}, Company: {company}, Match: {val[0].strip().lower() in company}"
            # )
            if company.lower() in val[0].strip().lower():
                vendor = Vendor.objects.get(id=int(id))
            else:
                # print(row)
                # raise TypeError("Vendor not found for company: " + company)
                pass

        product_check = Product.objects.filter(
            Q(reference_id__exact=reference_id)
            & Q(expiry_date__exact=expiry_date)
            & Q(name__exact=name)
        )

        if not product_check.exists():
            # product = Product(
            #     name=name,
            #     reference_id=reference_id,
            #     expiry_date=expiry_date,
            #     size=size,
            #     quantity_on_hand=quantity_on_hand,
            #     vendor=vendor,
            # )
            # product.save()
            print("almost ready")
        elif product_check.exists():
            print(len(product_check))
            for p in product_check:
                if p.reference_id == reference_id:
                    print(p.name)

        else:
            print("Item already present in DB, skipping.")
