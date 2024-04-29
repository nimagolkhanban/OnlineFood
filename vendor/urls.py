from django.urls import path
from accounts import views as accounts_views
from . import views
urlpatterns = [
    path('profile/', views.RestaurantProfileView.as_view(), name='restaurant_profile'),
]