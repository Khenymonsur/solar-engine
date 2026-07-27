from django.db.models.deletion import ProtectedError
from django.shortcuts import redirect
from django.db.models import Q
from django.db.models import Count

from .models import Appliance
from .forms import ApplianceForm


from django.contrib import messages
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)


from django.db.models import Avg


from .forms import (
    SolarPanelForm,
    BatteryForm,
    InverterForm,
    ChargeControllerForm,
)

from .models import (
    Manufacturer,
    SolarPanel,
    Battery,
    Inverter,
    ChargeController,
)


from django.contrib.auth.mixins import (
    LoginRequiredMixin,
    PermissionRequiredMixin,
)


class ManufacturerListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView,
):
    permission_required = "equipment.view_manufacturer"
    raise_exception = True
    model = Manufacturer
    template_name = "equipment/manufacturers/manufacturer_list.html"
    context_object_name = "manufacturers"
    paginate_by = 15
    queryset = Manufacturer.objects.order_by("name")

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        queryset = Manufacturer.objects.all()

        context["manufacturers_count"] = queryset.count()

        context["countries_count"] = (
            queryset.exclude(country="")
            .values("country")
            .distinct()
            .count()
        )

        context["products_count"] = (
            SolarPanel.objects.count()
            + Battery.objects.count()
            + Inverter.objects.count()
            + ChargeController.objects.count()
        )

        context["active_products"] = (
            SolarPanel.objects.filter(active=True).count()
            + Battery.objects.filter(active=True).count()
            + Inverter.objects.filter(active=True).count()
            + ChargeController.objects.filter(active=True).count()
        )

        return context




class ManufacturerDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):
    model = Manufacturer
    raise_exception = True
    permission_required = "equipment.view_manufacturer"
    template_name = "equipment/manufacturers/manufacturer_detail.html"


class ManufacturerCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView):
    permission_required = "equipment.add_manufacturer"
    raise_exception = True
    model = Manufacturer
    fields = "__all__"
    template_name = "equipment/manufacturers/manufacturer_form.html"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Manufacturer created successfully."
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("equipment:manufacturers-list")


class ManufacturerUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    permission_required = "equipment.change_manufacturer"
    raise_exception = True
    model = Manufacturer
    fields = "__all__"
    template_name = "equipment/manufacturers/manufacturer_form.html"

    def form_valid(self, form):

        messages.success(
            self.request,
            "Manufacturer updated successfully."
        )

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("equipment:manufacturers-list")



class ManufacturerDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    permission_required = "equipment.delete_manufacturer"
    raise_exception = True
    model = Manufacturer
    template_name = "equipment/manufacturers/manufacturer_confirm_delete.html"
    success_url = reverse_lazy("equipment:manufacturers-list")




class SolarPanelListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    permission_required = "equipment.view_solarpanel"
    raise_exception = True
    model = SolarPanel
    template_name = "equipment/solar/panel_list.html"
    context_object_name = "panels"
    paginate_by = 15
    queryset = (
        SolarPanel.objects
        .select_related("manufacturer")
        .order_by("manufacturer__name", "model")
    )


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["manufacturers_count"] = Manufacturer.objects.count()

        context["active_count"] = SolarPanel.objects.filter(
            active=True
        ).count()

        context["average_wattage"] = (
                SolarPanel.objects.aggregate(
                    Avg("wattage")
                )["wattage__avg"] or 0
        )

        return context


class SolarPanelCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    permission_required = "equipment.add_solarpanel"
    raise_exception = True
    model = SolarPanel
    form_class = SolarPanelForm
    template_name = "equipment/solar/panel_form.html"
    success_url = reverse_lazy("equipment:panel-list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Solar panel added successfully."
        )

        return super().form_valid(form)



class SolarPanelUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    permission_required = "equipment.change_solarpanel"
    raise_exception = True
    model = SolarPanel
    form_class = SolarPanelForm
    template_name = "equipment/solar/panel_form.html"
    success_url = reverse_lazy("equipment:panel-list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Solar panel updated successfully."
        )

        return super().form_valid(form)



class SolarPanelDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    permission_required = "equipment.delete_solarpanel"
    raise_exception = True
    model = SolarPanel
    template_name = "equipment/solar/panel_confirm_delete.html"
    success_url = reverse_lazy("equipment:panel-list")




class BatteryListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):

    permission_required = "equipment.view_battery"
    raise_exception = True
    model = Battery
    template_name = "equipment/batteries/battery_list.html"
    context_object_name = "batteries"
    paginate_by = 15
    queryset = (
        Battery.objects
        .select_related("manufacturer")
        .order_by("manufacturer__name", "model")
    )

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        context["manufacturers_count"] = Manufacturer.objects.count()

        context["active_count"] = Battery.objects.filter(
            active=True
        ).count()

        return context


class BatteryDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):

    model = Battery
    permission_required = "equipment.view_battery"
    template_name = "equipment/batteries/battery_detail.html"
    raise_exception = True


class BatteryCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    permission_required = "equipment.add_battery"
    raise_exception = True
    model = Battery
    form_class = BatteryForm
    template_name = "equipment/batteries/battery_form.html"
    success_url = reverse_lazy("equipment:battery-list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Battery added successfully."
        )

        return super().form_valid(form)


class BatteryUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    permission_required = "equipment.change_battery"
    raise_exception = True
    model = Battery
    form_class = BatteryForm
    template_name = "equipment/batteries/battery_form.html"
    success_url = reverse_lazy("equipment:battery-list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Battery updated successfully."
        )

        return super().form_valid(form)


class BatteryDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    permission_required = "equipment.delete_battery"
    raise_exception = True
    model = Battery
    template_name = "equipment/batteries/battery_confirm_delete.html"
    success_url = reverse_lazy("equipment:battery-list")




class InverterListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    permission_required = "equipment.view_inverter"
    raise_exception = True
    model = Inverter
    template_name = "equipment/inverters/inverter_list.html"
    context_object_name = "inverters"
    paginate_by = 15
    queryset = (
        Inverter.objects
        .select_related("manufacturer")
        .order_by("manufacturer__name", "capacity_kva")
    )


class InverterDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):

    model = Inverter
    permission_required = "equipment.view_inverter"
    template_name = "equipment/inverters/inverter_detail.html"
    raise_exception = True


class InverterCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    permission_required = "equipment.add_inverter"
    raise_exception = True
    model = Inverter
    form_class = InverterForm
    template_name = "equipment/inverters/inverter_form.html"
    success_url = reverse_lazy("equipment:inverter-list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Inverter added successfully."
        )

        return super().form_valid(form)


class InverterUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    permission_required = "equipment.change_inverter"
    raise_exception = True
    model = Inverter
    form_class = InverterForm
    template_name = "equipment/inverters/inverter_form.html"
    success_url = reverse_lazy("equipment:inverter-list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Inverter updated successfully."
        )

        return super().form_valid(form)


class InverterDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    permission_required = "equipment.delete_inverter"
    raise_exception = True
    model = Inverter
    template_name = "equipment/inverters/inverter_confirm_delete.html"
    success_url = reverse_lazy("equipment:inverter-list")




class ChargeControllerListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    permission_required = "equipment.view_chargecontroller"
    raise_exception = True
    model = ChargeController
    template_name = "equipment/controllers/controller_list.html"
    context_object_name = "controllers"
    paginate_by = 15

    queryset = (
        ChargeController.objects
        .select_related("manufacturer")
        .order_by(
            "manufacturer__name",
            "current_rating",
        )
    )


class ChargeControllerDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):

    model = ChargeController
    permission_required = "equipment.view_chargecontroller"
    template_name = "equipment/controllers/controller_detail.html"
    raise_exception = True


class ChargeControllerCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    permission_required = "equipment.add_chargecontroller"
    raise_exception = True
    model = ChargeController
    form_class = ChargeControllerForm
    template_name = "equipment/controllers/controller_form.html"
    success_url = reverse_lazy("equipment:controller-list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Charge Controller added successfully."
        )

        return super().form_valid(form)


class ChargeControllerUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    permission_required = "equipment.change_chargecontroller"
    raise_exception = True
    model = ChargeController
    form_class = ChargeControllerForm
    template_name = "equipment/controllers/controller_form.html"
    success_url = reverse_lazy("equipment:controller-list")

    def form_valid(self, form):

        messages.success(
            self.request,
            "Charge Controller updated successfully."
        )

        return super().form_valid(form)


class ChargeControllerDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    permission_required = "equipment.delete_chargecontroller"
    raise_exception = True
    model = ChargeController
    template_name = (
        "equipment/controllers/controller_confirm_delete.html"
    )
    success_url = reverse_lazy("equipment:controller-list")





class ApplianceListView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    ListView
):
    permission_required = "equipment.view_appliance"
    raise_exception = True
    model = Appliance
    template_name = "equipment/appliances/appliance_list.html"
    context_object_name = "appliances"
    paginate_by = 15


    def get_queryset(self):
        queryset = (
            Appliance.objects
            .annotate(
                assessment_count=Count("assessment_appliances")
            )
            .order_by(
                "category",
                "name"
            )
        )

        q = self.request.GET.get("q")

        if q:
            queryset = queryset.filter(
                Q(name__icontains=q)
                | Q(category__icontains=q)
            )

        return queryset


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        queryset = Appliance.objects.all()

        context["active_count"] = queryset.filter(active=True).count()

        context["categories_count"] = (
            queryset.values("category")
            .distinct()
            .count()
        )

        context["average_wattage"] = (
            queryset.aggregate(
                Avg("default_wattage")
            )["default_wattage__avg"]
            or 0
        )

        return context


class ApplianceDetailView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DetailView
):

    model = Appliance
    permission_required = "equipment.view_appliance"
    template_name = "equipment/appliances/appliance_detail.html"
    raise_exception = True



class ApplianceCreateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    CreateView
):
    permission_required = "equipment.add_appliance"
    raise_exception = True
    model = Appliance
    form_class = ApplianceForm
    template_name = "equipment/appliances/appliance_form.html"
    success_url = reverse_lazy("equipment:appliance-list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Appliance created successfully."
        )
        return super().form_valid(form)



class ApplianceUpdateView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    UpdateView
):
    permission_required = "equipment.change_appliance"
    raise_exception = True
    model = Appliance
    form_class = ApplianceForm
    template_name = "equipment/appliances/appliance_form.html"
    success_url = reverse_lazy("equipment:appliance-list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Appliance updated successfully."
        )
        return super().form_valid(form)



class ApplianceDeleteView(
    LoginRequiredMixin,
    PermissionRequiredMixin,
    DeleteView
):
    permission_required = "equipment.delete_appliance"
    raise_exception = True
    model = Appliance
    template_name = (
        "equipment/appliances/appliance_confirm_delete.html"
    )
    success_url = reverse_lazy(
        "equipment:appliance-list"
    )

    def post(self, request, *args, **kwargs):

        self.object = self.get_object()

        try:

            self.object.delete()

            messages.success(
                request,
                "Appliance deleted successfully."
            )

        except ProtectedError:

            messages.error(
                request,
                (
                    "This appliance cannot be deleted because it "
                    "is currently used in one or more engineering "
                    "assessments. Remove it from those assessments "
                    "first or mark it as inactive."
                )
            )

        return redirect(self.success_url)