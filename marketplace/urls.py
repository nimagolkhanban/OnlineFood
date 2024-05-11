from django.urls import path
from . import views


urlpatterns = [
    path('', views.MarketPlaceView.as_view(), name='marketplace'),
    path('<slug:vendor_slug>/', views.VendorDetailView.as_view(), name='vendor-detail'),
    # add and decrease to cart url
    path('add_to_cart/<int:food_id>/', views.add_to_cart, name='add-to-cart'),
    path('decrease_cart/<int:food_id>/', views.decrease_cart, name='decrease-cart')
]