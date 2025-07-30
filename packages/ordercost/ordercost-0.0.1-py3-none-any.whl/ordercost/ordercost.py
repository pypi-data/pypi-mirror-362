class OrderCostCalculator:
    def __init__(self, price_per_unit, quantity, tax_percent=0, discount_percent=0):
        self.price_per_unit = price_per_unit
        self.quantity = quantity
        self.tax_percent = tax_percent
        self.discount_percent = discount_percent

    def base_cost(self):
        return self.price_per_unit * self.quantity

    def discount_amount(self):
        return (self.discount_percent / 100) * self.base_cost()

    def tax_amount(self):
        return (self.tax_percent / 100) * (self.base_cost() - self.discount_amount())

    def total_cost(self):
        return self.base_cost() - self.discount_amount() + self.tax_amount()

    def breakdown(self):
        return {
            "base_cost": round(self.base_cost(), 2),
            "discount": round(self.discount_amount(), 2),
            "tax": round(self.tax_amount(), 2),
            "total": round(self.total_cost(), 2)
        }
