from django.shortcuts import render
from django.http import JsonResponse
from .models import *

# Create your views here.

async def dashboard(request):
    return render(request, 'app/index.html')

def deposit_withdraw(request):
    context = {
        'wallets': Wallet.objects.all(),
        'banks': BankAccount.objects.all()

    }
    return render(request, 'app/deposit_withdraw.html', context)

async def transaction_history(request):
    return render(request, 'app/transaction.html')

async def copy_trading(request):
    return render(request, 'app/copytrading.html')

def plans(request):
    context = {
        'plans': Plan.objects.all()
    }
    return render(request, 'app/plan&pricing.html', context)

async def settings(request):
    return render(request, 'app/settings.html')

async def referral(request):
    return render(request, 'app/referral.html')