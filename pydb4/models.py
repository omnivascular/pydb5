from django.db import models
from django.template.defaultfilters import date
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from datetime import datetime, date
from dateutil.relativedelta import relativedelta


vendor_details = {
    1: ["Boston Scientific", "BSCI"],
    2: ["Abbott", "ABBT"],
    3: ["ev3/Covidien/Medtronic", "MTRNC"],
    4: ["COOK Medical", "COOK"],
    5: ["Terumo", "TRMO"],
    6: ["Coulmed", "COULMD"],
}

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
    is_purchased = models.BooleanField(default=True)
    size = models.CharField(max_length=60, default="N/A", blank=True)
    quantity_on_hand = models.PositiveIntegerField(default=1)
    quantity_on_order = models.PositiveIntegerField(default=0)
    last_modified = models.DateTimeField(auto_now=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        self.ref_id_expiry_date = self.generate_combined_field()
        super().save(*args, **kwargs)

    def generate_combined_field(self):
        return f"{self.reference_id}***{self.expiry_date.date()}"

    class Meta:
        unique_together = ("reference_id", "expiry_date")
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
