from django import forms

class form0(forms.Form):
     im = forms.ImageField()

class form1(forms.Form):
     im = forms.CharField()
     vibor = forms.IntegerField()