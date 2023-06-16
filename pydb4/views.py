from django.shortcuts import render, redirect
from .models import Product, Vendor, vendor_details
from django.db.models import Q
from datetime import datetime
import json
from .forms import ProductForm
from .forms import UneditableProductForm
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.contrib import messages
from calendar import HTMLCalendar
import calendar
from django.core import serializers


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


def product_detail(request, item_id):
    product = Product.objects.filter(id__exact=item_id)

    return render(request, "pydb4/product_detail.html", {"product": product})

def product_search(request):
    multiple = False
    if request.method == "POST":
        searched = request.POST["searched"]
        print("type of searched is:", type(searched))
        if "-" in searched:
            multiple = True
            products = searched.split("-")
            print("type of products is:", type(products))
            queries = [Q(name__icontains=term) | Q(size__icontains=term) | Q(reference_id__icontains=term) for term in products]
            search_query = construct_search_query(queries)
            results = Product.objects.filter(search_query).order_by('expiry_date')
            print("type of results is:", type(results))
            return render(request, "pydb4/product_search.html", {"searched": products, "products": results, "multiple": multiple})
        else:    
            products = Product.objects.filter(Q(name__icontains=searched)|Q(size__icontains=searched)|Q(reference_id__icontains=searched)).order_by('expiry_date')
            
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


def update_product(request, product_id):
    product = Product.objects.get(pk=product_id)
    readonly_fields = ['name', 'reference_id', 'size', 'expiry_date', 'vendor']
    # readonly_fields = ['name', 'reference_id', 'expiry_date', 'vendor']
    if request.method == "POST":
        form = ProductForm(request.POST, instance=product, readonly_fields=readonly_fields)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('product_detail', args=[product_id]))
        else:
            messages.error(request, "Form unable to be saved, please contact IT admin.")
    else:
        form = ProductForm(instance=product, readonly_fields=readonly_fields)

    return render(request, 'pydb4/update_product.html', {"product": product, "form": form, "readonly_fields": readonly_fields})


def expiry_check_all_products(request):
    products = Product.objects.all()
    results = []
    for x in products:
        datecheck = x.days_until_expiry
        if datecheck.years == 0 and datecheck.months < 3:
            print(x.name, x.size, x.expiry_date.date())
            results.append(x)
    return render(request, 'pydb4/expiry_check.html', {"results": results})

def add_product(request):
    submitted = False
    if request.method == "POST":
        form = ProductForm(request.POST)
        if form.is_valid():
            # venue = form.save(commit=False)
            # venue.owner = request.user.id # logged in user
            # venue.save()
            product = form.save()
            submitted = True
            messages.success(request, "Product added successfully, thank you!")
            # return  render('/add_product?submitted=True')
            return render(request, "pydb4/product_detail.html", {"product": product, 'submitted': submitted})   
    else:
        form = ProductForm()
        if 'submitted' in request.GET:
            submitted = True
        return render(request, 'pydb4/add_product.html', {'form':form, 'submitted':submitted})

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




