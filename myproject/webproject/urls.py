from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
				path("",views.home,name="home"),
				path("product/",views.product,name="product"),
				path("customer/<str:pk>/",views.customer,name="customer"),
				path("order/<str:pk>/",views.createOrder,name="order"),
				path("update_order/<str:pk>/",views.updateOrder,name="update_order"),
				path("delete_order/<str:pk>/",views.deleteOrder,name="delete"),
				path("login/",views.loginpage,name="login"),
				path("logout/",views.logoutuser,name="logout"),
				path("register/",views.register,name="register"),
				path("user/",views.user,name="user"),
				path("account_settings/",views.account_settings,name="settings"),
				]