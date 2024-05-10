from django.urls import path
from . import views


urlpatterns = [
    path('', views.MarketPlaceView.as_view(), name='marketplace'),
    path('<slug:vendor_slug>/', views.VendorDetailView.as_view(), name='vendor-detail')
]