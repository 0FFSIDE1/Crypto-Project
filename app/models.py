import random
import uuid
from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.conf import settings

# Create your models here.

User = get_user_model()
class Profile(models.Model):
    username = models.CharField(max_length=15, default=None, unique=True)
    firstName = models.CharField(max_length=10, default=None, null=False)
    lastName = models.CharField(max_length=10, default=None, null=False)
    email = models.EmailField(max_length=50, unique=True, default=None, null=False)
    phone = models.CharField(max_length=15, default=None, blank=True)
    address =models.CharField(max_length=100, default=None, blank=True, null=True)
    dob = models.DateField(default=None, blank=True, null=True)
    bio = models.TextField(max_length=300, default=None, blank=True, null=True)
    hobbies = models.TextField(max_length=200, default=None, blank=True, null=True)
    kyc_verification = models.BooleanField(default=False)
    wallet_balance = models.DecimalField(max_digits=10000000000, decimal_places=2, default=None, blank=True, null=True)
    total_deposit = models.DecimalField(max_digits=10000000000, decimal_places=2, default=None, blank=True, null=True)
    total_withdraw = models.DecimalField(max_digits=1000000000, decimal_places=2, default=None, blank=True, null=True)
    total_profit = models.DecimalField(max_digits=1000000000, decimal_places=2, default=None, blank=True, null=True)
    choices = (('Active', 'Active'),('Inactive', 'Inactive'), ('Suspended', 'Suspended'))
    status = models.CharField(max_length=15, choices=choices, default='Inactive')
    img = models.ImageField(upload_to='user/img', blank=True, null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user', default=None, blank=True )
    is_admin = models.BooleanField(default=False)
    referral_code = models.CharField(max_length=10, unique=True, blank=True)
    referral_bonus = models.DecimalField(max_digits=190000000, decimal_places=2, default=None, blank=True, null=True)
    created_at = models.DateField(auto_created=True, auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = self.generate_referral_code()
        super().save(*args, **kwargs)

    def generate_referral_code(self):
        # Generate a unique referral code
        return str(uuid.uuid4())[:10]

    def get_referral_link(self):
        
        return f"{settings.SITE_URL}{reverse('register_with_referral', args=[self.referral_code])}"

    def __str__(self) -> str:
        return self.username

class OTP(models.Model):
    code = models.CharField(max_length=6, blank=True)
    user = models.OneToOneField(Profile, on_delete=models.CASCADE, related_name='otp')

    def __str__(self):
        return str(self.code)

    def save(self, *args, **kwargs):
        code_list = [x for x in range(10)]
        code_items = []
        for i in range(5):
            num = random.choice(code_list)
            code_items.append(num)
        code = "".join(str(n) for n in code_items)
        self.code = code
        super().save(*args, **kwargs)    


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
    maxPrice = models.CharField(max_length=100,default=None, blank=False, null=False)
    minPrice = models.CharField(max_length=100,default=None, blank=False, null=False)
    profit = models.CharField(max_length=100, default=None)
    planDuration = models.CharField(max_length=20,default=None, blank=False, null=False)
    user = models.ManyToManyField(Profile, related_name='plan', default=None, blank=True)
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
    date_created = models.DateTimeField(auto_created=True)
    transaction_type = models.CharField(max_length=10, default=None, blank=True, null=False)
    amount = models.CharField(max_length=100, default=None, blank=True, null=False)
    choices = (('Pending', 'Pending'), ('Failed', 'Failed'),('Ongoing', 'Ongoing'), ('Completed', 'Completed'))
    planName = models.CharField(max_length=20, default=None, blank=True, null=True)
    payment_method = models.CharField(max_length=20, default=None, blank=False, null=True)
    status = models.CharField(max_length=10, choices=choices, default='Pending')
    deposit_img = models.ImageField(upload_to='wallet', blank=True, null=True)
    wallet_address = models.CharField(max_length=100, default=None, blank=True, null=True)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='transaction', blank=True)
    def __str__(self) -> str:
        return f"{self.date_created} |{self.transaction_type} by {self.user}"
    
class Expert(models.Model):
    name =  models.CharField(default=None, max_length=20, blank=True, null=True)
    gains =  models.CharField(default=None, max_length=20, blank=True)
    copiers = models.CharField(default=None, max_length=20, blank=True)
    commision = models.CharField(default=None, max_length=20, blank=True)
    profit = models.CharField(default=None, max_length=20, blank=True)
    loss = models.CharField(default=None, max_length=20, blank=True)
    choices = (('Expert', 'Expert'), ('Moderate', 'Moderate'), ('Risk Trader', 'Risk Trader'), ('Conservative', 'Conservative')) 
    category = models.CharField(default=None, choices=choices, max_length=20, blank=True)
    risk = models.CharField(default=None, max_length=20, blank=True)
    planName =  models.ForeignKey(Plan, default=None, on_delete=models.CASCADE, related_name='expert', blank=True)
    def __str__(self) -> str:
        return f"{self.category} | {self.name}"