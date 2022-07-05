from django.db import models
from core.models import CoreModel
from django.contrib.postgres.fields import ArrayField
from config.settings import STRIPE_TVA_TAX_RATE as TAX_RATE


class Plan(CoreModel):
    name = models.CharField(max_length=150)
    description = ArrayField(models.TextField(null=True))
    duration = models.CharField(max_length=150, null=True)
    initial_price = models.FloatField(blank=True, null=True)
    price = models.FloatField()
    product_stripe_id = models.CharField(max_length=150, null=True)
    stripe_id = models.CharField(max_length=150, null=True)
    deleted = models.BooleanField(default=False)

    class Meta:
        db_table = "plans"
        ordering = ["price"]


class Pack(CoreModel):
    name = models.CharField(max_length=150)
    number_credits = models.IntegerField()
    description = ArrayField(models.TextField(null=True))
    initial_price = models.FloatField(blank=True, null=True)
    price = models.FloatField()
    deleted = models.BooleanField(default=False)
    product_stripe_id = models.CharField(max_length=150, null=True)
    price_stripe_id = models.CharField(max_length=150, null=True)

    class Meta:
        db_table = "packs"
        ordering = ["price"]


class PaymentHistory(CoreModel):
    data = models.DateTimeField()
    description = models.TextField()
    price = models.FloatField()
    number_of_credits = models.IntegerField(default=0)
    duration = models.CharField(max_length=100, default="")
    paid = models.BooleanField(default=False)
    tax_rate = models.FloatField(blank=True, null=True)
    tax_amount = models.FloatField(blank=True, null=True)
    total_price = models.FloatField(blank=True, null=True)

    class Meta:
        db_table = "payment_history"

    def save(self, *args, **kwargs):
        self.tax_rate = TAX_RATE
        self.tax_amount = self.price * TAX_RATE / 100
        self.total_price = self.price + self.tax_amount
        super().save(*args, **kwargs)
