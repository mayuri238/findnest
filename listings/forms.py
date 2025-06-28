from django import forms
from .models import Property

class PropertyForm(forms.ModelForm):
    class Meta:
         model = Property
         fields = ['title', 'description', 'address', 'rent', 'image', 'latitude', 'longitude']

from django import forms

class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
