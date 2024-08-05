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
    path('accounts/wallet/admin/<str:pk>/transaction', admin_transaction_detail, name='admin-transaction-detail'),
    path('accounts/wallet/kyc-verification', verify_kyc, name='kyc-verification'),
    path('accounts/wallet/invest', buy_plan, name='buy-plan'),
    path('accounts/wallet/plan/create', create_plan, name='create-plan'),
    path('accounts/wallet/admin/users', all_users, name='all-users'),
    path('accounts/wallet/admin/<int:pk>/user-detail', user_detail, name='user-detail'),
    path('accounts/wallet/admin/plan/transactions', plan_transaction, name='plan-transaction'),
    path('accounts/wallet/admin/transaction/update', update_transaction, name='update-trc'),   
]
