# myapp/apps.py
from django.apps import AppConfig


class PaymentPlansConfig(AppConfig):
    name = 'beer.apps.payment_plans'

    def ready(self):
        from .receivers import (on_charge_succeeded, on_charge_refunded, on_charge_failed, on_subscription_created, on_subscription_deleted)
