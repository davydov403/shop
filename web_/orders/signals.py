from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Order, OrderItem, InsufficientStockError

@receiver(post_save, sender=Order)
def order_post_save(sender, instance, **kwargs):
    print(f"Order {instance.id} saved. Status: {instance.status}")
    if instance.status == 'canceled':
        order_items = instance.orderitem_set.all()
        for order_item in order_items:
            order_item.product.stock += order_item.count
            order_item.product.save()
            print(f"Returned {order_item.count} items to stock for Product {order_item.product.id}")
    elif instance.status == 'active':
        order_items = instance.orderitem_set.all()
        for order_item in order_items:
            order_item.product.stock -= order_item.count
            order_item.product.save()
            print(f"Deducted {order_item.count} items from stock for Product {order_item.product.id}")


@receiver(post_save, sender=OrderItem)
@receiver(post_delete, sender=OrderItem)
def update_stock(sender, instance, **kwargs):
    product = instance.product
    try:
        product.stock = product.calculate_stock(instance.count)
        product.save()
    except InsufficientStockError as e:
        print(f"Error: {e}")