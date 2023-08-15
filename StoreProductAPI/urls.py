from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'single_store_products', views.SingleStoreProductViewSet)

urlpatterns = [
    path('store-products/', views.store_products, name="store-products"),
    path('store-products/<uuid:pk>', views.single_store_products, name="single-store-products"),
    # path('api/', include(router.urls))
]
