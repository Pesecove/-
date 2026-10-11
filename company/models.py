from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    """Кастомный пользователь с разделением ролей"""
    SUPPLIER = 'supplier'
    CONSUMER = 'consumer'
    
    ROLE_CHOICES = [
        (SUPPLIER, 'Поставщик'),
        (CONSUMER, 'Потребитель'),
    ]
    
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CONSUMER)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

class Warehouse(models.Model):
    """Модель Склада"""
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

class Product(models.Model):
    """Модель Товара"""
    name = models.CharField(max_length=255)
    sku = models.CharField(max_length=100, unique=True)

class WarehouseStock(models.Model):
    """Остатки товаров на конкретных складах"""
    warehouse = models.ForeignKey(Warehouse, on_delete=models.CASCADE, related_name='stocks')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('warehouse', 'product')