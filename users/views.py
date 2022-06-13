from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from bills.models import Bill, Item, Item_Payment
import pandas as pd

# Create your views here.
# clean terminal print("\033[H\033[J", end="")
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('login'))
    else:
        user = request.user

        # counting Account payable total and grouped by lender username
        account_payable = 0
        account_payable_by_lender = {}
        for payment in Item_Payment.objects.filter(payer = user).filter(is_payed = False).all():
            account_payable += payment.paying_amount
            lender_id = payment.item.bill.lender.id
            lender_username = get_user_model().objects.get(id = lender_id).username

            try:
                account_payable_by_lender[lender_username] += payment.paying_amount
            except:
                account_payable_by_lender[lender_username] = payment.paying_amount
        

        # counting Account receivable total and grouped by borrower username
        account_receivable = 0
        account_receivable_by_borrower = {}
        for payment in Item_Payment.objects.all():
            if payment.lender == user and payment.is_payed == False:
                account_receivable += payment.paying_amount
                try:
                    account_receivable_by_borrower[payment.payer.username] += payment.paying_amount
                except:
                    account_receivable_by_borrower[payment.payer.username] = payment.paying_amount


        return render(request, 'users/user.html', {
                'user': user,
                'account_payable': account_payable,
                'account_payable_by_lender': account_payable_by_lender,
                'account_receivable': account_receivable,
                'account_receivable_by_borrower': account_receivable_by_borrower
            })


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('index'))

        else:
            return render(request, 'users/login.html', {
                'message': 'Login or Password is incorrect'
            })
    return render(request, 'users/login.html')


def logout_view(request):
    logout(request)
    return render(request, 'users/login.html', {
        'message': 'Logged out'
    })



def pay(request, lender_username):
    # form with multiple https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select
    user = request.user
    lender = get_user_model().objects.get(username = lender_username)
    
    # making lst for [bill_name,  [payment_id, payment_name, paying_amount]]
    bill_payment = []
    for bill in Bill.objects.filter(lender = lender).all():
        payments_lst = []
        for item in Item.objects.filter(bill = bill).all():
            for payment in Item_Payment.objects.filter(item = item).filter(payer = user).filter(is_payed = False).all():
                payments_lst.append([payment.id, payment.item.name, payment.paying_amount])
        bill_payment.append([str(bill), payments_lst])

    return render(request, 'users/pay.html', {
        'user': user,
        'lender': lender,
        'bill_payment': bill_payment
    })


def make_payment(request, lender_username):
    if request.method == 'POST':
        payments_ids = request.POST['payments_ids']
        Item_Payment.objects.filter(id__in = payments_ids).update(is_payed=True)
        return HttpResponseRedirect(reverse('pay', args=(lender_username, )))


def receive(request, borrower_username):
    user = request.user
    borrower = get_user_model().objects.get(username = borrower_username)

    # making lst for [bill_name,  [payment_id, payment_name, paying_amount]]
    bill_payment = []
    for bill in Bill.objects.filter(lender = user).all():
        payments_lst = []
        for item in Item.objects.filter(bill = bill).all():
            for payment in Item_Payment.objects.filter(item = item).filter(payer = borrower).filter(is_payed = False).all():
                payments_lst.append([payment.id, payment.item.name, payment.paying_amount])
        bill_payment.append([str(bill), payments_lst])

    return render(request, 'users/receive.html', {
        'user': user,
        'borrower': borrower,
        'bill_payment': bill_payment
    })



def receive_payment(request, borrower_username):
    if request.method == 'POST':
        payments_ids = request.POST['payments_ids']
        Item_Payment.objects.filter(id__in = payments_ids).update(is_payed=True)
        return HttpResponseRedirect(reverse('pay', args=(borrower_username, )))
