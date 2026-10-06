from decimal import Decimal

class AssessmentSessionService:
    """
    Handles all Customer Assessment session operations.
    """

    SESSION_KEY = "assessment"

    # --------------------------------------------------
    # Session
    # --------------------------------------------------

    @classmethod
    def get(cls, request):
        return request.session.get(
            cls.SESSION_KEY,
            {}
        )

    @classmethod
    def save(cls, request, assessment):
        request.session[cls.SESSION_KEY] = assessment
        request.session.modified = True

    @classmethod
    def clear(cls, request):
        request.session.pop(
            cls.SESSION_KEY,
            None
        )
        request.session.modified = True

    # --------------------------------------------------
    # Wizard Steps
    # --------------------------------------------------

    @classmethod
    def save_customer(cls, request, data):

        assessment = cls.get(request)

        assessment["customer"] = data

        cls.save(request, assessment)

    @classmethod
    def save_property(cls, request, data):

        assessment = cls.get(request)

        assessment["property"] = data

        cls.save(request, assessment)

    @classmethod
    def save_power(
            cls,
            request,
            data,
    ):
        assessment = cls.get(request)

        power_data = {}

        for key, value in data.items():

            if isinstance(value, Decimal):
                power_data[key] = str(value)
            else:
                power_data[key] = value

        assessment["power"] = power_data

        cls.save(
            request,
            assessment,
        )

    # --------------------------------------------------
    # Appliance Handling
    # --------------------------------------------------

    @classmethod
    def appliance_list(cls, request):

        assessment = cls.get(request)

        return assessment.setdefault(
            "appliances",
            [],
        )

    @classmethod
    def add_appliance(
        cls,
        request,
        appliance_name,
        watts,
        quantity,
        hours_per_day,
    ):

        assessment = cls.get(request)

        appliances = assessment.setdefault(
            "appliances",
            [],
        )

        appliances.append({

            "id": len(appliances) + 1,

            "name": appliance_name,

            "watts": float(watts),

            "quantity": int(quantity),

            "hours_per_day": float(hours_per_day),

        })

        cls.save(request, assessment)

    @classmethod
    def remove_appliance(
        cls,
        request,
        appliance_id,
    ):

        assessment = cls.get(request)

        assessment["appliances"] = [

            item

            for item in assessment.get("appliances", [])

            if item["id"] != appliance_id

        ]

        cls.save(request, assessment)

    # --------------------------------------------------
    # Display Helpers
    # --------------------------------------------------

    @classmethod
    def selected_appliances(cls, request):

        assessment = cls.get(request)

        result = []

        for item in assessment.get("appliances", []):

            total_load = item["watts"] * item["quantity"]

            daily_energy = (

                total_load * item["hours_per_day"]

            ) / 1000

            result.append({

                "id": item["id"],

                "name": item["name"],

                "watts": item["watts"],

                "quantity": item["quantity"],

                "hours_per_day": item["hours_per_day"],

                "total": total_load,

                "daily_energy": daily_energy,

            })

        return result

    @classmethod
    def connected_load(cls, request):

        return sum(

            item["total"]

            for item in cls.selected_appliances(request)

        )

    @classmethod
    def daily_energy(cls, request):

        total = sum(

            item["daily_energy"]

            for item in cls.selected_appliances(request)

        )

        return round(total, 2)

    @classmethod
    def appliance_count(cls, request):

        return len(
            cls.selected_appliances(request)
        )