from django.shortcuts import render, redirect
from .models import Product, Vendor, vendor_details, AuditLog, Procedure
from django.contrib.auth.models import User
from django.db.models import Q
from datetime import datetime
import json
from .forms import ProductForm, ProcedureForm
from .forms import UneditableProductForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, HttpResponseNotAllowed
from django.urls import reverse
from django.contrib import messages
from calendar import HTMLCalendar
import calendar
from django.core import serializers
from django.views.decorators.cache import cache_control
import traceback
import qrcode as qr
import re


def construct_search_query_alternate(queries):
    if len(queries) == 1:
        return queries[0]  # Base case: return the single query

    # Recursive case: combine the first query with the result of the recursive call
    # return Q(queries[0]) | construct_search_query(queries[1:])
    return Q(queries[0]) & construct_search_query(queries[1:])

def construct_search_query(queries):
    if len(queries) == 1:
        return queries[0]  # Base case: return the single query

    # Recursive case: combine the first query with the result of the recursive call
    return Q(queries[0]) | construct_search_query(queries[1:])


# Create your views here.
def all_products(request):
    product_list = Product.objects.all()
    return render(request, "pydb4/product_list.html", {"product_list": product_list})


def all_vendors(request):
    vendor_list = Vendor.objects.all()
    return render(
        request,
        "pydb4/vendor_list.html",
        {"vendor_list": vendor_list},
    )

def all_procedures(request):
    procedure_list = Procedure.objects.all()
    return render(
        request,
        "pydb4/procedure_list.html",
        {"procedure_list": procedure_list},
    )

def all_vendor_products(request, vendor_id):
    print(request.META.get('HTTP_X_REQUESTED_WITH'))
    if request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest':
        products = Product.objects.filter(vendor_id=vendor_id)
        vendor = Vendor.objects.get(id=vendor_id)

        # product_data = serializers.serialize('json', products)
        product_data = [{"name": p.name} for p in products]
        vendor_data = {
            'id': vendor.id,
            'name': vendor.name,
            # Include any other desired fields
        }

        response_data = {
            'products': product_data,
            'vendor': vendor_data,
        }
        # Convert the response data to JSON
        # response_json = json.dumps(response_data)
        # print(response_json)
        return JsonResponse(response_data, safe=False)
    else:
        products = Product.objects.filter(vendor_id=vendor_id)
        vendor = Vendor.objects.get(id=vendor_id)
        return render(
            request,
            "pydb4/vendor_products.html",
            {"products": products, "vendor": vendor},
        )


# def all_vendor_products(request, vendor_id):
#     products = Product.objects.filter(vendor_id=vendor_id)
#     vendor = Vendor.objects.get(id=vendor_id)
#     return render(
#         request,
#         "pydb4/vendor_products.html",
#         {"products": products, "vendor": vendor},
#     )

# @cache_control(no_cache=True, must_revalidate=True)
def product_detail(request, item_id):
    # product = Product.objects.filter(id__exact=item_id)
    product = Product.objects.get(id=item_id)
    try:
        auditor = AuditLog.objects.get(id=product.employee.id)
        modifier = User.objects.get(id=auditor.omni_employee)
        img = qr.make(product.barcode)
        img.save(f'{item_id}-QR-code.png')
    except AttributeError:
        print('this one needs admin as default auditor')
        auditor = AuditLog.objects.get(id=1)
        modifier = User.objects.get(id=auditor.omni_employee)
        img = ''
    # modifier = ''
    print(product, auditor, modifier)
    print('here at line 101, in views.py')
    records = AuditLog.objects.filter(Q(object_id=item_id) & Q(field_name="quantity_on_hand")).order_by('modified_date')
    # for r in records:
    #     print(r.content_object)
    #     print(r.object_id)
    #     print(r.field_name)
    return render(request, "pydb4/product_detail.html", {"product": product, "records": records, "modifier": modifier, "pic": img})

# @cache_control(no_cache=True, must_revalidate=True)
def product_search(request):
    multiple = ''
    if request.method == "POST":
        searched = request.POST["searched"]
        print("type of searched is:", type(searched))
        if "," in searched and ';' not in searched:
            multiple = ','
            products = [s.strip().lower() for s in searched.split(",")]
            print("type of products is:", type(products))
            queries = [Q(name__icontains=term) | Q(size__icontains=term) | Q(reference_id__icontains=term) | Q(barcode__icontains=term) for term in products]
            search_query = construct_search_query(queries)
            results = Product.objects.filter(search_query).order_by('expiry_date')
            print("type of results is:", type(results))
            return render(request, "pydb4/product_search.html", {"searched": products, "products": results, "multiple": multiple})
        elif ";" in searched and ',' not in searched:
            multiple = ';'
            products = [s.strip().lower() for s in searched.split(";")]
            queries = [Q(name__icontains=term) | Q(size__icontains=term) | Q(reference_id__icontains=term) for term in products]
            search_query = construct_search_query_alternate(queries)
            results = Product.objects.filter(search_query).order_by('expiry_date')
            print("type of results is:", type(results))
            return render(request, "pydb4/product_search.html", {"searched": products, "products": results, "multiple": multiple})
        else:    
            products = Product.objects.filter(Q(name__icontains=searched)|Q(size__icontains=searched)|Q(reference_id__icontains=searched) | Q(barcode__icontains=searched)).order_by('expiry_date')
            
            messages.success(request, "Nice search, it worked!", extra_tags='search')
            return render(
                request,
                "pydb4/product_search.html",
                {
                    "searched": searched,
                    "products": products,
                    "multiple": multiple,
                },
            )
    else:
        return render(request, "pydb4/product_list.html", {})

# @cache_control(no_cache=True, must_revalidate=True)
def update_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    updated = False
    readonly_fields = ['name', 'reference_id', 'size', 'expiry_date', 'vendor']
    # readonly_fields = ['name', 'reference_id', 'expiry_date', 'vendor']
    if request.method == "POST":
        print(request)
        form = ProductForm(request.POST, instance=product, readonly_fields=readonly_fields)

        if form.is_valid():
            result = form.save(commit=False)
            try:
                result.employee = User.objects.get(pk=request.user.id) #logged in user
            except error as e:
                print('error here')
                traceback.print_exc()
            print('For updating product, User ID: ', request.user.id)
            result.save()
            updated = True
            redirect_url = reverse('product_detail', args=[product_id])
            if updated:
                redirect_url += '?redirect_flag=true'
            print(result.employee.username)
            redirect_url += f'?user={result.employee.username}'
            return HttpResponseRedirect(redirect_url)
        else:
            messages.error(request, "Form unable to be saved, please contact IT admin.")
    else:
        form = ProductForm(instance=product, readonly_fields=readonly_fields)

    return render(request, 'pydb4/update_product.html', {"product": product, "form": form, "readonly_fields": readonly_fields})

# @cache_control(no_cache=True, must_revalidate=True)
def expiry_check_products_by_month(request, month_number):
    products = Product.objects.all()
    results = []
    for x in products:
        datecheck = x.days_until_expiry
        if month_number == 1:
            if datecheck.years == 0 and datecheck.months <= 1:
                print(x.name, x.size, x.expiry_date.date())
                results.append(x)        
        if month_number == 3:
            if datecheck.years == 0 and datecheck.months <= 3:
                print(x.name, x.size, x.expiry_date.date())
                results.append(x)
        if month_number == 6:
            if datecheck.years == 0 and datecheck.months <= 6:
                print(x.name, x.size, x.expiry_date.date())
                results.append(x)
    return render(request, 'pydb4/expiry_check.html', {"results": results, "month_number": month_number})

# def verify_products(request):
#     submitted = False
#     if request.method == "POST":
#         print('got to here, line 201 in views.py')
#         pattern = r"\r\n|\n|,"  # Regular expression pattern to match "\r\n" or "\n"
#         barcodes_used = re.split(pattern, request.POST.get('products_used', ''))
#         queries = [Q(barcode__icontains=term) for term in barcodes_used if term != '']
#         search_query = construct_search_query(queries)
#         results = Product.objects.filter(search_query).order_by('expiry_date')

#     print('got to here, line 209 in views.py')
#     return HttpResponseNotAllowed(['POST'])

def procedure(request):
    submitted = False
    if request.method == "POST":
        print("POST here")
        form = ProcedureForm(request.POST)
        pattern = r"\r\n|\n|,"  # Regular expression pattern to match "\r\n" or "\n"
        barcodes_used = re.split(pattern, request.POST.get('products_used'))
        # products = list(set([Product.objects.filter(barcode__exact=b) for b in barcodes_used]))
        isolated_barcodes = set()
        uniques = [x for x in barcodes_used if x not in isolated_barcodes and not isolated_barcodes.add(x)]  
        duplicates = [x for x in barcodes_used]

        barcodes_exist = all(list(set([Product.objects.filter(barcode__exact=b).exists() for b in barcodes_used if b != ''])))
        # if barcodes_exist:
        # need to add logic for item barcodes that don't exist yet (could then show popup of add_product page)
        queries = [Q(barcode__icontains=term) for term in barcodes_used if term != '']
        search_query = construct_search_query(queries)
        results = Product.objects.filter(search_query).order_by('expiry_date')
        print('length of results queryset:')
        print(len(results))
        print('.items: ', request.POST.items)
        print('original products used field: ', barcodes_used)
        # print('processed products used field', products_used)
        print('patient: ', request.POST.get('patient'))
        print('procedure: ', request.POST.get('procedure'))
        if form.is_valid():
            print(type(form))
            print('it is valid')
            procedure = form.save(commit=False)
            try: 
                print('For adding procedure, User ID: ', request.user.id)
                procedure.employee = User.objects.get(pk=request.user.id) #logged in user
                procedure.products_used = barcodes_used
                if results:
                    print('showing len, type, and results object itself:')
                    print(len(results), type(results), results)
                    for r in results:
                        print(f"Removing one of this item from inventory: {r.name}-{r.expiry_date}")
                        print(f"Old quant: {r.quantity_on_hand}")
                        r.quantity_on_hand -= 1
                        print(f"New quant: {r.quantity_on_hand}")
                        r.save()
                        print(f'saved {r}')
                # product.employee = request.user.id
                procedure.save()
            except:
                traceback.print_exc()
            submitted = True
            return render(request, 'pydb4/procedure_detail.html', {'procedure': procedure, 'submitted': submitted, 'barcodes': barcodes_used, 'products': results})
        else:
            print(procedure.is_valid())
            print(procedure.errors)
            print('sorry form not correct, try again.')
            return render(request, 'pydb4/procedure_event.html', {'procedure': procedure})    
    else:
        form = ProcedureForm()
        print('GET here')
        return render(request, 'pydb4/procedure_event.html', {'form': form, 'submitted': submitted})


# @cache_control(no_cache=True, must_revalidate=True)
def add_product(request):
    submitted = False
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # venue = form.save(commit=False)
            # venue.owner = request.user.id # logged in user
            # venue.save()
            product = form.save(commit=False)
            try: 
                print('For adding product, User ID: ', request.user.id)
                product.employee = User.objects.get(pk=request.user.id) #logged in user
                # product.employee = request.user.id
                product.save()
            except:
                traceback.print_exc()
            submitted = True
            messages.success(request, "Product added successfully.")
            # return  render('/add_product?submitted=True')
            print(type(product))
            return render(request, "pydb4/product_detail.html", {"product": product, 'submitted': submitted})   
    else:
        form = ProductForm()
        if 'submitted' in request.GET:
            submitted = True
        return render(request, 'pydb4/add_product.html', {'form':form, 'submitted':submitted})

# @cache_control(no_cache=True, must_revalidate=True)
def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Guest"
    month = month.capitalize()
    # Convert month from name to number
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    # create a calendar
    cal = HTMLCalendar().formatmonth(
        year, 
        month_number)
    # Get current year
    now = datetime.now()
    current_year = now.year
    current_day = now.day
    
    # Query the Events Model For Dates
    # event_list = Event.objects.filter(
    #     event_date__year = year,
    #     event_date__month = month_number
    #     )

    # Get current time
    time = now.strftime('%I:%M %p')
    return render(request, 
        'pydb4/home.html', {
        "name": name,
        "year": year,
        "month": month,
        "month_number": month_number,
        "cal": cal,
        "current_day": current_day,
        "current_year": current_year,
        "time":time,
        # "event_list": event_list,
        })



# def update_event(request, event_id):
#     event = Event.objects.get(pk=event_id)
#     form = EventForm(request.POST or None, instance=event)
#     if form.is_valid():
#         form.save()
#         return redirect('list-events')

#     return render(request, 'events/update_event.html', 
#         {'event': event,
#         'form':form})


# def autocompleteModel(request):
#     if request.is_ajax():
#         q = request.GET.get("term", "").capitalize()
#         search_qs = Product.objects.filter(name__startswith=q)
#         results = []
#         # print q
#         for r in search_qs:
#             results.append(r.name)
#         data = json.dumps(results)
#     else:
#         data = "fail"
#     mimetype = "application/json"
#     return HttpResponse(data, mimetype)




