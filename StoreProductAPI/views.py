import random
from scripts.load import get_image_size, create_image, update_product, post_product
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from StoreProductAPI.serializers import ColorSerializer, SingleImageSerializer, ImageSerializer, ThumbnailSizeSerializer, ThumbnailSerializer, SingleProductSerializer, ProductSerializer
# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def store_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serialized_products = ProductSerializer(products, many=True)
        return Response(serialized_products.data)
    
    if request.method == 'POST':
        serializer_product = post_product(request.data, SingleProductSerializer)
        return Response(serializer_product.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT' or request.method == 'PATCH':
        product = Product.objects.get(id=request.data.get('id'))
        serialized_product_update = update_product(product, request.data, SingleProductSerializer)
        return Response(serialized_product_update.data, status=status.HTTP_200_OK)
    

@api_view(['GET', 'POST', 'PUT', 'PATCH', 'DELETE'])
def single_store_products(request, pk):
    product = get_object_or_404(Product.objects.all(), pk=pk)
    if request.method == 'GET':
        serialized_product = SingleProductSerializer(product)
        return Response(serialized_product.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT' or request.method == 'PATCH':
        serialized_product_update = update_product(product, request.data, SingleProductSerializer)
        return Response(serialized_product_update.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
    