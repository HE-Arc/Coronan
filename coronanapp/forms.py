from django import forms

class BetForm(forms.Form):
    cases = forms.IntegerField()
    sum = forms.IntegerField()