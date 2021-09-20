from django.contrib import admin
from django.urls import path, include
from ourapp import views
urlpatterns = [
    path('',views.home,name='home'),
    path('products',views.products,name='products'),
    path('customer/<str:pk_test>/',views.customer,name='customer'),
    path('create_order/',views.create_order,name='create_order'),
    path('create_order/<str:pk>',views.create_order,name='create_order'),
    path('update_order/<str:pk>',views.update_order,name='update_order'),
    path('delete_order/<str:pk>',views.delete_order,name='delete_order'),
    path('login_page/',views.login_page,name='login_page'),
    path('register_page',views.register_page,name='register_page'),
    path('logout_user',views.logout_user,name='logout_user'),
    path('user/',views.user_page,name='user')
    

]
    