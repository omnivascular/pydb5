import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "pydb.settings")
django.setup()

import csv
from datetime import datetime
from dateutil.parser import parse
from pydb4.models import Vendor, Product
from django.db.models import Q
import json

# from .pydb import settings

# settings.configure()

file = r"C:\Users\omniv\OneDrive\Documents\pydb4\pydb\inventory.csv"

vendor_details = {
    1: ["Boston Scientific", "BSCI"],
    2: ["Abbott", "ABBT"],
    3: ["ev3/Covidien/Medtronic", "MTRNC"],
    4: ["COOK Medical", "COOK"],
    5: ["Terumo", "TRMO"],
    6: ["Coulmed", "COULMD"],
}

vendor = Vendor.objects.get(id=3)

products = Product.objects.filter(Q(reference_id__startswith="AB35W") & Q(vendor_id=3))

print(vendor.name)

updated = []
check = [p.size.split("-") for p in products]


# for e in check:
#     print(len(e))
#     t = []
#     t.append(e[0].strip() + "mm")
#     t.append(e[1].strip() + "mm")
#     t.append(e[2].strip() + "cm")
#     t.append(e[3].strip() + "r")
#     updated.append(t)


# print(updated)
# for u in updated:
#     u2 = "-".join(u)
#     print(u2)

# print(len(products))

# val = json.dumps(updated)

# print(type(val))
# val2 = json.loads(val)
# print(type(val2))

print("----------------------------------------------------------------")

u3 = []
for e in check:
    # print(len(e)) #just for verifying length of each size field
    t = []
    t.append(e[0].strip() + ".0mm")
    t.append(e[1].strip() + "mm")
    t.append(e[2].strip() + "cm")
    t.append(e[3].strip().replace("F", ".0Fr"))
    # print(t)
    u3.append(t)
r = ["-".join(p) for p in u3]
print(r)
print(type(r[0]))

if len(r) == products.count():
    print("true")
print("----------------------------------------------------------------")

print(type(products))
if len(r) == products.count():
    for n in range(0, len(r)):
        print(products[n].size.strip())
        print(r[n])
        # products[n].size = r[n]
        # products[n].save(update_fields=["size"])

    # for ele in r:
    #     # print(r.index(ele))
    #     for p in products:
    #         print(f"This is old value: {p.size}, to be replaced with new value: {ele}.")

    # p.size = ele
    # p.save(update_fields=['size'])
