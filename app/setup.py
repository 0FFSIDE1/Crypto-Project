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
    new_balance = float(balance) - float(amount)
    user.wallet_balance = new_balance
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
    
def approve_deposit(id, user):
    deposit = TransactionHistory.objects.get(tr_no=id)
    deposit.status = 'Completed'
    deposit.save()
    user = Profile.objects.get(user=user)
    user.wallet_balance = float(user.wallet_balance) + float(deposit.amount)
    user.save()


def decline_deposit(id, user):
    deposit = TransactionHistory.objects.get(tr_no=id)
    deposit.status = 'Failed'
    deposit.save()
    user = Profile.objects.get(user=user)
    user.total_deposit = float(user.total_deposit) - float(deposit.amount)
    user.save()

def approve_withdraw(id, user):
    withdraw = TransactionHistory.objects.get(tr_no=id)
    withdraw = 'Completed'
    withdraw.save()
    user = Profile.objects.get(user=user)
    user.total_withdraw = float(user.total_withdraw) + float(withdraw.amount)
    user.save()

def decline_withdraw(id):
    withdraw = TransactionHistory.objects.get(tr_no=id)
    withdraw = 'Failed'
    withdraw.save()

def approve_plan(user):
    user = Profile.objects.get(user=user)
    plan = Plan.objects.get(users=user)
    plan.status = 'Active'
    plan.save()

def decline_plan(user):
    user = Profile.objects.get(user=user)
    plan = Plan.objects.get(users=user)
    plan.status = 'Failed'
    plan.save()

def is_admin(user):
    if user.profile.is_admin:
        return True
    else:
        return False

def kyc_verification(user):
    try:
        kyc = Kyc.objects.all()
        for k in kyc:
            if k.user == user:
                profile = Profile.objects.get(user=user)
                profile.kyc_verification = True
                profile.save()
                return True
    except Exception as e:
        return e
    
        
