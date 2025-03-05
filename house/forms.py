
from django import forms
from .models import house


class houseForm(forms.ModelForm):
    class Meta:
        model = house
        fields = ['name_house', 'description_house', 'image_house']