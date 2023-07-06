from django.contrib import admin
from .models import Product, Vendor, AuditLog, Procedure

# Register your models here.
# admin.site.register(Product)
# admin.site.register(Vendor)
admin.site.register(AuditLog)
admin.site.register(Procedure)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
	list_display = ('name', 'reference_id', 'expiry_date', 'is_purchased', 'size', 'barcode', 'quantity_on_hand', 'vendor')
	list_filter = ('expiry_date', )
	fields = (('name', 'size', 'quantity_on_hand', 'expiry_date'), ('vendor', 'is_purchased', 'barcode'), 'ref_id_expiry_date')
	ordering = ('name',)
	search_fields = ('name', 'reference_id')


@admin.register(Vendor)
class EventAdmin(admin.ModelAdmin):
	list_display = ('id', 'name', 'abbrev')
	ordering = ('id',)