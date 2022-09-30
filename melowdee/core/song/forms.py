from django import forms

# creating a form
class InputForm(forms.Form):
    artist_name = forms.CharField(max_length=200)

class URLForm(forms.Form):
    url = forms.CharField(max_length=100)
