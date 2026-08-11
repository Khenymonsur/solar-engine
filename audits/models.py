from decimal import Decimal

from django.db import models

from customers.models import Customer
from crm.models import SalesProfile
from equipment.models import Appliance as LibraryAppliance

from django.utils import timezone



class Assessment(models.Model):
    """
    Represents a complete solar assessment for a customer.
    """

    SYSTEM_VOLTAGES = (
        (12, "12 Volts"),
        (24, "24 Volts"),
        (48, "48 Volts"),
    )

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="assessments",
    )

    assigned_sales = models.ForeignKey(
        SalesProfile,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="assessments",
        help_text="Sales consultant responsible for this assessment.",
    )

    project_name = models.CharField(
        max_length=200,
    )

    backup_hours = models.PositiveIntegerField(
        default=8,
        help_text="Desired backup duration in hours.",
    )

    peak_sun_hours = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal("5.50"),
        help_text="Average peak sun hours.",
    )

    system_voltage = models.PositiveIntegerField(
        choices=SYSTEM_VOLTAGES,
        default=48,
    )

    notes = models.TextField(
        blank=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    updated_at = models.DateTimeField(
        auto_now=True,
    )

    STATUS_CHOICES = [

        ("Draft", "Draft"),
        ("In Progress", "In Progress"),
        ("Completed", "Completed"),
        ("Quoted", "Quoted"),
        ("Installed", "Installed"),
        ("Commissioned", "Commissioned"),

    ]

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default="Draft",
    )

    report_generated = models.BooleanField(
        default=False,
    )

    completion_percentage = models.PositiveIntegerField(
        default=0,
    )

    reference = models.CharField(
        max_length=25,
        unique=True,
        blank=True,
        editable=False,
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Assessment"
        verbose_name_plural = "Assessments"

    def __str__(self):
        return f"{self.customer.full_name} | {self.project_name}"



    def save(self, *args, **kwargs):
        """
        Save the assessment and generate a permanent
        reference number after the first save.
        """

        creating = self.pk is None

        super().save(*args, **kwargs)

        if creating and not self.reference:
            self.reference = (
                f"CE-{timezone.now():%Y%m%d}-{self.pk:06d}"
            )

            super().save(update_fields=["reference"])


    # --------------------------------------------------
    # Engineering Properties
    # --------------------------------------------------

    @property
    def total_appliances(self):
        return self.appliances.count()

    @property
    def connected_load(self):
        """
        Total connected running load in Watts.
        """
        return float(
            sum(
                appliance.quantity * appliance.power_rating
                for appliance in self.appliances.all()
            )
        )

    @property
    def running_load(self):
        """
        Alias for connected load.
        """
        return self.connected_load

    @property
    def total_surge_load(self):
        """
        Total starting/surge load in Watts.
        """
        return float(
            sum(
                appliance.quantity * appliance.surge_power
                for appliance in self.appliances.all()
            )
        )

    @property
    def total_critical_load(self):
        """
        Sum of all critical appliances.
        """
        return float(
            sum(
                appliance.quantity * appliance.power_rating
                for appliance in self.appliances.filter(
                    critical_load=True
                )
            )
        )

    @property
    def daily_energy(self):
        """
        Daily energy consumption in Watt-hours.
        """
        return float(
            sum(
                appliance.quantity
                * appliance.power_rating
                * appliance.hours_per_day
                for appliance in self.appliances.all()
            )
        )

    @property
    def peak_load(self):
        """
        Maximum instantaneous load.
        """
        return self.running_load







class Appliance(models.Model):
    """
    Individual appliance belonging to an assessment.
    """

    APPLIANCE_CATEGORIES = (
        ("Lighting", "Lighting"),
        ("Cooling", "Cooling"),
        ("Heating", "Heating"),
        ("Kitchen", "Kitchen"),
        ("Office", "Office"),
        ("Entertainment", "Entertainment"),
        ("Industrial", "Industrial"),
        ("Other", "Other"),
    )

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="appliances",
    )

    library_appliance = models.ForeignKey(
        LibraryAppliance,
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name="assessment_appliances",
    )

    category = models.CharField(
        max_length=30,
        choices=APPLIANCE_CATEGORIES,
        default="Other",
    )

    appliance_name = models.CharField(
        max_length=200,
    )

    quantity = models.PositiveIntegerField(
        default=1,
    )

    power_rating = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Running power in Watts.",
    )

    surge_power = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal("0.00"),
        help_text="Starting/Surge power in Watts.",
    )

    hours_per_day = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
    )

    voltage = models.PositiveIntegerField(
        default=230,
        help_text="Operating voltage.",
    )

    power_factor = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=Decimal("1.00"),
        help_text="Power factor.",
    )

    efficiency = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("100.00"),
        help_text="Appliance efficiency (%).",
    )

    critical_load = models.BooleanField(
        default=False,
    )

    simultaneous = models.BooleanField(
        default=True,
    )

    def save(self, *args, **kwargs):
        if self.library_appliance:
            self.appliance_name = self.library_appliance.name
            self.category = self.library_appliance.category
            self.power_rating = self.library_appliance.default_wattage

            self.surge_power = (
                    self.library_appliance.default_wattage
                    * self.library_appliance.surge_factor
            )

            self.hours_per_day = self.library_appliance.default_hours

        super().save(*args, **kwargs)

    @property
    def connected_load(self):
        """
        Running load for this appliance.
        """
        return self.quantity * self.power_rating

    @property
    def daily_energy(self):
        """
        Daily energy consumption (Wh).
        """
        return (
                self.quantity
                * self.power_rating
                * self.hours_per_day
        )

    @property
    def surge_load(self):
        """
        Starting load (surge).
        """
        return self.quantity * self.surge_power


    @property
    def daily_energy_kwh(self):
        """
        Daily energy in kWh.
        """
        return self.daily_energy / Decimal("1000")


    class Meta:
        ordering = ["id"]
        verbose_name = "Appliance"
        verbose_name_plural = "Appliances"

    def __str__(self):
        return self.appliance_name
