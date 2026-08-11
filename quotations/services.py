from django.db import transaction

from services.recommendation import RecommendationEngine
from services.bom import BillOfMaterialsService

from .models import Quotation, QuotationItem


class QuotationService:

    @staticmethod
    @transaction.atomic
    def create_from_assessment(assessment):

        recommendation = RecommendationEngine(
            assessment
        ).recommend()

        bom = BillOfMaterialsService(
            recommendation
        ).generate()

        quotation, created = Quotation.objects.get_or_create(
            assessment=assessment,
            defaults={
                "customer": assessment.customer,
                "subtotal": bom["subtotal"],
                "vat": bom["vat"],
                "grand_total": bom["grand_total"],
                "status": "draft",
            },
        )

        if not created:
            quotation.customer = assessment.customer
            quotation.subtotal = bom["subtotal"]
            quotation.vat = bom["vat"]
            quotation.grand_total = bom["grand_total"]
            quotation.status = "draft"
            quotation.save()

            quotation.items.all().delete()

        for item in bom["items"]:
            QuotationItem.objects.create(
                quotation=quotation,
                category=item["category"],
                manufacturer=item["manufacturer"],
                model=item["model"],
                specification=item["specification"],
                description=item["description"],
                quantity=item["quantity"],
                unit_price=item["unit_price"],
                total=(
                    item["quantity"] *
                    item["unit_price"],
                )
            )
        return quotation
