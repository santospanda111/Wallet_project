from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import render
from .forms import OwnerInfo, UserReg, TransferBalance
from .models import Balance, Owner,Transfer,User,ReceivedAmount
from django.db.models import F


def index(request):
    return render(request, 'index.html')


def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                owners = Owner.objects.filter(user=request.user)
                return render(request, 'home_user.html', {'owners': owners})
            else:
                return render(request, 'login_user.html', {'error_message': 'Your account has been disabled'})
        else:
            return render(request, 'login_user.html', {'error_message': 'Invalid login'})
    return render(request, 'login_user.html')

def register_user(request):
    form = UserReg(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        usertype = form.cleaned_data['usertype']

        user.set_password(password)
        user.save()
        user = authenticate(username=username, password=password)
        if usertype == 'premium':
            user_balance = Balance.objects.filter(user=user)
            user_balance.amount = 2500
            user_balance.save()
        elif usertype == 'non_premium':
            user_balance = Balance.objects.filter(user=user)
            user_balance.amount = 1000
            user_balance.save()
        if user is not None:
            if user.is_active:
                login(request, user)
                owners = Owner.objects.filter(user=request.user)
                return render(request, 'my_wallet.html', {'owners': owners})
    context = {
        "form": form,
    }
    return render(request, 'register_user.html', context)


def my_wallet(request):
    owners = Owner.objects.filter(user=request.user.username)
    if not owners:
        return render(request, 'login_user.html')
    else:
        return render(request, 'my_wallet.html', {'owners': owners})


def logout_user(request):
    logout(request)
    return render(request, 'index.html')


def all_orders(request):
    if not request.user.is_authenticated():
        return render(request, 'login_user.html')
    else:
        transfers = Transfer.objects.filter(user=request.user)
        recs = ReceivedAmount.objects.filter(user=request.user)
        return render(request, 'all_orders.html', {'transfers':transfers,
                                                          'recs':recs})


def transfer_balance(request):
    if not request.user.is_authenticated():
        return render(request, 'login_user.html')
    else:
        owners = Owner.objects.filter(user=request.user)
        user=request.user
        for s in owners:
            senderName = s.name
        form = TransferBalance(request.POST or None)
        if form.is_valid():
            myform = form.save(commit=False)
            rcvr_name = form.cleaned_data['name']
            receivers = Owner.objects.filter(name=rcvr_name)
            if receivers.exists():
                transferAmount = form.cleaned_data['transfer_amount']
                for owner in owners:
                    ownerBalance = owner.balance
                for receiver in receivers:
                    receiverName = receiver.name
                    receiverBalance = receiver.balance+transferAmount
                if ownerBalance >= transferAmount:
                    Owner.objects.filter(id__in=owners).update(balance=F('balance') - transferAmount)
                    Owner.objects.filter(id__in=receivers).update(balance=F('balance') + transferAmount)
                    userr = User.objects.get(owner__in=receivers)
                    p = ReceivedAmount.objects.filter(user=userr).create(rec_amount=transferAmount,rec_name=senderName)
                    p.user=userr
                    p.save()
                    myform.user=request.user
                    myform.save()
                    return render(request, 'transfer_successful.html', {'owners': owners,
                                                                               'transferAmount':transferAmount,
                                                                               'receiverName':receiverName,
                                                                               })
                else:
                    return render(request, 'recharge_unsuccessful.html')

            else:
                return render(request, 'transfer_unsuccessful.html')

        context = {
            "form": form,
            'owners': owners,
        }
        return render(request, 'transfer_balance.html', context)

