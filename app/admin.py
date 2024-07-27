from django.contrib import admin
from .models import User, Plan, Transaction, Wallet

# Register your models here.
admin.site.register(User)
admin.site.register(Plan)
admin.site.register(Transaction)
admin.site.register(Wallet)
