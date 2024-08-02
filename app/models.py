from uuid import uuid4
import uuid
from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()
class Profile(models.Model):
    username = models.CharField(max_length=15, default=None, unique=True)
    firstName = models.CharField(max_length=10, default=None, null=False)
    lastName = models.CharField(max_length=10, default=None, null=False)
    email = models.EmailField(max_length=50, unique=True, default=None, null=False)
    phone = models.CharField(max_length=15, default=None, blank=True)
    bio = models.TextField(max_length=300, default=None, blank=True, null=True)
    hobbies = models.TextField(max_length=200, default=None, blank=True, null=True)
    kyc_verification = models.BooleanField(default=False)
    wallet_balance = models.FloatField(max_length=None, default=None, blank=True, null=True)
    total_deposit = models.FloatField(max_length=None, default=None, blank=True, null=True)
    total_withdraw = models.FloatField(max_length=None, default=None, blank=True, null=True)
    total_profit = models.FloatField(max_length=None, default=None, blank=True, null=True)
    choices = (('Active', 'Active'),('Inactive', 'Inactive'), ('Suspended', 'Suspended'))
    status = models.CharField(max_length=15, choices=choices, default='Inactive')
    img = models.ImageField(upload_to='user/img', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', default=None, blank=True )
    is_admin = models.BooleanField(default=False)
    created_at = models.DateField(auto_now=True)

    def __str__(self) -> str:
        return self.username

class Kyc(models.Model):
    user = models.OneToOneField(Profile, related_name='owner', on_delete=models.CASCADE)
    choices = (("Driver's License", "Driver's License"), ("Passport", "Passport"), ("State ID", "State ID"))
    id_type = models.CharField(default=None, choices=choices, max_length=20, blank=True)
    id_number = models.CharField(max_length=20, default=None, unique=True)
    expiry_date = models.DateField(default=None)
    front_img = models.ImageField(upload_to='kyc/img', blank=True, null=True)
    back_img = models.ImageField(upload_to='kyc/img', blank=True, null=True)


class Plan(models.Model):
    planName = models.CharField(max_length=15, default=None, unique=True)
    maxPrice = models.IntegerField(default=None, blank=False, null=False)
    minPrice = models.IntegerField(default=None, blank=False, null=False)
    profit = models.CharField(max_length=20, default=None)
    planDuration = models.IntegerField(default=None, blank=False, null=False)
    choices = (('Pending', 'Pending'), ('Failed', 'Failed'), ('Active', 'Active'), ('Completed', 'Completed'))
    status = models.CharField(max_length=15, choices=choices, default='Pending', blank=False, null=False)
    users = models.ManyToManyField(Profile, related_name='plan', blank=True)
    created_at = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.planName

class Wallet(models.Model):
    wallet_name = models.CharField(max_length=10, default=None, blank=False)
    wallet_slug = models.CharField(max_length=10, default=None, blank=True, null=True)
    wallet_address = models.CharField(max_length=100, default=None, blank=True, null=True)
    logo_img = models.ImageField(upload_to='wallet', blank=True, null=True)
    qrcode_img = models.ImageField(upload_to='wallet', blank=True, null=True)
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
 
class TransactionHistory(models.Model):
    tr_no = models.CharField(max_length=50, primary_key=True, default=uuid.uuid4)
    date_created = models.DateField(auto_now=True)
    transaction_type = models.CharField(max_length=10, default=None, blank=True, null=False)
    amount = models.CharField(max_length=100, default=None, blank=True)
    choices = (('Pending', 'Pending'), ('Failed', 'Failed'), ('Completed', 'Completed'))
    payment_method = models.CharField(max_length=20, default=None, blank=False, null=False)
    status = models.CharField(max_length=10, choices=choices, default='Pending')
    deposit_img = models.ImageField(upload_to='wallet', blank=True, null=True)
    wallet_address = models.CharField(max_length=100, default=None, blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='transaction', blank=True)
    def __str__(self) -> str:
        return f"{self.date_created} |{self.transaction_type} by {self.user}"
    
