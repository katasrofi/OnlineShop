from .models import Product, ProductImage, Category, Review 
from django import forms

# Create the forms here 
class AddProductForm(forms.ModelForm):
    class Meta:
        model = Product 
        fields = ["category", "name", "description", "attributes", "price", "stock"]

    # Images form to handle several image 
    # images = forms.FileField(widget=forms.FileInput(attrs={"multiple": True}), required=False)

    # Additional information for spesific product 
    attributes_keys = forms.CharField(required=False, widget=forms.HiddenInput())
    attributes_values = forms.CharField(required=False, widget=forms.HiddenInput())

    # Cleaning 
    def clean(self):
        cleaned_data = super().clean()

        # Take the key from hidden input 
        keys = cleaned_data.get("attributes_keys", "").split(",")
        values = cleaned_data.get("attributes_values", "").split(",")

        # Create the keys and values dictionary 
        attributes = {
            key.strip(): value.strip()
            for key, value in zip(keys, values)
            if key and value 
        }

        # Save the data 
        cleaned_data["attributes"] = attributes 
        return cleaned_data 


