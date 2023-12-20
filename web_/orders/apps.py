from django.apps import AppConfig


class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    def ready(self):
        from .models import Order
        from . import signals
        signals.post_save.connect(signals.order_post_save, sender=Order)