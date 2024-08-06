from django.shortcuts import redirect, render
from django.http import JsonResponse
from .models import *
from django.contrib import messages
from .setup import *
from django.db.models import Q
# Create your views here.

def dashboard(request):
    return render(request, 'app/user_dashboard.html')

def deposit_withdraw(request):
    user = Profile.objects.get(user=request.user)
    context = {
        'wallets': Wallet.objects.all(),
        'banks': BankAccount.objects.all(),
        'user': user
    }
    return render(request, 'app/deposit_withdraw.html', context)

def deposit(request, pk):
    wallets = Wallet.objects.get(wallet_name=pk)
    context ={
        "wallet": wallets
    }
    return render(request,'app/deposit.html', context)

def confirm_deposit(request):
    user = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        transaction = TransactionHistory.objects.create(
            user=user,
            amount=request.POST['amount'],
            transaction_type='Deposit',
            payment_method=request.POST['wallet_name'],
            deposit_img = request.FILES.get('payment_slip'),
            wallet_address = request.POST['wallet_address']
        )
        transaction.save()
        if user.total_deposit == None:
            user.total_deposit = 0.00
        user.save()
        print(user.total_deposit)
        total_deposit = float(user.total_deposit) + float(transaction.amount)
        user.total_deposit = total_deposit
        user.status = 'Active'
        user.save()
        messages.success(request, 'Processing Payment, this should take few mintues')
    return redirect('transaction')

def update_transaction(request):
    pk = request.POST['transaction_id']
    tr_type = request.POST['transaction_type']
    status = request.POST.get('status', None)
    username = request.POST['user']
    if request.method == 'POST':
        if status is not None:
            if tr_type == 'Deposit' and status == 'Completed':       
                approve_deposit(id=pk, user=username)
            elif tr_type == 'Deposit' and status == 'Failed':
                decline_deposit(id=pk, user=username)
            elif tr_type == 'Withdraw' and status == 'Completed':
                approve_withdraw(id=pk, user=username)
            elif tr_type == 'Withdraw' and status == 'Failed':
                decline_withdraw(id=pk)
            elif tr_type == 'Invest' and status == 'Completed':
                approve_invest(id=pk)
            elif tr_type == 'Invest' and status == 'Failed':
                decline_invest(id=pk)
            elif tr_type == 'Invest' and status == 'Ongoing':
                tr = TransactionHistory.objects.get(tr_no=pk)
                tr.status = 'Ongoing'
                tr.save()
        
            if tr_type == 'Deposit' or tr_type == 'Withdraw':
                messages.success(request, 'Updated Successfully')
                return redirect('transaction')
            else:
                messages.success(request, 'Updated Successfully')
                return redirect('plan-transaction')
        else:
            if tr_type == 'Deposit' or tr_type == 'Withdraw':
                messages.error(request, 'Invalid Request, choose status')
                return redirect('transaction')
            else:
                messages.error(request, 'Invalid Request, choose status')
                return redirect('plan-transaction')
            


def withdraw(request):
    if request.method =='POST':
        amount = float(request.POST['amount'])
        wallet = request.POST.get('wallet')
        wallet_add = request.POST['wallet_add']
        if insufficient_balance(amount=amount, user=request.user):
            messages.error(request, 'Insufficient Balance')
            return redirect('deposit-withdraw')
        else:
            transaction = TransactionHistory.objects.create(
                user=Profile.objects.get(user=request.user),
                amount=amount,
                transaction_type='Withdraw',
                payment_method=wallet,
                wallet_address=wallet_add
            )
            transaction.save()
            messages.success(request, 'Withrawal processing, this may take few mintues!')
            return redirect('transaction')
        
def get_kyc(request, pk):
    kyc = Kyc.objects.get(pk=pk)
    data = {
        
        'name': kyc.user.username,
        'front_img': kyc.front_img.url if kyc.front_img else None,
        'back_img': kyc.back_img.url if kyc.back_img else None,

    }
    return JsonResponse(data, safe=False)


def kyc(request):
    kyc = Kyc.objects.all()
    context = {
        'kyc': kyc
    }        
    return render(request, 'app/pending.html', context)

def update_kyc(request):
    if request.method == 'POST':
        status = request.POST.get('status', None)
        print(status)
        if status is not None:
            user = request.POST['user']
            print(user)
            profile = Profile.objects.get(username=user)
            print(profile)
            try:
                profile.kyc_verification = True
                profile.save()
                messages.success(request, 'Update successfully')
                return redirect('view-kyc')
            except Exception as e:
                messages.error(request, f'{e}')
                return redirect('view-kyc')
        else:
            messages.error(request, 'Invalid Request!, choose status')
            return redirect('view-kyc')
    return redirect('view-kyc')


def verify_kyc(request):
    if request.method == 'POST':
        user = Profile.objects.get(user=request.user)
        try:
            kyc = Kyc.objects.create(
                user=user,
                id_type=request.POST['id_type'],
                id_number=request.POST['id_no'],
                front_img = request.FILES.get('front_img'),
                back_img = request.FILES.get('back_img'),
                expiry_date=request.POST['expiry_date']
            )
            kyc.save()
            messages.success(request, 'KYC Verification Processing, this may take a few days!')
            return redirect('settings')
        except Exception as e:
            messages.error(request, e)
            return render(request, 'app/kyc_verification.html')
    return render(request, 'app/kyc_verification.html')


def transaction_history(request):
    if is_admin(user=request.user):
        user = Profile.objects.get(user=request.user)
        transactions = TransactionHistory.objects.filter(Q(transaction_type='Deposit') | Q(transaction_type='Withdraw')).order_by('-date_created')
        context = {
            'transactions': transactions
        }
        return render(request, 'app/transaction.html', context)
    else:
        user = Profile.objects.get(user=request.user)
        transactions = TransactionHistory.objects.filter(user=user).order_by('-date_created')
        context = {
            'transactions': transactions
        }
        return render(request, 'app/transaction.html', context)

def transaction_detail(request, pk):
    transaction = TransactionHistory.objects.get(pk=pk)
    
    context = {
        'transaction': transaction
    }
    return render(request, 'app/transaction_detail.html', context)

def admin_transaction_detail(request, pk):
    transaction = TransactionHistory.objects.get(pk=pk)
    data = {
        'tr_no': transaction.tr_no,
        'transaction_type': transaction.transaction_type,
        'amount': transaction.amount,
        'user': transaction.user.username
    }
    return JsonResponse(data, safe=True)


def copy_trading(request):
    return render(request, 'app/copytrading.html')

def plans(request):
    context = {
        'plans': Plan.objects.all()
    }
    return render(request, 'app/plan&pricing.html', context)

def get_plan(request, pk):
    plan = Plan.objects.get(pk=pk)
    data = {
        'name': plan.planName,
        'profit': plan.profit
    }
    return JsonResponse(data, safe=True)

def buy_plan(request): 
        if request.method == 'POST':       
            try:
                if check_kyc_verification(user=request.user):
                    user = Profile.objects.get(user=request.user)
                    wallet_balance = user.wallet_balance
                    plan = request.POST['plan']
                    request_amount = request.POST['amount']
                   
                    if not insufficient_balance(amount=request_amount, user=request.user):
                        if check_balance_for_plan(wallet_balance=wallet_balance, plan_name=plan, request_amount=request_amount):
                            user.wallet_balance = float(wallet_balance) - float(request_amount)
                            user.save()
                            p = Plan.objects.get(planName=plan)
                            p.user.add(user)
                            p.save()
                            transaction = TransactionHistory.objects.create(transaction_type='Invest',
                            amount=float(request_amount), planName=plan, user=user, payment_method='Internal Transfer')
                            transaction.save()
                            messages.success(request, 'Processing investment, this should take only few mintues')
                            return redirect('transaction') 
                        else:
                            messages.error(request, 'Insufficient balance')
                            return redirect('plans')
                    else:
                        messages.error(request, 'Insufficient balance')
                        return redirect('plans')
                else:
                    messages.error(request, 'KYC Verification needed to perform action.')
                    return redirect('plans')              
            except Exception as e:
                messages.error(request, f'{e}')
                return redirect('plans')


def create_plan(request):
    if request.method == 'POST':
        try:
            plan_name = request.POST['plan_name']
            minp = request.POST['min_amount']
            maxp = request.POST['max_amount']
            profit = request.POST['profit']
            duration = request.POST['duration']
            plan = Plan.objects.create(
                planName=plan_name,
                minPrice=minp,
                maxPrice=maxp,
                profit=profit,
                planDuration=duration,
            )
            plan.save()
            messages.success(request, 'Successful, New Plan added!')
            return redirect('plans')
        except Exception as e:
            messages.error(request, f'{e}')
            return redirect('plans')
        
def all_users(request):
    users = Profile.objects.all()
    context = {
        'users': users
    }
    return render(request, 'app/users.html', context)

def user_detail(request, pk):
    users = Profile.objects.get(pk=pk)
    context = {
        'users': users,
    }
    return render(request, 'app/user_detail.html', context)

def get_user(request, pk):
    user = Profile.objects.get(pk=pk)
    data = {
        'username': user.username,
        'status': user.status,
        'pk': user.pk,
    }
    return JsonResponse(data, safe=True)


def update_user(request):
    if request.method == 'POST':
        try:
            pk = request.POST['myForm']
            user = Profile.objects.get(pk=pk)
            status = request.POST.get('status', None)
            user.status = status
            user.save()
            messages.success(request, 'User updated successfully!')
            return redirect('all-users')
        except Exception as e:
            messages.error(request, f'{e}')
            return redirect('all-users')


def make_user_admin(request, pk):
    user = Profile.objects.get(pk=pk)
    user.is_admin = True
    user.save()
    messages.success(request, 'User is Now an Admin!')
    return redirect('all-users')

def plan_transaction(request):
    transactions = TransactionHistory.objects.filter(transaction_type='Invest')
    context = {
        'transactions': transactions    
    }
    return render(request, 'app/plan_transaction.html', context)
def settings(request):
    user = Profile.objects.get(user=request.user)
    context = {
        'users': user,
        'plans': Plan.objects.filter(user=user)
    }
    if request.method == 'POST':
        try:
            profile = Profile.objects.get(user=request.user)
            profile.firstName = request.POST['firstName']
            profile.lastName = request.POST['lastName']
            profile.bio = request.POST['bio']
            profile.hobbies = request.POST['hobbies']
            profile.img = request.FILES.get('profile_photo')
            profile.address = request.POST['address']
            profile.phone = request.POST['phone']
            profile.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('settings')
        except Exception as e:
            messages.error(request, f'{e}')
            return redirect('settings')
    return render(request, 'app/my_account.html', context)


def referral(request):
    return render(request, 'app/referral.html')

def expert_traders(request):
    experts = Expert.objects.all()
    if request.method == 'POST':
        try:
            expert = Expert.objects.create(
                name=request.POST['name'],
                gains=request.POST['gains'],
                copiers=request.POST['copiers'],
                loss=request.POST['loss'],
                risk=request.POST['risk'],
                category=request.POST.get('category', None),
                commission=request.POST['commision'],
                plan_name=request.POST['plan_name'],
            )
            expert.save()
            messages.success(request, 'Expert trader created successfully')
            return redirect('experts')
        except Exception as e:
            messages.error(request, f'{e}')
            return redirect('experts')

    context = {
        'experts': experts,
    }  
    return render(request, 'app/expert.html', context)

def wallet_and_banks(request):
    return render(request, 'app/wallets.html')