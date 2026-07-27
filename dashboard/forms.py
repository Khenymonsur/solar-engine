from django import forms

from .models import (
    UserProfile,
    UserPreference,
    SystemSetting,
)


class ProfileForm(forms.ModelForm):

    class Meta:

        model = UserProfile

        fields = [
            "avatar",
            "phone",
            "department",
            "employee_id",
            "job_title",
            "biography",
        ]

        widgets = {

            "phone": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "department": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "employee_id": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "job_title": forms.TextInput(
                attrs={
                    "class": "form-control",
                }
            ),

            "biography": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "rows": 5,
                }
            ),

        }


class PreferenceForm(forms.ModelForm):

    class Meta:

        model = UserPreference

        exclude = ["user"]

        widgets = {

            "theme": forms.Select(
                attrs={"class": "form-select"}
            ),

            "language": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "timezone": forms.TextInput(
                attrs={"class": "form-control"}
            ),

            "date_format": forms.Select(
                attrs={"class": "form-select"}
            ),

        }




class SystemSettingForm(forms.ModelForm):

    class Meta:

        model = SystemSetting
        fields = "__all__"
        widgets = {

            "company_name": forms.TextInput(attrs={"class": "form-control"}),
            "company_email": forms.EmailInput(attrs={"class": "form-control"}),
            "company_phone": forms.TextInput(attrs={"class": "form-control"}),
            "website": forms.URLInput(attrs={"class": "form-control"}),
            "currency": forms.TextInput(attrs={"class": "form-control"}),
            "quotation_prefix": forms.TextInput(attrs={"class": "form-control"}),
            "invoice_prefix": forms.TextInput(attrs={"class": "form-control"}),
            "default_backup_hours": forms.NumberInput(attrs={"class": "form-control"}),
            "safety_margin": forms.NumberInput(attrs={"class": "form-control"}),
            "default_voltage": forms.NumberInput(attrs={"class": "form-control"}),
            "google_maps_api_key": forms.PasswordInput(
                attrs={"class": "form-control"},
                render_value=True,
            ),

            "weather_api_key": forms.PasswordInput(
                attrs={"class": "form-control"},
                render_value=True,
            ),
        }