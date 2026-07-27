from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission



class Command(BaseCommand):

    help = "Create default roles and assign permissions."

    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write(self.style.NOTICE("Creating roles..."))

        # --------------------------------------------------
        # Administrator
        # --------------------------------------------------

        admin_group, _ = Group.objects.get_or_create(
            name="Administrator"
        )

        admin_group.permissions.set(
            Permission.objects.all()
        )

        # --------------------------------------------------
        # Engineer
        # --------------------------------------------------

        engineer_group, _ = Group.objects.get_or_create(
            name="Engineer"
        )

        engineer_permissions = [

            # Customers

            "view_customer",
            "add_customer",
            "change_customer",
            "delete_customer",

            # Assessments

            "view_assessment",
            "add_assessment",
            "change_assessment",
            "delete_assessment",

            # Equipment

            "view_manufacturer",
            "add_manufacturer",
            "change_manufacturer",
            "delete_manufacturer",

            "view_appliance",
            "add_appliance",
            "change_appliance",
            "delete_appliance",

            "view_solarpanel",
            "add_solarpanel",
            "change_solarpanel",
            "delete_solarpanel",

            "view_battery",
            "add_battery",
            "change_battery",
            "delete_battery",

            "view_inverter",
            "add_inverter",
            "change_inverter",
            "delete_inverter",

            "view_chargecontroller",
            "add_chargecontroller",
            "change_chargecontroller",
            "delete_chargecontroller",

            # Reports

            "view_report",

            # Quotations

            "view_quotation",
            "add_quotation",
            "change_quotation",
        ]

        engineer_group.permissions.set(
            Permission.objects.filter(
                codename__in=engineer_permissions
            )
        )

        # Dashboard custom permissions

        dashboard_permissions = Permission.objects.filter(
            codename__in=[
                "view_analytics",
                "view_userprofile",
                "view_userpreference",
            ]
        )

        engineer_group.permissions.add(*dashboard_permissions)

        # --------------------------------------------------
        # Sales Executive
        # --------------------------------------------------

        sales_group, _ = Group.objects.get_or_create(
            name="Sales Executive"
        )

        sales_permissions = [

            "view_customer",
            "add_customer",
            "change_customer",

            "view_assessment",

            "view_quotation",
            "add_quotation",
            "change_quotation",

            "view_report",
        ]

        sales_group.permissions.set(
            Permission.objects.filter(
                codename__in=sales_permissions
            )
        )

        sales_group.permissions.add(*dashboard_permissions)

        # --------------------------------------------------
        # Finance
        # --------------------------------------------------

        finance_group, _ = Group.objects.get_or_create(
            name="Finance"
        )

        finance_permissions = [

            "view_report",

            "view_quotation",
            "change_quotation",
        ]

        finance_group.permissions.set(
            Permission.objects.filter(
                codename__in=finance_permissions
            )
        )

        finance_group.permissions.add(*dashboard_permissions)

        # --------------------------------------------------
        # Customer Service
        # --------------------------------------------------

        support_group, _ = Group.objects.get_or_create(
            name="Customer Service"
        )

        support_permissions = [

            "view_customer",
            "add_customer",
            "change_customer",

            "view_quotation",

            "view_assessment",
        ]

        support_group.permissions.set(
            Permission.objects.filter(
                codename__in=support_permissions
            )
        )

        support_group.permissions.add(*dashboard_permissions)

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "✓ Roles created successfully."
            )
        )
        self.stdout.write("")