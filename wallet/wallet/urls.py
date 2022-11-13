from django.conf.urls import url
from . import views

app_name = 'wallet'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^login_user$', views.login_user, name='login_user'),
    url(r'^register_user$', views.register_user, name='register_user'),
    url(r'^my_wallet$', views.my_wallet, name='my_wallet'),
    url(r'^logout_user$', views.logout_user, name='logout_user'),
    url(r'^all_orders$', views.all_orders, name='all_orders'),
    url(r'^transfer_balance$', views.transfer_balance, name='transfer_balance')
]
