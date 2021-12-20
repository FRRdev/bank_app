from django.db import models
from django.conf import settings


class Bank(models.Model):
    name = models.CharField(max_length=120, unique=True)
    address = models.CharField(max_length=120, unique=True)
    year_of_foundation = models.PositiveIntegerField()
    director = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Currency(models.Model):
    bank = models.ForeignKey(Bank, on_delete=models.CASCADE, related_name='currencies',null=True,blank=True)
    code = models.CharField(max_length=3)
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="categories")
    name = models.CharField(max_length=32, blank=True)

    def __str__(self):
        return f'{self.name} - {self.user}'


class Transaction(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="transactions")
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, related_name="transactions")
    date = models.DateTimeField()
    description = models.TextField(blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True,
                                 related_name="transactions")

    def __str__(self):
        return f"{self.amount} {self.currency.code} {self.date}"


class AllowList(models.Model):
    ip_address = models.GenericIPAddressField()

    def __str__(self):
        return self.ip_address
