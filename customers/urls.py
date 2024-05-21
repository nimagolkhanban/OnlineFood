from django.urls import path
from . import views
from accounts import views as AccountView

urlpatterns = [
    path('', AccountView.CustomerDashboardView.as_view(), name='customer-dashboard'),
    path('profile/', views.CustomerProfileView.as_view(), name='customer-profile'),
    path('my-orders/', views.MyOrdersView.as_view(), name='customer-my-orders'),
    path('order-detail/<int:order_number>/', views.OrderDetailView.as_view(), name='order_detail'),

]