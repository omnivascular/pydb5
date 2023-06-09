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

# Choose vendor
# vendor = Vendor.objects.get(id=1)
# vendor = Vendor.objects.get(id=2)
# vendor = Vendor.objects.get(id=3)
# vendor = Vendor.objects.get(id=4)
vendor = Vendor.objects.get(id=5)
# vendor = Vendor.objects.get(id=6)

# Choose starting digits/letters common to a set of products and their vendor as filter params

# done
# products = Product.objects.filter(Q(reference_id__startswith="AB35W") & Q(vendor_id=3))
# products = Product.objects.filter(Q(reference_id__startswith="A14BX") & Q(vendor_id=3))
# products = Product.objects.filter(Q(reference_id__startswith="RSS") & Q(vendor_id=5))
# products = Product.objects.filter(
#     Q(reference_id__startswith="A14BX") & Q(vendor_id=3) & Q(size__startswith="4.0mm")
# )
# products = Product.objects.filter(Q(reference_id__startswith="H7493") & Q(vendor_id=1))
# prod = Product.objects.filter(name__icontains="Opticross")
# prod = Product.objects.filter(Q(name__icontains="Jetstream") & Q(vendor_id=1))
# prod = Product.objects.filter(Q(name__icontains="Perclose Proglide") & Q(vendor_id=2))
# prod = Product.objects.filter(Q(name__icontains="Protege GPS") & Q(vendor_id=3))
prod = Product.objects.filter(Q(reference_id__startswith="PRB35-") & Q(vendor_id=3))
# prod = Product.objects.filter(Q(name__icontains="?") & Q(vendor_id=?))
# prod = Product.objects.filter(Q(name__icontains="?") & Q(vendor_id=?))
# prod = Product.objects.filter(Q(name__icontains="?") & Q(vendor_id=?))
# prod = Product.objects.filter(Q(name__icontains="?") & Q(vendor_id=?))


print(prod)

for x in prod:
    print(x.size)
    # test = [a, b, c, d, e] = x.size.split("-")
    # # print(test)
    # test = [e.strip() for e in test]
    # a = a + "mm"
    # b = b + "mm"
    # c = c + "cm"
    # d = d + "inch"
    # e = e + "r"
    # test = [a, b, c, d, e]
    # # print(test)
    # test2 = "-".join(test)
    # # print(test2)
    # x.size = test2
    # x.save(update_fields=["size"])
    # print("updated")

    # test = x.size.strip().replace("F", "Fr").replace(" (2.0 mm)", "-2.0mm")
    # print(test)
    # # x.size = test
    # # x.save(update_fields=["size"])
    # print("updated")

    # test = [a, b] = x.size.strip().split(" ")
    # a = a.strip() + "r"
    # test = [a, b]
    # test2 = "-".join(test)
    # print(test2)

    # test = [a, b, c] = x.size.split("-")
    # a = a.strip().replace("2.1", "2.1mm").replace("3.0", "3.0mm")
    # b = b.strip() + "r"
    # c = c.strip() + "cm"
    # test = [a, b, c]
    # # print(test)
    # test2 = "-".join(test)
    # print(test2)
    # x.size = test2
    # x.save(update_fields=["size"])
    # print("updated for jetstream item")
    # for y in products:
    #     if x == y:
    #         print("match")
    #         print(x.size)
    #         test = [a, b] = x.size.split("-")
    #         a = a + "r"
    #         b = b + "cm"
    #         test = [a, b]
    #         test2 = "-".join(test)
    #         print(test2)
    # x.size = test2
    # x.save(update_fields=["size"])
    # print("done saved")

# print(products)
# for p in products:
#     print(p.size)
# test = p.size.split("-")
# if len(test) == 2:
#     test = [a, b] = p.size.split("-")
#     a = a + "mm"
#     b = b + "mm"
#     test2 = "-".join(test)
#     # print(test2)
# p.size = test2
# p.save(update_fields=["size"])
# print("updated value")
# else:
#     test = [a, b, c] = p.size.split("-")
#     a = a + "mm"
#     b = b + "mm"
#     c = c + "cm"
#     test = [a, b, c]
#     test2 = "-".join(test)
# print(test2)
# p.size = test2
# p.save(update_fields=["size"])
# print("updated value")

# test2 = "-".join(test)
# print(test2)

# test = [a, b, c, d] = p.size.split("-")
# a = a + "mm"
# b = b + "mm"
# c = c + "cm"
# d = d + "r"
# test = [a, b, c, d]
# # print(test)
# test2 = "-".join(test)
# print(test2)
# p.size = test2
# p.save(update_fields=["size"])
# print("completed update")
# p.size = p.size.replace("Fr", ".0Fr")
# p.save(update_fields=["size"])
# print("saved")

# t = input("yes or no to update?")
# if t == "yes":
#     # p.size = p.size.replace("4mm", "4.0mm")
#     # p.save(update_fields=["size"])
#     continue
# else:
#     continue

# products = Product.objects.filter(Q(reference_id__startswith="RSS401") & Q(vendor_id=5))
# products = Product.objects.filter(Q(reference_id__startswith="AB35W") & Q(vendor_id=3))
# products = Product.objects.filter(Q(reference_id__startswith="AB35W") & Q(vendor_id=3))
# products = Product.objects.filter(Q(reference_id__startswith="AB35W") & Q(vendor_id=3))
# products = Product.objects.filter(Q(reference_id__startswith="AB35W") & Q(vendor_id=3))
# products = Product.objects.filter(Q(reference_id__startswith="AB35W") & Q(vendor_id=3))

# Empty list for holding
# updated = []

# # Isolate each set of size values from within each product from queryset of products
# check = [p.size.split("-") for p in products]
# check2 = [q[0].replace("mm", ".0mm") for q in check if len(q[0]) == 3]


# print(check2)

# print(check)

u3 = []
# for e in check:
#     # Verify length of each field for item is same, edit below per item set
#     print(len(e))
#     t = []
#     print(check.index(e))
# if len(e) == 4 and len(e[0]) == 3:
#     print(e)
# print(check.index(e))

# r = ["-".join(p) for p in u3]

# products[n].size = r[n]
# products[n].save(update_fields=["size"])
# t.append(e)
# u3.append(t)
# print(u3)

# if len(e) == 4:
#     t.append(e[0].strip() + "mm")
#     t.append(e[1].strip() + "mm")
#     t.append(e[2].strip() + "cm")
#     t.append(e[3].strip().replace("F", ".0Fr"))
#     u3.append(t)
# elif len(e) == 5:
#     t.append(e[0].strip() + "mm")
#     t.append(e[1].strip().replace(")", "mm)"))
#     t.append(e[2].strip() + "mm")
#     t.append(e[3].strip() + "cm")
#     t.append(e[4].strip().replace("F", ".0Fr"))
#     u3.append(t)

# t.append(e[0].strip() + ".0mm")
# t.append(e[1].strip() + "mm")
# t.append(e[2].strip() + "cm")
# t.append(e[3].strip().replace("F", ".0Fr"))
# u3.append(t)


# print(u3)
# # Re-assembling strings with dash
# r = ["-".join(p) for p in u3]

# print(r)
# print(type(r[0]))

# # Match up lengths first, then isolate specific size field and update after confirm
# if len(r) == products.count():
#     for n in range(0, len(r)):
#         print(products[n].size.strip())
#         print(r[n])
# products[n].size = r[n]
# products[n].save(update_fields=["size"])
