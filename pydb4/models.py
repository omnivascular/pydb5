from django.db import models
# from django.template.defaultfilters import date
from django.core.exceptions import ValidationError
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import User
import json


placeholder = ''

# # to be added when URLs fully ready
# vendor_details = {
#     1: ["Boston Scientific", "BSCI", f"https://www.bostonscientific.com/en-US/search.html#q={placeholder}"],
#     2: ["Abbott", "ABBT", f"https://www.abbott.com/searchresult.html?q={placeholder}&s=true"],
#     3: ["ev3/Covidien/Medtronic", "MTRNC", f"https://www.medtronic.com/us-en/search-results.html#q={placeholder}"],
#     4: ["COOK Medical", "COOK", f"https://www.cookmedical.com/search/?#stq={placeholder}"],
#     5: ["Terumo", "TRMO"],
#     6: ["Coulmed", "COULMD"],
# }


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

"""
new vendor to add for venovo venous stent system:
BD, Becton, Dickinson and Company

url- https://www.bd.com/en-us/products-and-solutions/products?heroSearchValue={placeholder}&publishedAt=all-dates
"""

vendor_choices = [
    (str(key), f"{value[0]} ({value[1]})") for key, value in vendor_details.items()
]


def listing_vendors():
    print("Vendor ID  -  Vendor Name  -  Vendor Abbreviation")
    for key, value in vendor_details.items():
        print(f"{key}  -  {value[0]}  -  {value[1]}")




class Vendor(models.Model):
    id = models.CharField(
        primary_key=True, unique=True, max_length=2, choices=vendor_choices
    )
    name = models.CharField(max_length=200)
    abbrev = models.CharField(max_length=50)
    # url = models.URLField(max_length=200)

    def save(self, *args, **kwargs):
        listing_vendors()
        if self.id in vendor_details:
            self.name, self.abbrev = vendor_details[self.id]
        else:
            raise ValidationError(
                _("Invalid vendor ID provided, must be a vendor from records.")
            )
        super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

# class OmniUser(models.Model):
#     first_name = models.CharField(max_length=60)
#     last_name = models.CharField(max_length=60)
#     email = models.EmailField('User Email')

#     def __str__(self):
#         return self.first_name + ' ' + self.last_name


class AuditLog(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    field_name = models.CharField(max_length=255)
    old_value = models.CharField(max_length=255)
    new_value = models.CharField(max_length=255)
    modified_date = models.DateTimeField()
    omni_employee = models.PositiveIntegerField("Employee last edited", blank=False,default=1)
 
    def get_quantity_field(self):
        return f"Quantity on hand" if 'quantity_on_hand' in self.field_name else "Not yet defined field name" 

    # p = Product.objects.filter(pk=1)

    # def __str__(self) -> str:
    #     return f"Value changed: {self.get_field_name()}, Old value: {self.old_value}, New value: {self.new_value}, Date changed: {self.modified_date}"

class Product(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        unique=True,
        serialize=False,
        verbose_name="ID",
    )
    name = models.CharField(max_length=300)
    reference_id = models.CharField(max_length=100)
    expiry_date = models.DateTimeField(auto_now=False, auto_now_add=False)
    ref_id_expiry_date = models.CharField(max_length=250, unique=True)
    # barcode_ref_id_expiry_date = models.CharField(max_length=250, unique=True, default="N/A")
    is_purchased = models.BooleanField(default=True)
    size = models.CharField(max_length=60, default="N/A", blank=True)
    barcode = models.CharField(max_length=300, default="N/A", blank=True, null=True)
    quantity_on_hand = models.PositiveIntegerField(default=1)
    quantity_on_order = models.PositiveIntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)
    employee = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.ref_id_expiry_date = self.generate_ref_id_expiry_field()
        # self.barcode_ref_id_expiry_date = self.generate_barcode_ref_id_expiry_field()
        if self.pk:
            # Retrieve the existing object from the database
            old_instance = Product.objects.get(pk=self.pk)

            # Compare the fields and record changes
            for field in self._meta.fields:
                field_name = field.name
                old_value = getattr(old_instance, field_name)
                new_value = getattr(self, field_name)

                if old_value != new_value:
                    # Create an audit log entry for each changed field
                    # user = User.objects.get(id=)
                    AuditLog.objects.create(
                        content_object=self,
                        field_name=field_name,
                        old_value=str(old_value),
                        new_value=str(new_value),
                        modified_date=datetime.now(),
                        omni_employee=self.employee.id
                    )

        super().save(*args, **kwargs)

    def generate_ref_id_expiry_field(self):
        return f"{self.reference_id}***{self.expiry_date.date()}"

    # def generate_barcode_ref_id_expiry_field(self):
    #     return f"{self.barcode}***{self.reference_id}***{self.expiry_date.date()}"

    class Meta:
        unique_together = ("reference_id", "expiry_date", "barcode")
        # ordering = ["name"]
        ordering = ["expiry_date"]
        indexes = [models.Index(fields=["ref_id_expiry_date", "name"])]

    def __str__(self) -> str:
        return self.name

    @property
    def days_until_expiry(self):
        today = date.today()
        # expiry_converted = [int(n) for n in self.expiry_date.split("-")]

        time_remaining = relativedelta(self.expiry_date.date(), today)
        # days_remaining = relativedelta(datetime(*expiry_converted).date(), today)
        # days_remaining = datetime(*expiry_converted).date() - today
        # days_remaining_str = str(days_remaining).split(",", 1)[0]
        return time_remaining


class Procedure(models.Model):
    procedure = models.CharField(max_length=300, blank=False, null=False)
    patient = models.CharField(max_length=300, blank=False, null=False)
    date_performed = models.DateTimeField(auto_now=True)
    # products_used = models.ManyToManyField(Product)
    products_used = models.CharField(max_length=300, blank=False, null=False)
    employee = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    # CHOICES = [("1", "Add to Inventory"), ("2", "Delete from Inventory")]
    # choice_field = models.CharField(max_length=1, choices=CHOICES)
    class Meta:
        unique_together = ("patient", "date_performed")
        ordering = ["date_performed"]
        indexes = [models.Index(fields=["patient", "procedure"])]

    def __str__(self) -> str:
        return self.procedure



"""

product_id = 1  # Assuming the product ID you want to retrieve the audit logs for

# Retrieve the audit logs for the specified product
queryset = AuditLog.objects.filter(object_id=product_id).order_by('date')

# Get the product name
product_name = queryset.first().content_object.name  # Assuming the product has a "name" field

# Collate the audit logs into a dictionary
audit_logs = {
    'product_name': product_name,
    'audit_logs': [
        {
            'date': audit_log.date,
            'field_name': audit_log.get_field_name(),
            'old_value': audit_log.old_value,
            'new_value': audit_log.new_value,
        }
        for audit_log in queryset
    ]
}

"""