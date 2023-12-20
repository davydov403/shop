from django.contrib import admin
from .models import Manager, Product, Order, OrderItem

admin.site.register(Manager)
admin.site.register(Product)
admin.site.register(Order)
admin.site.register(OrderItem)
