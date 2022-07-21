from django.urls import path
from . import views

app_name = 'bills'
urlpatterns = [
    path('', views.index, name='index'), #, namespace='bills'
    path('add', views.add, name='add'),
    path('delete_bill', views.delete_bill, name='delete_bill'),
    path('<int:bill_id>', views.bill, name='bill'),
    path('<int:bill_id>/add_item', views.add_item, name='add_item'),
    path('<int:bill_id>/assign_payment', views.assign_payment, name='assign_payment'),
    path('<int:bill_id>/delete_payment', views.delete_payment, name='delete_payment'),
    path('api/get_bills', views.get_bills, name='api_get_bills'),
    path('api/get_all_users', views.get_all_users, name='get_all_users')
]