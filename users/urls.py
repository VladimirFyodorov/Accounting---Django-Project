from django.urls import path
from . import views

app_name = 'users'
urlpatterns = [
    path('', views.index, name='index'),
    #path('login', views.login_view, name='login'),
    path('login', views.login, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('pay/<str:lender_username>', views.pay, name='pay'),
    path('pay/<str:lender_username>/make_payment', views.make_payment, name='make_payment'),
    path('receive/<str:borrower_username>', views.receive, name='receive'),
    path('receive/<str:borrower_username>/receive_payment', views.receive_payment, name='receive_payment')
]