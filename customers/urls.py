from django.urls import path
from . import views
from accounts import views as AccountView

urlpatterns = [
    path('', AccountView.CustomerDashboardView.as_view(), name='customer-dashboard'),
    path('profile/', views.CustomerProfileView.as_view(), name='customer-profile'),

]