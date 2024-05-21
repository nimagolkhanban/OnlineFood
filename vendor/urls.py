from django.urls import path
from accounts import views as accounts_views
from . import views
urlpatterns = [
    path('profile/', views.RestaurantProfileView.as_view(), name='restaurant_profile'),
    path('menu-builder/', views.MenuBuilderView.as_view(), name='menu-builder'),
    path('menu-builder/category/<int:pk>/', views.FoodItemsByCategoryView.as_view(), name='food-items-by-category'),

    # category CRUD
    path('menu-builder/category/add/', views.AddCategoryView.as_view(), name='add-category'),
    path('menu-builder/category/edit/<int:pk>/', views.EditCategoryView.as_view(), name='edit-category'),
    path('menu-builder/category/delete/<int:pk>/', views.DeleteCategoryView.as_view(), name='delete-category'),

    # food item CRUD
    path('menu-builder/food/add/<int:pk>/', views.AddFoodView.as_view(), name='add-food'),
    path('menu-builder/food/edit/<int:pk>/', views.EditFoodView.as_view(), name='edit-food'),
    path('menu-builder/food/delete/<int:pk>/', views.DeleteFoodView.as_view(), name='delete-food'),

    # opening hour multiple form handel in one url
    path('opening-hour/', views.OpeningHourView.as_view(), name='opening-hour'),
    path('opening-hour/remove/<int:pk>/', views.RemoveOpeningHourView.as_view(), name='remove-opening-hour'),
    path('vendor-order-detail/<int:order_number>/', views.VendorOrderDetailView.as_view(), name='vendor-order-detail')


]