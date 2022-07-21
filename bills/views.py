from datetime import date

from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import get_user_model

##### API
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import BillSerializer, ItemSerializer, Item_PaymentSerializer, UserSerializer
import json

from .models import Bill, Item, Item_Payment

# Create your views here.
def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse('users:login'))

    acc_user = request.user

    All_bills = Bill.objects.all()
    
    # not payed bills [bill_str, bill_id]
    not_payed_bills = []
    for bill in All_bills:
        if not bill.is_payed:
            not_payed_bills.append([str(bill), bill.id])


    User = get_user_model()
    users = User.objects.all()
    return render(request, 'bills/index.html', {
            'user': acc_user,
            'first_name_first_letter': acc_user.first_name[0],
            'last_name_first_letter': acc_user.last_name[0],
            'not_payed_bills': not_payed_bills,
            'users': users
        })

def add(request):
    if request.method == 'POST':
        name = request.POST['name']
        date = request.POST['date']
        comment = request.POST['comment']
        lender_id = int(request.POST['lender'])
        User = get_user_model()
        lender = User.objects.get(id = lender_id)
        bill = Bill(name = name, date = date, comment=comment, lender = lender)
        bill.save()
        return HttpResponseRedirect(reverse('bills:index'))



def delete_bill(request):
    if request.method == 'POST':
        bill_id = int(request.POST['bill_id'])
        bill = Bill.objects.get(id = bill_id)
        bill.delete()

        return HttpResponseRedirect(reverse('bills:index'))



def bill(request, bill_id):
    users = get_user_model().objects.all()
    bill = Bill.objects.get(id = bill_id)
    items = Item.objects.filter(bill = bill).all().order_by('id')
    payments = Item_Payment.objects.filter(item__in = items).all().order_by('payer', 'item_id')

    # total cost is method therefore i have to iterate to count it
    total_costs = 0
    for item in items:
        total_costs += item.cost_total
    

    return render(request, 'bills/bill.html', {
            'bill': bill,
            'items': items,
            'total_costs': total_costs,
            'payments': payments,
            'users': users
        })



def add_item(request, bill_id):
    if request.method == 'POST':
        name = request.POST['name']
        amount = request.POST['amount']
        cost_per_exemplar = request.POST['cost_per_exemplar']
        bill = Bill.objects.get(id = bill_id)
        item = Item(name=name, amount=amount, cost_per_exemplar = cost_per_exemplar, bill=bill)
        item.save()
        return HttpResponseRedirect(reverse('bills:bill', args=(bill_id, )))


def assign_payment(request, bill_id):
    if request.method == 'POST':
        item_id = int(request.POST['item'])
        payer_id = int(request.POST['payer'])
        paying_part = float(request.POST['paying_part'])

        item = Item.objects.get(id = item_id)
        payer = get_user_model().objects.get(id = payer_id)

        item_payment = Item_Payment(item = item, payer = payer, paying_part = paying_part)
        item_payment.save()
        return HttpResponseRedirect(reverse('bills:bill', args=(bill_id, )))



def delete_payment(request, bill_id):
    if request.method == 'POST':
        payment_id = int(request.POST['payment'])
        Item_Payment.objects.filter(id = payment_id).delete()
        return HttpResponseRedirect(reverse('bills:bill', args=(bill_id, )))

########################### APIs ###########################
############################################################

@api_view(['GET'])
def get_bills(request):

    not_payed_bills = []
    for bill in Bill.objects.all():
        if not bill.is_payed:
            serializedBill = BillSerializer(bill).data

            lender = get_user_model().objects.get(id = serializedBill["lender"])
            serializedBill["lender"] = UserSerializer(lender).data


            items = Item.objects.filter(bill = bill).all()
            serializedBill["items"] = ItemSerializer(items, many = True).data


            not_payed_bills.append(serializedBill)

    return Response(not_payed_bills)


@api_view(['GET'])
def get_all_users(request):
    return Response(UserSerializer(get_user_model().objects.all(), many=True).data)
