from django.urls import path
from . import views
urlpatterns = [
    path('store-products/', views.store_products, name="store-products"),
    
]
