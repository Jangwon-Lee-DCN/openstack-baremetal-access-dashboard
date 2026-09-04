from django import forms
from uuid import uuid4


class RequestForm(forms.Form):
    idempotency_key = forms.CharField(widget=forms.HiddenInput, min_length=8, max_length=128)
    profile = forms.ChoiceField(choices=())
    quantity = forms.IntegerField(min_value=1, max_value=16)
    lease_days = forms.IntegerField(min_value=1, max_value=365)
    rack = forms.ChoiceField(choices=(), required=False)
    purpose = forms.CharField(
        min_length=3, max_length=1000, widget=forms.Textarea(attrs={"rows": 5}),
    )

    def __init__(self, *args, offers=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["profile"].label = "Hardware profile"
        self.fields["profile"].help_text = "Select the hardware class required by the workload."
        self.fields["quantity"].initial = 1
        self.fields["quantity"].help_text = "Between 1 and 16 nodes."
        self.fields["lease_days"].label = "Lease duration"
        self.fields["lease_days"].initial = 1
        self.fields["lease_days"].help_text = "The lease begins after administrator approval."
        self.fields["rack"].label = "Rack preference"
        self.fields["rack"].help_text = "Leave this unrestricted to use any eligible rack."
        self.fields["purpose"].help_text = "Describe the research workload and any special requirements."
        for name, field in self.fields.items():
            if name != "idempotency_key":
                field.widget.attrs.setdefault("class", "form-control")
        self.fields["quantity"].widget.attrs.update({"inputmode": "numeric", "placeholder": "1"})
        self.fields["lease_days"].widget.attrs.update({"inputmode": "numeric", "placeholder": "1"})
        self.fields["purpose"].widget.attrs.setdefault(
            "placeholder", "Example: Kubernetes networking experiment for a two-week project"
        )
        if not self.is_bound:
            self.initial["idempotency_key"] = str(uuid4())
        self.fields["profile"].choices = sorted({(row["profile"], row["profile"]) for row in offers})
        racks = sorted({(row["rack"], row["rack"]) for row in offers if row.get("rack")})
        self.fields["rack"].choices = [("", "No preference (any eligible rack)"), *racks]


class DeployForm(forms.Form):
    idempotency_key = forms.CharField(widget=forms.HiddenInput, min_length=8, max_length=128)
    version = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    node_uuid = forms.UUIDField(widget=forms.HiddenInput)
    image_id = forms.ChoiceField(choices=())
    hostname = forms.RegexField(r"^[a-zA-Z0-9][a-zA-Z0-9.-]{0,62}$", max_length=63)
    user_data = forms.CharField(required=False, max_length=65536, widget=forms.Textarea)

    def __init__(self, *args, images=(), **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["image_id"].choices = [(row["id"], row["name"]) for row in images]


class PowerForm(forms.Form):
    idempotency_key = forms.CharField(widget=forms.HiddenInput, min_length=8, max_length=128)
    version = forms.IntegerField(min_value=0, widget=forms.HiddenInput)
    node_uuid = forms.UUIDField(widget=forms.HiddenInput)
    action = forms.ChoiceField(choices=[
        ("on", "Power on"), ("off", "Power off"), ("reboot", "Reboot"),
        ("soft off", "Soft power off"), ("soft reboot", "Soft reboot"),
    ])
