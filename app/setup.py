from .models import *

def insufficient_balance(amount, user):
    user = Profile.objects.get(user=user)
    balance = user.wallet_balance
    if balance == None or float(amount) > balance:
        return True
    else:
        return False

def withdraw_funds(amount, user):
    user = Profile.objects.get(user=user)
    balance = user.wallet_balance
    withdraw = float(balance) - float(amount)
    user.wallet_balance = withdraw
    user.save()


def check_kyc_verification(user):
    user = Profile.objects.get(user=user)
    if user.kyc_verification:
        return True
    else:
        return False
    
def check_balance_for_plan(wallet_balance, plan_name):
    plan = Plan.objects.get(planName=plan_name)
    if float(wallet_balance) < plan.minPrice or wallet_balance > plan.maxPrice:
        return False
    else:
        return True