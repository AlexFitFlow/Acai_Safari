from django.urls import path     
from . import views
urlpatterns = [
    path('', views.main),
    path('register', views.register),
    path('login', views.login),
    path('logout', views.logout),
    path('main', views.main),
    path('order_page', views.order_page),
    path('story_page', views.story_page),
    path('login_page', views.login_page),
    path('contact_page', views.contact_page),
    path('account', views.account_page),
    path('build', views.build),
    path('create_bowl', views.create_bowl),
    path('receipt/<int:id>', views.receipt),
    path('purchase', views.purchase),
    path('purchase_page', views.purchase_page),
    path('surprise', views.surprise),
    path('re_order', views.re_order_page),
    path('order_again/<int:id>', views.order_again),
    path('update_user/<int:id>', views.update_user)
]