from django.urls import path
from .views import *


urlpatterns = [
    path('accounts/wallet/dashboard', dashboard, name='dashboard'),
    path('accounts/wallet/deposit', deposit_withdraw, name='deposit-withdraw'),
    path('accounts/wallet/transactions', transaction_history, name='transaction'),
    path('accounts/wallet/copy-trading', copy_trading, name='copytrading'),
    path('accounts/wallet/plans', plans, name='plans'),
    path('accounts/wallet/settings', settings, name='settings'),
    path('accounts/wallet/referrals', referral, name='referral'),
]