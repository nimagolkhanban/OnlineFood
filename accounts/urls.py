from django.urls import path
from . import views


urlpatterns = [
    path('registeruser/', views.RegisterUserView.as_view(), name='registeruser'),
    path('registervendor/', views.RegisterVendorView.as_view(), name='registervendor'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('customerdashboard/', views.CustomerDashboardView.as_view(), name='customerdashboard'),
    path('vendordashboard/', views.VendorDashboardView.as_view(), name='vendordashboard'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
]



























