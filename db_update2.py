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


search = "2023-10-09"
search2 = "10-09-2023"
res = convert_date_to_search_format(search)
print(type(res))

barcodes_used = ["987654", "987652"]

products = all(
    list(
        set(
            [
                Product.objects.filter(barcode__exact=b).exists()
                for b in barcodes_used
                if b != ""
            ]
        )
    )
)
# finding = all(products)
print(products)

testing = [1, 2, 3]
t_set = set(testing)
if not t_set.add(3):
    print("it is already there")
else:
    print("it is not there")

products = Product.objects.all()

print("at len of products.distcint() ---->")
print(len(products.distinct()))
print(products.distinct().values("barcode", "expiry_date").count())
print(products.count())


file_barcodes_latest = r"C:\Users\omniv\Downloads\inventory-update-07052023.csv"


# for p in products:
#     if p.quantity_on_hand == 0:
#         print("this one is done", p.name)
#     if "used" in p.barcode or "expired" in p.barcode:
#         print(p, p.name)
#         p.delete()
#         print("deleted", p.name)


# WORKS!!!! alh--for strings of YYYY-mm-dd format
# p = Product.objects.filter(
#     Q(reference_id__startswith="H74939")
#     & Q(ref_id_expiry_date__icontains=convert_date_to_search_format(search).date())
# )

# now works for strings of dates in mm-dd-yyyy
# p = Product.objects.filter(
#     Q(reference_id__startswith="H74939")
#     & Q(ref_id_expiry_date__icontains=test_format(search2).date())
# )


# print(p)

# for ele in p:
#     print(ele.name)
#     print(ele.ref_id_expiry_date)
# print(len(p))


# with open(file_barcodes, "r") as f:
#     csv1 = csv.DictReader(f)
#     for row in csv1:
#         expiry = row["expiry_date"]
#         ref = row["reference_id"]
#         p = Product.objects.filter(
#             Q(reference_id__icontains=ref)
#             & Q(ref_id_expiry_date__icontains=test_format(expiry).date())
#         )
#         if p.exists():
#             print(p)

#         else:
#             print("it doesnt exist bro")
#             break

# with open(file_barcodes_latest, "r", encoding="utf-8", newline="") as f:
#     reader = csv.DictReader(f)
#     for index, row in enumerate(reader, start=1):
#         for row in reader:
#             expiry = row["expiry_date"].strip()
#             ref = row["reference_id"].strip()
#             company = row["company"].strip()
#             product = row["product"].strip()
#             ref_id_expiry_date = f"{ref}***{expiry}"
#             size = row["size"].strip()
#             quantity = row["quantity"].strip()
#             barcode = row["barcode"].strip()
#             row_number = index
#             # print("---------------------here >>", index)
#             obj, created = Product.objects.update_or_create(
#                 expiry_date__icontains=test_format(expiry).date(),
#                 reference_id__icontains=ref,
#                 defaults={
#                     "name": product,
#                     "reference_id": ref,
#                     "expiry_date": test_format(expiry),
#                     "size": size,
#                     "barcode": barcode,
#                     "employee": User.objects.get(id=1),
#                     "vendor": Vendor.objects.get(name__icontains=company),
#                     "quantity_on_hand": quantity,
#                 },
#             )
#             if created:
#                 print(f"{obj.name} created.")
#             else:
#                 print(f"{obj.name} updated.")

# print(row_number)
# print(row)
# obj, created = Product.objects.update_or_create(reference_id=ref, expiry_date=)
# test_ref = "H74939200124020"
# test_exp = "02-07-2027"
# check = Product.objects.filter(
#     Q(expiry_date__icontains=test_format(test_exp).date())
#     & Q(reference_id__icontains=test_ref),
# )
# if check.first():
#     print("index matches!")
#     print(check.first().name)
#     break

print("here")


test_ref = "H74939200124020"
test_exp = "02-07-2027"
check = Product.objects.filter(
    Q(expiry_date__icontains=test_format(test_exp).date())
    & Q(reference_id__icontains=test_ref),
)
if check.first():
    print("index matches!")
    print(check.first().name)


file_barcodes_2 = r"C:\Users\omniv\OneDrive\Documents\pydb4\pydb\inventory-barcodes-current-07052023.csv"


# with open(file_barcodes_2, "r", encoding="utf-8", newline="") as f:
#     reader = csv.DictReader(f)
#     for index, row in enumerate(reader, start=1):
#         for row in reader:
#             expiry = row["expiry_date"].strip()
#             ref = row["reference_id"].strip()
#             company = row["company"].strip()
#             product = row["product"].strip()
#             ref_id_expiry_date = f"{ref}***{expiry}"
#             size = row["size"].strip()
#             quantity = row["quantity"].strip()
#             barcode = row["barcode"].strip()
#             row_number = index
#             print("---------------------here >>", index)
#             p = Product.objects.filter(
#                 expiry_date=test_format(expiry).date(), reference_id__icontains=ref
#             )
#             if not p.exists():
#                 print(p.first().name)

# break
# obj, created = Product.objects.update_or_create(
#     expiry_date__icontains=test_format(expiry).date(),
#     reference_id__icontains=ref,
#     defaults={
#         "name": product,
#         "reference_id": ref,
#         "expiry_date": test_format(expiry),
#         "size": size,
#         "barcode": barcode,
#         "employee": User.objects.get(id=1),
#         "vendor": Vendor.objects.get(name__icontains=company),
#         "quantity_on_hand": quantity,
#     },
# )

# if 'used' or 'expired' or 'present' in barcodes or quantity


# p = Product.objects.filter(
#     Q(ref_id_expiry_date__icontains="H7493929")
#     & Q(ref_id_expiry_date__icontains="2023-10-09")
# )
# print(p)


# for e in w:
#     if e.ref_id_expiry_date == "":
#         print(e.name)

# with open(file, "r") as file1, open(file_barcodes, "r") as file2:
#     data1 = csv.DictReader(file1)
#     data2 = csv.DictReader(file2)
#     # for r1, r2 in zip(data1, data2):
#     if (
#         r1["reference_id"] == r2["reference_id"]
#         and r1["expiry_date"] == r2["expiry_date"]
#     ):
#         print(r1, r2)


# diff = compare(
#     load_csv(open(file), key="ref_id_expiry_date"),
#     load_csv(open(file_barcodes), key="ref_id_expiry_date"),
# )

# # if diff:
# #     print(diff)


# with open(file, "r") as file1, open(file_barcodes, "r") as file2:
#     # Load the CSV data into dictionaries
#     # data1 = load_csv(file1)
#     # data2 = load_csv(file2)

#     data1 = csv.DictReader(file1)
#     data2 = csv.DictReader(file2)

#     ignored_column = "column_name"
#     data1_modified = {}
#     data2_modified = {}

#     # Create modified dictionaries for each row
#     for row in data1:
#         modified_row = {
#             key: value for key, value in row.items() if key != ignored_column
#         }
#         data1_modified[row["ref_id_expiry_date"]] = modified_row

#     for row in data2:
#         modified_row = {
#             key: value for key, value in row.items() if key != ignored_column
#         }
#         data2_modified[row["ref_id_expiry_date"]] = modified_row

#     # Perform the comparison using csv-diff module
#     diff = compare(data1_modified, data2_modified)

#     # Process the comparison results
#     for change in diff:
#         print(change)
#         print(type(change))


# Open the two CSV files and store their rows in two separate lists
# with open(file) as f1, open(file_barcodes) as f2, open("updated.csv", "a") as f:
# csv1 = list(csv.reader(f1))
# csv2 = list(csv.reader(f2))
# csv1 = csv.DictReader(f1)
# csv2 = csv.DictReader(f2)
#     csv3 = csv.DictReader(f)
#     count = 0
#     for row1, row2 in zip(csv1, csv2):
#         if row1["ref_id_expiry_date"] == row2["ref_id_expiry_date"]:
#             print(row2)
#         else:
#             count += 1
#             # print("difference here:")
#             # print(row1, row2)

# print(count)

# # Iterate over the rows of both files simultaneously using zip()
# for i, (row1, row2) in enumerate(zip(csv1, csv2)):
#     # For each row, compare the values of each cell and store the differences in a list for further analysis
#     diff = [i, []]
#     for j, (cell1, cell2) in enumerate(zip(row1, row2)):
#         if cell1 != cell2:
#             diff[1].append(j)
#     # Once all the rows have been compared, analyze the differences list to identify the discrepancies between the files
#     if diff[1]:
#         print(f"Difference found in row {diff[0]}: cells {diff[1]}")
