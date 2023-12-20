from django.db import models
from django.contrib.auth.models import User

class InsufficientStockError(Exception):
    pass

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    products = models.ManyToManyField('Product', through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey('Cart', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    count = models.PositiveIntegerField(default=1)
    discount = models.FloatField(default=0)
    cost = models.FloatField(default=0)

    def __str__(self):
        return f"CartItem {self.id} - {self.cart} - {self.product}"

class Manager(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    stock = models.IntegerField()
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    
    def __str__(self):
        return self.name

    def calculate_stock(self, count):
        """
        Вычисляет новый запас товара после заказа.
        """
        if self.stock < count:
            raise InsufficientStockError(f"Insufficient stock for product {self.id}. Available: {self.stock}, Requested: {count}")
        return self.stock - count
    
class Order(models.Model):
    customer = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    manager = models.ForeignKey(Manager, on_delete=models.SET_NULL, null=True)
    type = models.CharField(max_length=255, choices=[("online", "Online"), ("offline", "Offline")])
    status = models.CharField(max_length=255, choices=[("active", "Active"), ("completed", "Completed"), ("canceled", "Canceled")])

    def __str__(self):
        return f"Order {self.id} - {self.customer}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.IntegerField()
    discount = models.FloatField(default=0)
    cost = models.FloatField()

    def __str__(self):
        return f"OrderItem {self.id} - {self.order} - {self.product}"