from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import *
from .forms import OrderForm,CreateUserForm,CustomerForm
from .filters import OrderFilter
from .decorators import unauthenticated_user,allowed_users,admin_only
from django.contrib.auth.models import Group

# Create your views here.

@login_required(login_url="login")
@allowed_users(allowed_roles="Customers")
def user(request):
	orders = request.user.customer.order_set.all()
	total_orders = orders.count()
	delivered = orders.filter(status="delivered").count()
	pending = orders.filter(status="pending").count()
	context={"orders":orders,"total_orders":total_orders,
	"delivered":delivered,"pending":pending}
	return render(request,"webhtml/user.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles="Customers")
def account_settings(request):
	customer = request.user.customer
	form = CustomerForm(instance=customer)

	if request.method == "POST":
		form = CustomerForm(request.POST,request.FILES,instance=customer)
		if form.is_valid():
			form.save()
	context={"form":form}
	return render(request,"webhtml/account_settings.html",context)

@unauthenticated_user
def register(request):

	form = CreateUserForm()
	if request.method == "POST":
		form = CreateUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = form.cleaned_data.get("username")
			group = Group.objects.get(name="Customers")
			user.groups.add(group)
			Customer.objects.create(user=user,)
			messages.success(request,"account was successfully created for " + username)
			return redirect("login")
	context={"form":form}
	return render(request,"webhtml/register.html",context)

@unauthenticated_user
def loginpage(request):

	context={}

	if request.method == "POST":
		username = request.POST.get("username")
		password = request.POST.get("password")

		user = authenticate(request,username=username,password=password)

		if user is not None:
			login(request,user)
			return redirect("/")
		else:
			#messages.info("username or password is invalid")
			return render(request,"webhtml/login.html",context)
	return render(request,"webhtml/login.html",context)

def logoutuser(request):
	logout(request)
	return redirect('login')


@login_required(login_url="login")
@admin_only
def home(request):
	customers = Customer.objects.all()
	orders = Order.objects.all()
	total_customers = customers.count()
	total_orders = orders.count()
	delivered = orders.filter(status="delivered").count()
	pending = orders.filter(status="pending").count()
	context={"customers":customers,"orders":orders,"total_orders":total_orders,
	"delivered":delivered,"pending":pending}
	return render(request,"webhtml/dashboard.html",context)



@login_required(login_url="login")
def product(request):
	products = Product.objects.all()
	return render(request,"webhtml/product.html",{"products":products})

@login_required(login_url="login")
def customer(request,pk):
	print("hello")
	customers = Customer.objects.get(id=pk)
	orders = customers.order_set.all()
	orders_count = orders.count()
	myFilter = OrderFilter(request.GET,queryset=orders)
	orders = myFilter.qs
	context = {"customers":customers,"orders":orders,"orders_count":orders_count,"myFilter":myFilter}
	return render(request,"webhtml/customer.html",context)

def createOrder(request,pk):
	OrderFormSet = inlineformset_factory(Customer,Order,fields=("product","status"),extra=5)
	customers = Customer.objects.get(id=pk)
	formset = OrderFormSet(queryset=Order.objects.none(),instance=customers)
	#form = OrderForm(initial={"customer":customers})
	context={"formset":formset}
	if request.method == "POST":
		formset = OrderFormSet(request.POST,instance=customers)
		if formset.is_valid():
			print("valid")
			formset.save()
			return redirect("/")
	return render(request,"webhtml/order_form.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles="admin")
def updateOrder(request,pk):
	order = Order.objects.get(id=pk)
	forms = OrderForm(instance=order)
	if request.method =="POST":
		forms=OrderForm(request.POST,instance=order)
		if forms.is_valid():
			forms.save()
			return redirect("/")
	context = {"forms":forms}
	return render(request,"webhtml/order_form.html",context)

@login_required(login_url="login")
@allowed_users(allowed_roles="admin")
def deleteOrder(request,pk):
	order = Order.objects.get(id=pk)
	print(order.id)
	context={"item":order}
	if request.method == "POST":
		order.delete()
		return redirect("/")
	return render(request,"webhtml/delete_order.html",context)