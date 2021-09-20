from django.shortcuts import render,redirect
from .models import *
from .forms import *
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import Group
from django.contrib.auth.forms import UserCreationForm


from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user,allowed_user,admin_only
# Create your views here.
@login_required(login_url='login_page/')
@admin_only
def home(request):
    customers=Customer.objects.all()
    orders= Order.objects.all().order_by('-date_created')[:3]
    order_count=Order.objects.count()

    order_pending=Order.objects.filter(status='Pending').count()
    order_delivered=Order.objects.filter(status='Delivered').count()
    return render(request,'accounts/dashboard.html',context={'customers':customers,'orders':orders,'order_count':order_count,'order_pending':order_pending,'order_delivered':order_delivered})


    
def customer(request,pk_test):
    customer= Customer.objects.get(id=pk_test)

    orders=customer.order_set.all()
    order_count = orders.count()

    context={'customer':customer,'orders':orders,'order_count':order_count}
    return render(request,'accounts/customer.html',context=context)

def products(request):
    products= Product.objects.all()
    return render(request,'accounts/products.html',{'products':products})

def create_order(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order,fields=('product','status'),extra=10)
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(), instance=customer)

   
    if request.method=='POST':
        formset=OrderFormSet(request.POST,instance=customer)
        print(request.POST)
        if formset.is_valid():
            formset.save()
            return redirect ('/')
    context={'formset':formset}

    return render(request,'accounts/create_order.html',context)


def update_order(request,pk):
    form=OrderForm()
    
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    print(request.method)

    if request.method=='POST':
        form=OrderForm(request.POST,instance=order)
        print(request.POST)
        if form.is_valid():
            form.save()
            return redirect ('/')

    
        

    return render(request,'accounts/create_order.html',context={'form':form})


def delete_order(request,pk):
    
    print('hello')

    print(request.method)
    order=Order.objects.get(id=pk)
    if request.method=='POST':

    
        print(order)
        order.delete()
        return redirect('/')        

     
    return render(request,'accounts/delete.html',context= {'item':order})
@unauthenticated_user
def login_page(request):
    context={}
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            messages.info(request,'username or password is wrong')
        

    return render(request,'accounts/login.html',context)

def register_page(request):
    form=UserCreationForm()
    context={'form':form}
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid:
            user=form.save()
            group=Group.objects.get(name='customer')
            user.groups.add(group)
            Customer.objects.create(user=user)
            return redirect('/')
    return render(request,'accounts/register.html',context)

def logout_user(request):
    logout(request)
    return redirect('login_page')


def user_page(request):
    order=request.user.customer.order_set.all()
    order_count=request.user.customer.order_set.count()
    order_pending=request.user.customer.order_set.filter(status='Pending').count()
    order_delivered=request.user.customer.order_set.filter(status='Delivered').count() 
    context={'orders':order,'order_count':order_count,'order_pending':order_pending,'order_delivered':order_delivered}
    return render(request,'accounts/users.html',context=context)