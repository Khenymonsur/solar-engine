from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission


class Command(BaseCommand):
    help = "Create default roles and assign permissions."

    DASHBOARD_PERMISSIONS = [
        "view_userprofile",
        "view_userpreference",
        "view_analytics",
    ]

    ROLES = {

        "Engineer": [

            "view_customer",
            "add_customer",
            "change_customer",
            "delete_customer",

            "view_assessment",
            "add_assessment",
            "change_assessment",
            "delete_assessment",

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

            "view_quotation",
            "add_quotation",
            "change_quotation",
        ],

        "Sales Executive": [

            "view_customer",
            "add_customer",
            "change_customer",

            "view_assessment",

            "view_quotation",
            "add_quotation",
            "change_quotation",

        ],

        "Finance": [

            "view_quotation",
            "change_quotation",
            "view_assessment",
        ],

        "Customer Service": [

            "view_customer",
            "add_customer",
            "change_customer",

            "view_assessment",

            "view_quotation",
        ],
    }

    def assign_permissions(self, group, codenames):

        requested = set(codenames)

        permissions = Permission.objects.filter(
            codename__in=codenames
        )

        found = set(
            permissions.values_list(
                "codename",
                flat=True,
            )
        )

        missing = requested - found

        if missing:
            self.stdout.write(

                self.style.WARNING(

                    f"⚠ {group.name}: Missing permissions -> "

                    f"{', '.join(sorted(missing))}"

                )

            )

        group.permissions.set(permissions)

        self.stdout.write(

            self.style.SUCCESS(

                f"✔ {group.name:<20}"

                f"{permissions.count()} permissions"

            )

        )

    def handle(self, *args, **options):

        self.stdout.write("")
        self.stdout.write(
            self.style.NOTICE("Setting up roles...")
        )
        self.stdout.write("")

        administrator, _ = Group.objects.get_or_create(
            name="Administrator"
        )

        administrator.permissions.set(
            Permission.objects.all()
        )

        self.stdout.write(
            self.style.SUCCESS(
                f"✔ Administrator        "
                f"{Permission.objects.count()} permissions"
            )
        )

        dashboard_permissions = list(
            Permission.objects.filter(
                codename__in=self.DASHBOARD_PERMISSIONS
            )
        )

        for role, permissions in self.ROLES.items():

            group, _ = Group.objects.get_or_create(
                name=role
            )

            self.assign_permissions(
                group,
                permissions,
            )

            group.permissions.add(*dashboard_permissions)

        self.stdout.write("")
        self.stdout.write(
            self.style.SUCCESS(
                "Roles created successfully."
            )
        )
        self.stdout.write("")