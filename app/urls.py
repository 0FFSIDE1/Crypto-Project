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
    path('accounts/wallet/<int:pk>/plan', get_plan, name='get-plan'),
    path('accounts/wallet/<str:pk>/deposit', deposit, name='deposit'),
    path('accounts/wallet/confirm-deposit', confirm_deposit, name='confirm-deposit'),
    path('accounts/wallet/withdraw', withdraw, name='withdraw'),
    path('accounts/wallet/<str:pk>/transaction', transaction_detail, name='transaction-detail'),
    path('accounts/wallet/kyc-verification', verify_kyc, name='kyc-verification'),
    path('accounts/wallet/update/profile', update_profile, name='update-profile'),
    path('accounts/wallet/invest', buy_plan, name='buy-plan'),
    
]
