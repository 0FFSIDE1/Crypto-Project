from uuid import uuid4
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
    img = models.ImageField(upload_to='user/img', blank=True, null=True)
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.username

class Kyc(models.Model):
    user = models.OneToOneField(User, related_name='owner', on_delete=models.CASCADE)
    choices = (("Driver's License", "Driver's License"), ("Passport", "Passport"), ("State ID", "State ID"))
    id_type = models.CharField(default=None, choices=choices, max_length=20, blank=True)
    id_number = models.CharField(max_length=20, default=None)
    expiry_date = models.DateField(default=None)
    front_img = models.ImageField(upload_to='kyc/img', blank=True, null=True)
    back_img = models.ImageField(upload_to='kyc/img', blank=True, null=True)


class Plan(models.Model):
    planName = models.CharField(max_length=15, default=None, unique=True)
    maxPrice = models.IntegerField(default=None, blank=False, null=False)
    minPrice = models.IntegerField(default=None, blank=False, null=False)
    profit = models.CharField(max_length=20, default=None)
    planDuration = models.IntegerField(default=None, blank=False, null=False)
    users = models.ManyToManyField(User, related_name='user', blank=True)
    created_at = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.planName

class Wallet(models.Model):
    wallet_name = models.CharField(max_length=10, default=None, blank=False)
    wallet_slug = models.CharField(max_length=10, default=None, blank=True, null=True)
    wallet_address = models.CharField(max_length=100, default=None, blank=True, null=True)
    img = models.ImageField(upload_to='wallet', blank=True, null=True)
    def __str__(self) -> str:
        return f'{self.wallet_name} | {self.wallet_slug}'

class BankAccount(models.Model):
    bank_name = models.CharField(max_length=10, default=None, blank=True, null=False)
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
    
class TransactionHistory(models.Model):
    tr_no = models.UUIDField(primary_key=True)
    data_created = models.DateField(auto_now=True)
    transaction_type = models.CharField(max_length=10, default=None, blank=True, null=False)
    amount = models.CharField(max_length=100, default=None, blank=True)
    choices = (('Pending', 'Pending'), ('Failed', 'Failed'), ('Completed', 'Completed'))
    payment_method = models.CharField(max_length=20, default=None, blank=False, null=False)
    status = models.CharField(max_length=10, choices=choices, default='Pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transaction', blank=True)
    def __str__(self) -> str:
        return f"{self.transaction_type} by {self.user}"
    
