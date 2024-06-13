from django import forms
from .models import *

class PresentationForm(forms.ModelForm):
    class Meta:
        model = Presentation
        fields = ['name', 'description', 'status']

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