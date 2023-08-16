from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# router = DefaultRouter()
# router.register(r'single_store_products', views.SingleStoreProductViewSet)

urlpatterns = [
    path('store-products/', views.store_products, name="store-products"),
    path('store-products/<uuid:pk>', views.single_store_product, name="single-store-product"),
    path('image-products/', views.image_products, name="image-products"),
    path('image-products/<uuid:pk>', views.single_image_product, name="single-image-product"),
    
    # path('api/', include(router.urls))
]
