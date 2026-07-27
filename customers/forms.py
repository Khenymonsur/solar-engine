from django import forms

from .choices import NIGERIAN_STATES
from .models import Customer



class CustomerForm(forms.ModelForm):

    class Meta:
        model = Customer

        fields = [
            "full_name",
            "company_name",
            "email",
            "phone",
            "whatsapp",
            "address",
            "state",
            "lga",
            "area",
            "city",
            "building_type",
        ]

        widgets = {

            "full_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "company_name": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "email": forms.EmailInput(
                attrs={"class": "form-control"}
            ),

            "phone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "whatsapp": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "address": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 3,
                }
            ),

            "state": forms.Select(
                choices=NIGERIAN_STATES,
                attrs={
                    "class": "form-select",
                    "id": "id_state",
                },
            ),

            "lga": forms.Select(
                choices=[("", "Select State First")],
                attrs={
                    "class": "form-select",
                    "id": "id_lga",
                },
            ),

            "area": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "e.g. Lekki Phase 1, GRA, Wuse II",
                }
            ),

            "city": forms.TextInput(
                attrs={
                    "class": "form-control",
                    "placeholder": "Legacy field (Feature in Progress)",
                }
            ),

            "building_type": forms.Select(
                attrs={"class": "form-select"}
            ),
        }


    def __init__(self, *args, **kwargs):

        super().__init__(*args, **kwargs)

        for name, field in self.fields.items():

            if isinstance(field.widget, forms.Select):
                field.widget.attrs.setdefault("class", "form-select")
            else:
                field.widget.attrs.setdefault("class", "form-control")

        # Preserve selected LGA when editing
        self.fields["lga"].widget.attrs["data-selected"] = (
            self.instance.lga if self.instance.pk else ""
        )
