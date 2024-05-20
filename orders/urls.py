from django.urls import path
from . import views

urlpatterns = [
    path('order-complete/<int:order_number>/', views.OrderComplete.as_view(), name='order-complete'),
    path('pdf_view/<int:order_number>/', views.ViewPDF.as_view(), name="pdf_view"),
]