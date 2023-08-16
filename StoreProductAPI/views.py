import random
from scripts.load import get_image_size, create_image, create_thumbnail
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from StoreProductAPI.serializers import ColorSerializer, SingleImageSerializer, ImageSerializer, ThumbnailSizeSerializer, ThumbnailSerializer, SingleProductSerializer, ProductSerializer
# Create your views here.


@api_view(['GET', 'POST', 'PUT', 'PATCH'])
def store_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serialized_products = ProductSerializer(products, many=True)
        return Response(serialized_products.data)
    
    elif request.method == 'POST':
        serializer_product = SingleProductSerializer(data=request.data)
        serializer_product.is_valid(raise_exception=True)
        serializer_product.save()
        return Response(serializer_product.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        product = get_object_or_404(Product, pk=request.data.get('id'))
        serialized_product_update = SingleProductSerializer(product, data=request.data)
        serialized_product_update.is_valid(raise_exception=True)
        serialized_product_update.save()
        return Response(serialized_product_update.data, status=status.HTTP_200_OK)
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def single_store_product(request, pk):
    product = get_object_or_404(Product.objects.all(), pk=pk)
    if request.method == 'GET':
        serialized_product = SingleProductSerializer(product)
        return Response(serialized_product.data, status=status.HTTP_200_OK)
    
    if request.method == 'PUT' or request.method == 'PATCH':
        serialized_product_update = SingleProductSerializer(product, data=request.data)
        serialized_product_update.is_valid(raise_exception=True)
        serialized_product_update.save()
        return Response(serialized_product_update.data, status=status.HTTP_200_OK)

    if request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'PATCH'])
def image_products(request):
    if request.method == 'GET':
        images = Image.objects.all()
        serialized_image = ImageSerializer(images, many=True)
        return Response(serialized_image.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serializer_image = SingleImageSerializer(data=request.data)
        serialized_image.is_valid(raise_exceptions=True)
        serialized_image.save()
        return Response(serializer_image.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        image = get_object_or_404(Image, pk=request.data.get('id'))
        serialized_image_update = SingleImageSerializer(image, data=request.data)
        serialized_image_update.is_valid(raise_exception=True)
        serialized_image_update.save()
        return Response(serialized_image_update.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def single_image_product(request, pk):
    image = get_object_or_404(Image, pk=pk)
    if request.method == 'GET':
        serialized_image = SingleImageSerializer(image)
        return Response(serialized_image.data, status=status.HTTP_200_OK)
    
    elif request.method in ['PUT', 'PATCH']:
        serialized_image_update = SingleImageSerializer(image, data=request.data)
        serialized_image_update.is_valid(raise_exception=True)
        serialized_image_update.save()
        return Response(serialized_image_update.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    
    