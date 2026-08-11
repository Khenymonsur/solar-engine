from decimal import Decimal


class BillOfMaterialsService:
    """
    Builds a Bill of Materials (BOM) from the
    RecommendationEngine output.
    """

    VAT_RATE = Decimal("0.075")  # 7.5%

    def __init__(self, recommendation):
        self.recommendation = recommendation

    def _build_item(self, product, quantity):
        """
        Create a single BOM line item.
        """

        if not product or quantity <= 0:
            return None

        unit_price = Decimal(str(getattr(product, "price", 0) or 0))
        line_total = unit_price * Decimal(quantity)

        return {
            "category": (
                product._meta.verbose_name.title()
                if hasattr(product, "_meta")
                else product.__class__.__name__
            ),
            "manufacturer": (
                str(product.manufacturer)
                if getattr(product, "manufacturer", None)
                else ""
            ),
            "model": getattr(product, "model", ""),
            "description": str(product),
            "specification": self._get_specification(product),
            "quantity": quantity,
            "unit": "pcs",
            "unit_price": unit_price,
            "total": line_total,
            "currency": "NGN",
            "warranty": getattr(product, "warranty", None),
        }

    def _get_specification(self, product):
        """
        Return a human-readable specification.
        """

        if hasattr(product, "wattage"):
            return f"{product.wattage}W"

        if hasattr(product, "capacity_ah"):
            return (
                f"{product.voltage}V / "
                f"{product.capacity_ah}Ah"
            )

        if hasattr(product, "capacity_kva"):
            return f"{product.capacity_kva} kVA"

        if hasattr(product, "current_rating"):
            return (
                f"{product.voltage}V / "
                f"{product.current_rating}A"
            )

        return "-"

    def generate(self):
        """
        Generate the complete Bill of Materials.
        """

        items = []

        components = [

            (
                self.recommendation.get("panel"),
                self.recommendation.get("panel_quantity", 0),
            ),

            (
                self.recommendation.get("battery"),
                self.recommendation.get("battery_quantity", 0),
            ),

            (
                self.recommendation.get("inverter"),
                self.recommendation.get("inverter_quantity", 0),
            ),

            (
                self.recommendation.get("controller"),
                self.recommendation.get("controller_quantity", 0),
            ),

        ]

        for product, quantity in components:

            item = self._build_item(product, quantity)

            if item:
                items.append(item)

        subtotal = sum(
            (item["total"] for item in items),
            Decimal("0"),
        )

        vat = subtotal * self.VAT_RATE

        grand_total = subtotal + vat

        return {
            "items": items,
            "item_count": len(items),
            "subtotal": subtotal,
            "vat": vat,
            "grand_total": grand_total,
        }