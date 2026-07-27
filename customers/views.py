from django.contrib import messages
from django.db.models import Count, Q
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from .forms import CustomerForm
from .models import Customer
from audits.models import Assessment


class CustomerListView(ListView):
    permission_required = "customers.view_customer"
    model = Customer
    template_name = "customers/customer_list.html"
    context_object_name = "customers"
    paginate_by = 20

    def get_queryset(self):
        queryset = (
            Customer.objects
            .annotate(
                assessment_total=Count("assessments")
            )
            .order_by("full_name")
        )

        search = self.request.GET.get("q")

        if search:
            queryset = queryset.filter(
                Q(full_name__icontains=search)
                | Q(company_name__icontains=search)
                | Q(email__icontains=search)
                | Q(phone__icontains=search)
                | Q(state__icontains=search)
                | Q(city__icontains=search)
                | Q(lga__icontains=search)
                | Q(area__icontains=search)
            )

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        customers = Customer.objects.all()

        context.update({

            "customer_count": customers.count(),
            "assessment_count": Assessment.objects.count(),
            "residential_count": customers.filter(
                building_type=Customer.RESIDENTIAL
            ).count(),
            "commercial_count": customers.filter(
                building_type=Customer.COMMERCIAL
            ).count(),
            "industrial_count": customers.filter(
                building_type=Customer.INDUSTRIAL
            ).count(),

            "completed_designs": 0,

        })

        return context


class CustomerDetailView(DetailView):
    permission_required = "customers.view_customer"
    model = Customer
    template_name = "customers/customer_detail.html"
    context_object_name = "object"


class CustomerCreateView(CreateView):
    permission_required = "customers.add_customer"
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customers:list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Customer created successfully."
        )
        return super().form_valid(form)


class CustomerUpdateView(UpdateView):
    permission_required = "customers.change_customer"
    model = Customer
    form_class = CustomerForm
    template_name = "customers/customer_form.html"
    success_url = reverse_lazy("customers:list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Customer updated successfully."
        )
        return super().form_valid(form)


class CustomerDeleteView(DeleteView):
    permission_required = "customers.delete_customer"
    model = Customer
    template_name = "customers/customer_confirm_delete.html"
    success_url = reverse_lazy("customers:list")

    def form_valid(self, form):
        messages.success(
            self.request,
            "Customer deleted successfully."
        )
        return super().form_valid(form)