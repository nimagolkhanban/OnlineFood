from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.myaccount),
    # register and activate account
    path('registeruser/', views.RegisterUserView.as_view(), name='registeruser'),
    path('registervendor/', views.RegisterVendorView.as_view(), name='registervendor'),
    path('activate/<uidb64>/<token>/', views.activate_account, name='activate'),
    # log in and out
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    # dashboard redirectors
    path('myaccount/', views.myaccount, name='myaccount'),
    path('customerdashboard/', views.CustomerDashboardView.as_view(), name='customerdashboard'),
    path('vendordashboard/', views.VendorDashboardView.as_view(), name='vendordashboard'),
    # forgot password
    path('forgotpassword/', views.ForgotPasswordView.as_view(), name='forgotpassword'),
    path('resetpassword_validate/<uidb64>/<token>/', views.ResetPasswordValidateView.as_view(), name='resetpasswordvalidate'),
    path('resetpassword/', views.ResetPasswordView.as_view(), name='resetpassword'),
    # vendor link
    path('vendor/', include("vendor.urls")),

]



























