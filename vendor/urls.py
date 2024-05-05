from django.urls import path
from accounts import views as accounts_views
from . import views
urlpatterns = [
    path('profile/', views.RestaurantProfileView.as_view(), name='restaurant_profile'),
    path('menu-builder/', views.MenuBuilderView.as_view(), name='menu-builder'),
    path('menu-builder/category/<int:pk>/', views.FoodItemsByCategoryView.as_view(), name='food-items-by-category')
]