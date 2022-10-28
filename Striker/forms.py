from django import forms
from django.forms import widgets, DateField, Textarea
# from django.forms.widgets import NumberInput
from .models import Player

class PlayerModelForm(forms.ModelForm):
  class Meta:
    model = Player
    fields = (
      'name',
      'allycode',
      'level',
      'gp',
      'gpChar',
      'gpShip'
    )
    
    
class StrikeForm(forms.Form):
  strike_date = forms.DateField()
  activity = forms.CharField()
  ishard = forms.BooleanField()
  comments = forms.CharField(required=False)
