from django import forms
from .models import value
from django import forms

class TitleForm(forms.ModelForm):
    class Meta:
        model= value
        fields=['task','complete']





