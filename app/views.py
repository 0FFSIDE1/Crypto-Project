from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse
from django.views import View
from .models import *
from asgiref.sync import sync_to_async

# Create your views here.

async def dashboard(request):
    return render(request, 'app/index.html')

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
    return redirect('transaction')


def transaction_history(request):
    user = Profile.objects.get(user=request.user)
    transactions = TransactionHistory.objects.filter(user=user)
    context = {
        'transactions': transactions
    }
    return render(request, 'app/transaction.html', context)

async def copy_trading(request):
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

def settings(request):
    user = Profile.objects.get(user=request.user)
    context = {
        'user': user
    }

    return render(request, 'app/my_account.html', context)

async def referral(request):
    return render(request, 'app/referral.html')