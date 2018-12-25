from django import forms

class ProofRowForm(forms.Form):
    statement = forms.CharField(label="", max_length = 50)
    reason    = forms.CharField(label="", max_length = 100)
