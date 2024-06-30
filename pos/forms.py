from django import forms
from .models import *

class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['name', 'description', 'status']
        #widgets = {"title": forms.TextInput(attrs={"class": "form-control inputs"}), "description": forms.Textarea(attrs={"class": "form-control inputs"}),"image": forms.FileInput(attrs={"class": "form-control-field inputs"}) }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['categoryname', 'status']

class SizeForm(forms.ModelForm):
    class Meta:
        model = Size
        fields = ['size', 'status']

class SettingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = ['systemname', 'image', 'address', 'phone', 'exchange']