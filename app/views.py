from django.shortcuts import render
from django.http import JsonResponse

# Create your views here.

async def dashboard(request):
    return render(request, 'app/index.html')

async def deposit_withdraw(request):
    return render(request, 'app/deposit_withdraw.html')

async def transaction_history(request):
    return render(request, 'app/transaction.html')

async def copy_trading(request):
    return render(request, 'app/copytrading.html')

async def plans(request):
    return render(request, 'app/plan&pricing.html')

async def settings(request):
    return render(request, 'app/settings.html')

async def referral(request):
    return render(request, 'app/referral.html')