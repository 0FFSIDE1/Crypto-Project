from .models import *

def insufficient_balance(amount, user):
    user = Profile.objects.get(user=user)
    balance = user.wallet_balance
    if balance == None:
        balance = 0
    if float(amount) > float(balance):
        return True
    else:
        return False

def withdraw_funds(amount, user):
    user = Profile.objects.get(username=user)
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
    
def check_balance_for_plan(wallet_balance, plan_name, request_amount):
    plan = Plan.objects.get(planName=plan_name)
    if float(wallet_balance) < float(plan.minPrice):
        return False
    elif float(request_amount) < float(plan.minPrice) or float(request_amount) > float(plan.maxPrice):
        return False
    else:
        return True
    
def approve_deposit(id, user):
    deposit = TransactionHistory.objects.get(tr_no=id)
    deposit.status = 'Completed'
    deposit.save()
    user = Profile.objects.get(username=user)
    if user.wallet_balance is None:
        user.wallet_balance = 0
    
    balance = float(user.wallet_balance) + float(deposit.amount)
    user.wallet_balance = balance
    user.save()
    print(user.wallet_balance)
    print(deposit.amount)


def decline_deposit(id, user):
    deposit = TransactionHistory.objects.get(tr_no=id)
    deposit.status = 'Failed'
    deposit.save()
    user = Profile.objects.get(username=user)
    user.total_deposit = float(user.total_deposit) - float(deposit.amount)
    user.save()

def approve_withdraw(id, user):
    withdraw = TransactionHistory.objects.get(tr_no=id)
    withdraw.status = 'Completed'
    withdraw.save()
    profile = Profile.objects.get(username=user)
    if profile.total_withdraw == None:
        profile.total_withdraw = 0
    profile.total_withdraw = float(profile.total_withdraw) + float(withdraw.amount)
    profile.save()
    withdraw_funds(amount=withdraw.amount, user=user)

def decline_withdraw(id):
    withdraw = TransactionHistory.objects.get(tr_no=id)
    withdraw.status = 'Failed'
    withdraw.save()

def approve_invest(id):
    plan = TransactionHistory.objects.get(tr_no=id)
    plan.status = 'Completed'
    plan.save()

def decline_invest(id):
    plan = TransactionHistory.objects.get(tr_no=id)
    plan.status = 'Failed'
    plan.save()
    
def is_admin(user):
    if user.user.is_admin:
        return True
    else:
        return False

def kyc_verification(user):
    try:
        kyc = Kyc.objects.all()
        profile = Profile.objects.get(user=user)
        for k in kyc:
            if k.user == user:
                profile.kyc_verification = True
                profile.save()
                return True
    except Exception as e:
        return e
    
        
