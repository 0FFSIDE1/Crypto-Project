from django.contrib import admin
from .models import User, Plan, Transaction, Wallet, BankAccount, Kyc

# Register your models here.
admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Transaction)
admin.site.register(Wallet)
admin.site.register(BankAccount)
admin.site.register(Kyc)
