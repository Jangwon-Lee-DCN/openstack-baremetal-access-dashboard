from django import forms


class RequestForm(forms.Form):
    profile = forms.ChoiceField(choices=())
    quantity = forms.IntegerField(min_value=1, max_value=16)
    lease_days = forms.IntegerField(min_value=1, max_value=365)
    rack = forms.ChoiceField(choices=(), required=False)
    purpose = forms.CharField(min_length=3, max_length=1000, widget=forms.Textarea)

    def __init__(self, *args, offers=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile"].choices = sorted({(row["profile"], row["profile"]) for row in offers})
        racks = sorted({(row["rack"], row["rack"]) for row in offers if row.get("rack")})
        self.fields["rack"].choices = [("", "Any eligible rack"), *racks]
