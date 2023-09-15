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
