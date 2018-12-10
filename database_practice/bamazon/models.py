from django.db import models

# Create your models here.

class Item(models.Model):
    def __str__(self):
        return self.product_name
    product_name = models.CharField(max_length=200)
    department_name = models.CharField(max_length=200)
    price = models.FloatField()
    stock = models.IntegerField()

class Departments(models.Model):
    def __str__(self):
        return self.department_name
    department_name = models.CharField(max_length=200)
    over_head_costs = models.IntegerField()
    product_sales = models.IntegerField(default=0)