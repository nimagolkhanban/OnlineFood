from django.urls import path
from . import views


urlpatterns = [
    path('registeruser/', views.RegisterUserView.as_view(), name='registeruser'),
    path('registervendor/', views.RegisterVendorView.as_view(), name='registervendor'),

    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),

    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
]