from django import forms
from django.forms import ModelForm, SelectDateWidget
# from .models import Venue, Event
from .models import Product, Vendor, vendor_details

# Admin SuperUser Event Form
# class EventFormAdmin(ModelForm):
# 	class Meta:
# 		model = Event
# 		fields = ('name', 'event_date', 'venue', 'manager', 'attendees', 'description')
# 		labels = {
# 			'name': '',
# 			'event_date': 'YYYY-MM-DD HH:MM:SS',
# 			'venue': 'Venue',
# 			'manager': 'Manager',
# 			'attendees': 'Attendees',
# 			'description': '',			
# 		}
# 		widgets = {
# 			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Name'}),
# 			'event_date': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Event Date'}),
# 			'venue': forms.Select(attrs={'class':'form-select', 'placeholder':'Venue'}),
# 			'manager': forms.Select(attrs={'class':'form-select', 'placeholder':'Manager'}),
# 			'attendees': forms.SelectMultiple(attrs={'class':'form-control', 'placeholder':'Attendees'}),
# 			'description': forms.Textarea(attrs={'class':'form-control', 'placeholder':'Description'}),
# 		}

# Product Form

class ProductForm(ModelForm):
	class Meta:
		model = Product
		fields = ('name', 'reference_id', 'expiry_date', 'size', 'quantity_on_hand', 'vendor')
		labels = {
		'name': 'Product Name:',
		'reference_id': 'Reference ID:',
		'expiry_date': 'Expiration Date:',
		'size': 'Size:',
		'quantity_on_hand': 'Quantity currently on hand:',
		'vendor': 'Vendor ID:',		
		}
		widgets = {
			'name': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Product Name'}),
			'reference_id': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Reference ID'}),
			'expiry_date': forms.DateInput(attrs={'class':'form-select', 'placeholder':'Expiration Date: (MM/DD/YYYY)'}, format="%m/%d/%Y"),
			'size': forms.TextInput(attrs={'class':'form-control', 'placeholder':'Size'}),
			# 'quantity_on_hand': forms.NumberInput(attrs={'class':'form-control', 'placeholder':'Quantity available'}),
			'quantity_on_hand': forms.NumberInput(
			    attrs={
			        'class': 'form-control',
			        'placeholder': 'Quantity available',
			        'min': '0',  # Minimum value allowed for the input
			        'step': '1',  # Step value for increment and decrement
			        'id': 'id_quantity_on_hand',
			    },
			),

			'vendor': forms.Select(attrs={'class':'form-select', 'placeholder':'Vendor'}),
		}

	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)


	def __init__(self, *args, **kwargs):
		readonly_fields = kwargs.pop('readonly_fields', [])
		super().__init__(*args, **kwargs)
		for field in readonly_fields:
			self.fields[field].disabled = True
	expiry_date = forms.DateField(widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),),)

class UneditableProductForm(ProductForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields['reference_id'].widget.attrs['disabled'] = True
		self.fields['expiry_date'].widget.attrs['disabled'] = True
		self.fields['vendor'].widget.attrs['disabled'] = True
		self.fields['name'].widget.attrs['disabled'] = True
		self.fields['size'].widget.attrs['disabled'] = True





	# def __init__(self, *args, **kwargs):
	# 	super().__init__(*args, **kwargs)
	# 	# self.fields['reference_id'].widget.attrs['disabled'] = True
	# 	# self.fields['expiry_date'].widget.attrs['disabled'] = True
	# 	# self.fields['vendor'].widget.attrs['disabled'] = True
	# 	# self.fields['name'].widget.attrs['disabled'] = True
	# 	# self.fields['size'].widget.attrs['disabled'] = True

	# 	# vendor = forms.ChoiceField(choices=vendor_details)
	# # name = forms.CharField(disabled=True)
	# # reference_id = forms.CharField(disabled=True)
	# # size = forms.CharField(disabled=True)
	# expiry_date = forms.DateField(widget=SelectDateWidget(empty_label=("Choose Year", "Choose Month", "Choose Day"),),)
	# 	