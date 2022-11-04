from django import forms
from django.forms import widgets, DateField, Textarea
# from django.forms.widgets import NumberInput
from .models import Player, Strike

class StrikeModelForm(forms.ModelForm):
  class Meta:
    model = Strike
    fields = (
      'player',
      'strike_date',
      'activity',
      'ishard',
      'comments'
    )
    widgets = {
      'strike_date': widgets.DateInput(attrs={'type':'date'}),
      'comments': Textarea(attrs={'cols': 40, 'rows': 5}),
    }
  

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
