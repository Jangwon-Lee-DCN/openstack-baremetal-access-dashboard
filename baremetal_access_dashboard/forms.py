from django import forms


class RequestForm(forms.Form):
    profile = forms.RegexField(r"^[a-z0-9][a-z0-9_-]{1,63}$", max_length=64)
    quantity = forms.IntegerField(min_value=1, max_value=16)
    lease_days = forms.IntegerField(min_value=1, max_value=365)
    rack = forms.RegexField(r"^[A-Za-z0-9][A-Za-z0-9 _-]{0,63}$", max_length=64, required=False)
    purpose = forms.CharField(min_length=3, max_length=1000, widget=forms.Textarea)
