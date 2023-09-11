from django.urls import path, re_path, include
from django.contrib import admin
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    path("products", views.all_products, name="all-products"),
    path("vendors", views.all_vendors, name="all-vendors"),
    path("procedures", views.all_procedures, name="all-procedures"),
    path(
        "vendors/<int:vendor_id>/",
        views.all_vendor_products,
        name="all-vendor-products",
    ),
    path(
        "product/<int:item_id>/",
        views.product_detail,
        name="product_detail",
    ),
    # re_path(r"^ajax_calls/search/$", views.autocompleteModel, name="autocomplete"),
    path("product_search", views.product_search, name="product_search"),
    path("update_product/<int:product_id>/", views.update_product, name="update_product"),
    path('add_product/', views.add_product, name='add_product'),
    path('home', views.home, name='home'),
    path('expiring_products/', views.expiry_check_all_products, name='expiry_check_all_products'),
    path('procedure/', views.procedure, name='procedure'),
]

admin.site.header = "Omni Vascular Inventory Management"
admin.site.site_title = "Browser Title"
admin.site.index_title = "Welcome to Omni IT!"
