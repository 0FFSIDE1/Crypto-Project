from django.db import models

# Create your models here.
class User(models.Model):
    username = models.CharField(max_length=15, default=None, unique=True)
    firstName = models.CharField(max_length=10, default=None, null=False)
    lastName = models.CharField(max_length=10, default=None, null=False)
    email = models.EmailField(max_length=50, unique=True, default=None, null=False)
    phone = models.CharField(max_length=15, default=None, blank=True, null=False)
    created_at = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return self.username
    

class Plan(models.Model):
    planName = models.CharField(max_length=15, default=None, unique=True)
    planPrice = models.IntegerField(default=None, blank=False, null=False)
    planDuration = models.IntegerField(default=None, blank=False, null=False)
    users = models.ManyToManyField(User, related_name='user')
    created_at = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return f'{self.planName} | {self.planPrice}'

class Transaction(models.Model):
    name = models.CharField(max_length=10, default=None, null=False, blank=False)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE, related_name='plan')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='users')
    transactionAmount = models.IntegerField(default=None, blank=False, null=False)
    def __str__(self) -> str:
        return f"{self.name} by {self.user}"