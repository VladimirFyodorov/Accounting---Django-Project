from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout, get_user_model
from bills.models import Bill, Item, Item_Payment

# Create your views here.
# clean terminal print("\033[H\033[J", end="")
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login'))
    else:
        acc_user = request.user
        first_name_first_letter = acc_user.first_name[0]
        last_name_first_letter = acc_user.last_name[0]
        # counting Account payable total and grouped by lender username
        account_payable = 0
        account_payable_by_lender = {}
        account_payable_by_lender = {}
        account_payables_v_to_v_ids = []
        for user in get_user_model().objects.all(): #.exclude(user = user):
            account_payable_by_lender[user.first_name] = 0

        for payment in Item_Payment.objects.filter(payer = acc_user).filter(is_payed = False).all():
            account_payable += payment.paying_amount
            lender_id = payment.item.bill.lender.id
            lender_first_name = get_user_model().objects.get(id = lender_id).first_name
            account_payable_by_lender[lender_first_name] += payment.paying_amount

            if lender_id == 1:
                account_payables_v_to_v_ids.append([payment.id, payment.paying_amount])


        

        # counting Account receivable total and grouped by borrower username
        account_receivable = 0
        account_receivable_by_borrower = {}
        for user in get_user_model().objects.all(): #.exclude(user = user):
            account_receivable_by_borrower[user.first_name] = 0

        for payment in Item_Payment.objects.all():
            if payment.lender == acc_user and payment.is_payed == False:
                account_receivable += payment.paying_amount
                account_receivable_by_borrower[payment.payer.first_name] += payment.paying_amount

        
        #counting Net result = account_receivable - account_payable
        account_Net = account_receivable - account_payable
        account_Net_by_user = account_receivable_by_borrower.copy()

        for key in account_payable_by_lender:
            account_Net_by_user[key] -= account_payable_by_lender[key]

        
        # rounding results
        account_payable = -round(account_payable)
        account_receivable = round(account_receivable)
        account_Net = round(account_Net)

        for key in account_payable_by_lender:
            account_payable_by_lender[key] = -round(account_payable_by_lender[key])

        for key in account_receivable_by_borrower:
            account_receivable_by_borrower[key] = round(account_receivable_by_borrower[key])

        for key in account_Net_by_user:
            account_Net_by_user[key] = round(account_Net_by_user[key])

        return render(request, 'users/account.html', {
                'user': user,
                'first_name_first_letter': first_name_first_letter,
                'last_name_first_letter': last_name_first_letter,
                'account_payable': account_payable,
                'account_payable_by_lender': account_payable_by_lender,
                'account_receivable': account_receivable,
                'account_receivable_by_borrower': account_receivable_by_borrower,
                'account_Net': account_Net,
                'account_Net_by_user': account_Net_by_user,
                'account_payables_v_to_v_ids': account_payables_v_to_v_ids
            })



def login_view(request):
    if request.method == 'POST' and len(request.POST['password']) == 0:
            emails = get_user_model().objects.values_list('email', flat=True).all()
            email = request.POST['email']
            if email in emails:
                user = get_user_model().objects.get(email = email)
                first_name = user.first_name
                last_name = user.last_name
                return render(request, 'users/login.html', {
                    'first_name': first_name,
                    'first_name_first_letter': first_name[0],
                    'last_name': last_name,
                    'last_name_first_letter': last_name[0],
                    'email': email,
                    'form_numer': 2,
                })
            else:
                return render(request, 'users/login.html', {
                    'form_numer': 1,
                    'message': 'incorrect email'
                })
    elif request.method == 'POST' and len(request.POST['password']) > 0:
        email = request.POST['email']
        password = request.POST['password']
        username = get_user_model().objects.get(email = email).username
        first_name =  get_user_model().objects.get(email = email).first_name
        last_name =  get_user_model().objects.get(email = email).last_name
        user = authenticate(request, username = username, password = password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('users:index'))

        else:
            return render(request, 'users/login.html', {
            'first_name': first_name,
            'first_name_first_letter': first_name[0],
            'last_name': last_name,
            'last_name_first_letter': last_name[0],
            'email': email,
            'form_numer': 2,
            'message': f'Email or Password is incorrect'
            })


    return render(request, 'users/login.html', {
        'form_numer': 1
    })



def logout_view(request):
    logout(request)
    return render(request, 'users/login.html')



def pay(request, lender_username):
    # form with multiple https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select
    user = request.user
    lender = get_user_model().objects.get(username = lender_username)
    
    # making lst for [bill_name,  bill_total_sum, [payment_id, payment_name, paying_amount, paying_part]]
    bill_payment = []
    for bill in Bill.objects.filter(lender = lender).all():
        payments_lst = []
        bill_total = 0
        for item in Item.objects.filter(bill = bill).all():
            for payment in Item_Payment.objects.filter(item = item).filter(payer = user).filter(is_payed = False).all():
                payments_lst.append([payment.id, payment.item.name, payment.paying_amount, payment.paying_part])
                bill_total += payment.paying_amount
        if not (payments_lst == []):
            bill_payment.append([str(bill), bill_total, payments_lst])

    return render(request, 'users/pay.html', {
        'user': user,
        'lender': lender,
        'bill_payment': bill_payment
    })


def make_payment(request, lender_username):
    if request.method == 'POST':
        payment_id = int(request.POST['payment_id'])
        Item_Payment.objects.filter(id = payment_id).update(is_payed=True)
        return HttpResponseRedirect(reverse('users:pay', args=(lender_username, )))


def receive(request, borrower_username):
    user = request.user
    borrower = get_user_model().objects.get(username = borrower_username)

    # making lst for [bill_name, bill_total_sum, [payment_id, payment_name, paying_amount, paying_part]]
    bill_payment = []
    for bill in Bill.objects.filter(lender = user).all():
        payments_lst = []
        bill_total = 0
        for item in Item.objects.filter(bill = bill).all():
            for payment in Item_Payment.objects.filter(item = item).filter(payer = borrower).filter(is_payed = False).all():
                payments_lst.append([payment.id, payment.item.name, payment.paying_amount, payment.paying_part])
                bill_total += payment.paying_amount
        if not (payments_lst == []):
            bill_payment.append([str(bill), bill_total, payments_lst])

    return render(request, 'users/receive.html', {
        'user': user,
        'borrower': borrower,
        'bill_payment': bill_payment
    })



def receive_payment(request, borrower_username):
    if request.method == 'POST':
        #payments_ids = request.POST['payments_ids']
        #Item_Payment.objects.filter(id__in = payments_ids).update(is_payed=True)
        payment_id = int(request.POST['payment_id'])
        Item_Payment.objects.filter(id = payment_id).update(is_payed=True)
        return HttpResponseRedirect(reverse('users:receive', args=(borrower_username, )))

