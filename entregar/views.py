from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login , logout
from .models import *
from .forms import OrderForm , CreateUserForm , CustomerForm
from .filters import OrderFilter , CustomerFilter
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .decorators import unauthenticated_user , allowed_users ,admin_only

@unauthenticated_user
def registerPage(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')


            messages.success(request, 'Conta criada com Sucesso para ' + username)
            return redirect('login')

    context = {'form': form}
    return render(request, 'entregar/register.html', context)


@unauthenticated_user
def loginPage(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Nome de usuario ou password incorrecto!')

    context = {}
    return render(request, 'entregar/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')



@login_required(login_url='login')
@admin_only
def home(request):
    orders = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    delivered = orders.filter(status = 'Entregue').count()
    pending = orders.filter(status = 'Pendente').count()

    myFilter = CustomerFilter(request.GET, queryset=customers)
    customers = myFilter.qs

    context = {'orders':orders, 'customers':customers,'total_orders':total_orders,'delivered':delivered,'pending':pending ,'myFilter': myFilter}
    return render(request,'entregar/dashboard.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def userPage(request):
    orders = request.user.customer.order_set.all()
    total_orders = orders.count()
    delivered = orders.filter(status='Entregue').count()
    pending = orders.filter(status='Pendente').count()

    context = {'orders':orders,'total_orders':total_orders,'delivered':delivered,'pending':pending}
    return render(request, 'entregar/user.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['customer'])
def accontSettings(request):
    customer = request.user.customer
    form = CustomerForm(instance=customer)

    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES,instance=customer)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'entregar/account_settings.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def products(request):
    products = Product.objects.all()
    return render(request,'entregar/products.html',{'products':products})

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders = customer.order_set.all()
    order_count =orders.count()

    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs

    context = {'customer': customer,'orders':orders,'order_count':order_count,'myFilter':myFilter}
    return render(request,'entregar/customer.html',context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin','customer'])
def createOrder(request, pk):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'), extra=10)
    customer = Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(), instance=customer)

    if request.method == 'POST':
        formset = OrderFormSet(request.POST, instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {'formset':formset}
    return render(request, 'entregar/order_form.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request, pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        form = OrderForm(request.POST , instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form': form}
    return render(request, 'entregar/order_form2.html', context)

@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request, pk):
    order = Order.objects.get(id=pk)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context = {'item':order}
    return render(request, 'entregar/delete.html', context)