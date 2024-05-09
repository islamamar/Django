from django.shortcuts import render , redirect
from django.http import HttpResponse 
from .models import *  
from .forms import * 
from django.forms import inlineformset_factory 
from .filters import *
from django.contrib.auth import authenticate , login, logout 
from django.contrib import messages 
from  django.contrib.auth.decorators import login_required 
from .decorators import * 
from django.contrib.auth.models import Group

# Create your views here.  
# @allowedUsers(allowedGroups=['admin']) 
@forAdmins
@login_required(login_url='login')
def home(request): 
    orders = Order.objects.all() 
    customers = Customer.objects.all()   
    t_orders = orders.count()
    P_order = orders.filter(status="pending").count()  
    In_order= orders.filter(status ='in Progress').count() 
    d_order= orders.filter(status ='delivered').count()  
    out_order= orders.filter(status ='out of order').count() 
    context = {
        "orders":orders, 
        "customers":customers ,
        "t_orders" :t_orders ,  
        "P_order" :P_order , 
        "In_order" :In_order ,  
        "d_order" :d_order , 
        "out_order" :out_order   


    }
    return render(request, "bookstore/dashboard.html",context)

@login_required(login_url='login')
def customer(request,pk):
    customer=Customer.objects.get(id=pk)  
    orders =customer.order_set.all()  
    searchFilter = OrderFilter(request.GET, queryset=orders)  
    orders = searchFilter.qs

    context= {
        "customer":customer, 
        "orders":orders ,
        "searchFilter":searchFilter
    }

    return render(request , "bookstore/customer.html" , context )

@forAdmins
@login_required(login_url='login')
def book(request): 
    book = Book.objects.all()    
    return  render(request , "bookstore/book.html" , {"book":book} ) 

@login_required(login_url='login')
def create(request):
    form = OrderForm() 
    if request.method =='POST': # when i click to submit button 
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save() # save the data that i get from form to database 
            return redirect('/') 
    context= {"form" :form} 
    return render(request, 'bookstore/order_form.html' , context) 

@login_required(login_url='login')
def createOrder(request, pk):
    orderFormset=inlineformset_factory(Customer, Order, fields=('book','status') ,extra=8) 
    customer= Customer.objects.get(id=pk)  
    formset= orderFormset(queryset=Order.objects.none(), instance=customer) 
    if request.method =='POST': 
        formset = orderFormset(request.POST, instance=customer)
        if formset.is_valid(): 
            formset.save() 
            return redirect('/') 
    context ={"formset":formset} 
    return render(request, "bookstore/create_order.html", context)




@login_required(login_url='login')
def update(request, pk): 

    order =Order.objects.get(id=pk)  
    form= OrderForm(instance=order)  # before clicking to submit btn   
    if request.method =='POST':     
        form= OrderForm(request.POST, instance=order) 
        if form.is_valid(): 
            form.save() 
            return redirect('/') 
    context ={"form" :form} 
    return render(request, 'bookstore/order_form.html' , context) 

@login_required(login_url='login')
def delete(request, pk) :
    order= Order.objects.get(id=pk)
    if request.method == 'POST': 
        order.delete()
        return redirect('/') 
    context= {"order":order}
    return render(request, "bookstore/delete_order.html", context) 

@notLoggedUser
def register(request) :
        form=  CreateNewUser() 
        if request.method =='POST':
            form= CreateNewUser(request.POST)
            if form.is_valid():  # should any new user be  a (customer)                 
                user=form.save() 
                username= form.cleaned_data.get('username')
                group= Group.objects.get(name="customer")
                user.groups.add(group) 
                messages.success(request, username +"created succeffuly")
                return redirect('home') # Go to login  
        context= {'form':form} 
        return render(request, 'bookstore/register.html', context) 

@notLoggedUser
def UserLogin(request): 
        if request.method =='POST': 
            print("entered login function ")
            username =request.POST.get('username') 
            password =request.POST.get('password') 
            user= authenticate(request, username=username , password= password)
            if user is not None: 
                login(request, user) 
                return redirect('home')
            else:
                messages.info(request, "Credentails error")
        context= {} 
        return render(request, "bookstore/login.html", context) 

@login_required(login_url='login')
def  userLogout(request):
    logout(request) 
    return redirect('login') 

def userProfile(request): 
    orders= request.user.customer.order_set.all()  
    t_orders = orders.count()
    P_order = orders.filter(status="pending").count()  
    In_order= orders.filter(status ='in Progress').count() 
    d_order= orders.filter(status ='delivered').count()  
    out_order= orders.filter(status ='out of order').count() 
    context = {
        "orders":orders, 
        "t_orders" :t_orders ,  
        "P_order" :P_order , 
        "In_order" :In_order ,  
        "d_order" :d_order , 
        "out_order" :out_order   


    }
    return render(request, 'bookstore/profile.html', context) 


def profileInfo(request):
    customer =request.user.customer
    form = CustomerForm(instance=customer) 
    if request.method =='POST':    
        form = CustomerForm(request.POST, request.FILES, instance=customer) 
        if form.is_valid() : 
            print(">>>>>>>> islam")          
            form.save()
            print(request.user.customer.avatar.url)
    context = {"form" :form} 
    return render(request, "bookstore/profile_info.html", context)







