from django import forms
from customers.nigeria import STATE_LGAS


class CustomerRegistrationForm(forms.Form):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "id_password1",
                "placeholder": "Create a password",
            }
        ),
    )

    password2 = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "id": "id_password2",
                "placeholder": "Confirm your password",
            }
        ),
    )

    def clean(self):

        cleaned = super().clean()

        if cleaned.get("password1") != cleaned.get("password2"):
            raise forms.ValidationError(
                "Passwords do not match."
            )

        return cleaned




class AssessmentStepOneForm(forms.Form):

    full_name = forms.CharField(
        label="Full Name",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your full name",
            }
        ),
    )

    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter your email",
            }
        ),
    )

    phone = forms.CharField(
        label="Phone Number",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "08012345678",
            }
        ),
    )

    whatsapp = forms.CharField(
        required=False,
        label="WhatsApp Number",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Optional",
            }
        ),
    )



class AssessmentStepTwoForm(forms.Form):

    PROPERTY_TYPES = [
        ("residential", "Residential"),
        ("commercial", "Commercial"),
        ("industrial", "Industrial"),
    ]

    BUILDING_TYPES = [
        ("flat", "Flat"),
        ("duplex", "Duplex"),
        ("bungalow", "Bungalow"),
        ("office", "Office"),
        ("shop", "Shop"),
        ("factory", "Factory"),
        ("school", "School"),
        ("hospital", "Hospital"),
        ("hotel", "Hotel"),
        ("church", "Church / Mosque"),
        ("other", "Other"),
    ]

    property_type = forms.ChoiceField(
        choices=PROPERTY_TYPES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    building_type = forms.ChoiceField(
        choices=BUILDING_TYPES,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    state = forms.ChoiceField(
        label="State",
        choices=[
            ("", "Select State"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_state",
            }
        ),
    )

    lga = forms.ChoiceField(
        label="Local Government Area",
        choices=[
            ("", "Select LGA"),
        ],
        widget=forms.Select(
            attrs={
                "class": "form-select",
                "id": "id_lga",
            }
        ),
    )

    city = forms.CharField(
        label="City / Town",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Enter city or town",
            }
        ),
    )

    address = forms.CharField(
        label="Property Address",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "id_address",
                "placeholder": "Start typing your address...",
                "autocomplete": "off",
            }
        ),
    )

    latitude = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "id": "id_latitude",
            }
        ),
    )

    longitude = forms.CharField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                "id": "id_longitude",
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Populate State dropdown
        self.fields["state"].choices = [
            ("", "Select State"),
            *[(state, state) for state in sorted(STATE_LGAS.keys())],
        ]

        # Determine selected state
        state = (
                self.data.get("state")
                or self.initial.get("state")
        )

        # Populate LGA dropdown
        self.fields["lga"].choices = [("", "Select LGA")]

        if state in STATE_LGAS:
            self.fields["lga"].choices += [
                (lga, lga)
                for lga in STATE_LGAS[state]
            ]



class AssessmentStepThreeForm(forms.Form):

    YES_NO = [

        ("yes", "Yes"),

        ("no", "No"),

    ]

    POWER_SCOPE = [

        ("full", "Entire Building"),

        ("essential", "Essential Appliances Only"),

    ]

    grid_available = forms.ChoiceField(

        label="Do you currently have grid electricity?",

        choices=YES_NO,

        widget=forms.RadioSelect,

    )

    generator_available = forms.ChoiceField(

        label="Do you currently use a generator?",

        choices=YES_NO,

        widget=forms.RadioSelect,

    )

    BACKUP_OPTIONS = [
        (3, "3 Hours"),
        (6, "6 Hours"),
        (8, "8 Hours (Recommended)"),
        (10, "10 Hours"),
        (12, "12 Hours"),
        (24, "24 Hours"),
    ]

    backup_hours = forms.ChoiceField(
        label="Desired Backup Time",
        choices=BACKUP_OPTIONS,
        widget=forms.Select(
            attrs={
                "class": "form-select",
            }
        ),
    )

    power_scope = forms.ChoiceField(

        label="Which appliances should the system power?",

        choices=POWER_SCOPE,

        widget=forms.RadioSelect,

    )



class AssessmentApplianceForm(forms.Form):

    appliance_name = forms.CharField(
        label="Appliance",
        max_length=150,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. Television",
            }
        ),
    )

    watts = forms.DecimalField(
        label="Rated Power (Watts)",
        max_digits=10,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. 120",
            }
        ),
    )

    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
            }
        ),
    )

    hours_per_day = forms.DecimalField(
        label="Hours Used Per Day",
        max_digits=4,
        decimal_places=1,
        initial=8,
        widget=forms.NumberInput(
            attrs={
                "class": "form-control",
                "placeholder": "e.g. 6",
            }
        ),
    )
