from django.db import models
from billing.models import BillingProfile

ADDRESS_TYPES = (
    ('billing', 'Billing'),
    ('shipping', 'Shipping'),
)
class Address(models.Model):
    billing_profile = models.ForeignKey(BillingProfile, on_delete=models.CASCADE)
    address_type = models.CharField(max_length=160, choices=ADDRESS_TYPES)
    address_line_1 = models.CharField(max_length=160)
    address_line_2 = models.CharField(max_length=160, blank=True, null=True)
    city = models.CharField(max_length=160)
    state = models.CharField(max_length=160)
    country = models.CharField(max_length=160, default='United States of America')
    zip_code = models.CharField(max_length=160)

    def __str__(self):
        return f"{str(self.billing_profile)}'s address"

    def line_2(self):
        if self.address_line_2:
            return f'{self.address_line_2}\n'
        else:
            return ''
    def get_address(self):

        return f'{self.address_line_1},\n{self.line_2()}{self.city}, {self.state}, {self.zip_code}\n{self.country}'