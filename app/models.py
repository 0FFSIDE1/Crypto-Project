from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=15, default=None, unique=True)
    firstName = models.CharField(max_length=10, default=None, null=False)
    lastName = models.CharField(max_length=10, default=None, null=False)
    email = models.EmailField(max_length=50, unique=True, default=None, null=False)
    phone = models.CharField(max_length=15, default=None, blank=True)
    kyc_verification = models.BooleanField(default=False)
    total_deposit = models.FloatField(max_length=None, default=None, blank=True, null=True)
    total_withdraw = models.FloatField(max_length=None, default=None, blank=True, null=True)
    total_profit = models.FloatField(max_length=None, default=None, blank=True, null=True)
    choices = (('Active', 'Active'),('Inactive', 'Inactive'), ('Suspended', 'Suspended'), ('Pending Review', 'Pending Review'))
    status = models.CharField(max_length=15, choices=choices, default='Inactive')
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.username
    

class Plan(models.Model):
    planName = models.CharField(max_length=15, default=None, unique=True)
    maxPrice = models.IntegerField(default=None, blank=False, null=False)
    minPrice = models.IntegerField(default=None, blank=False, null=False)
    planDuration = models.IntegerField(default=None, blank=False, null=False)
    users = models.ManyToManyField(User, related_name='user')
    created_at = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return f'{self.planName} | {self.planPrice}'

class Wallet(models.Model):
    wallet_name = models.CharField(max_length=10, default=None, blank=False)
    wallet_slug = models.CharField(max_length=10, default=None, blank=True, null=True)
    wallet_address = models.CharField(max_length=100, default=None, blank=True, null=True)
    def __str__(self) -> str:
        return f'{self.wallet_name} | {self.wallet_slug}'

class BankAccount(models.Model):
    bank_name = models.CharField(max_length=10, default=None, blank=True, null=True)
    bank_address = models.CharField(max_length=10, default=None)
    owner = models.CharField(max_length=10, default=None)
    routing_no = models.CharField(max_length=25, default=None, blank=True, null=True)
    accout_no = models.CharField(max_length=20, default=None)
    def __str__(self) -> str:
        return f'{self.bank_name} | {self.owner}'

class Transaction(models.Model):
    name = models.CharField(max_length=10, default=None, null=False, blank=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plan')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    transactionAmount = models.IntegerField(default=None, blank=False, null=False)
    def __str__(self) -> str:
        return f"{self.name} by {self.user}"