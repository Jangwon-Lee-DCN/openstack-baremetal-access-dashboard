from django import forms
from uuid import uuid4


class RequestForm(forms.Form):
    idempotency_key = forms.CharField(widget=forms.HiddenInput, min_length=8, max_length=128)
    profile = forms.ChoiceField(choices=())
    quantity = forms.IntegerField(min_value=1, max_value=16)
    lease_days = forms.IntegerField(min_value=1, max_value=365)
    rack = forms.ChoiceField(choices=(), required=False)
    purpose = forms.CharField(min_length=3, max_length=1000, widget=forms.Textarea)

    def __init__(self, *args, offers=(), **kwargs):
        super().__init__(*args, **kwargs)
        if not self.is_bound:
            self.initial["idempotency_key"] = str(uuid4())
        self.fields["profile"].choices = sorted({(row["profile"], row["profile"]) for row in offers})
        racks = sorted({(row["rack"], row["rack"]) for row in offers if row.get("rack")})
        self.fields["rack"].choices = [("", "Any eligible rack"), *racks]
