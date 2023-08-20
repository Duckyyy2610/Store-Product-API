import random
import re
from scripts.function import get_image_size, get_or_create_image, get_or_create_thumbnail, add_or_delete, get_ordering
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
        product_uuid = request.query_params.get('uuid')
        product_name = request.query_params.get('name')
        product_price = request.query_params.get('price')
        product_company = request.query_params.get('company')
        product_description = request.query_params.get('description')
        product_category = request.query_params.get('category') 
        product_shipping = request.query_params.get('shipping')
        ordering = request.query_params.get('ordering')

        if product_uuid: 
            products = products.filter(uuid__icontains=product_uuid)

        if product_name:
            products = products.filter(name__icontains=product_name)
        
        if product_price:
            products = products.filter(price__icontains=product_price)

        if product_company:
            products = products.filter(company__icontains=product_company)

        if product_description:
            products = products.filter(description__icontains=product_description)

        if product_category:
            products = products.filter(category__icontains=product_category)

        if ordering:
            products = get_ordering(products, ordering)
        # products = products.filter(shipping__contains=product_company)

        serialized_products = ProductSerializer(products, many=True)
        return Response(serialized_products.data)
    
    elif request.method == 'POST':
        serialized_product = SingleProductSerializer(data=request.data)
        serialized_product.is_valid(raise_exception=True)
        serialized_product.save()
        return Response(serialized_product.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        product = get_object_or_404(Product, id=request.data.get('id'))
        serialized_product_update = None
        if request.method == 'PUT':
            serialized_product_update = SingleProductSerializer(product, data=request.data)
        else:
            serialized_product_update = SingleProductSerializer(product, data=request.data, partial=True)

        serialized_product_update.is_valid(raise_exception=True)
        serialized_product_update.save()
        return Response(serialized_product_update.data, status=status.HTTP_200_OK)
    

@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def single_store_product(request, pk):
    product = get_object_or_404(Product, pk=pk)

    if request.method == 'GET':
        serialized_product = SingleProductSerializer(product)
        return Response(serialized_product.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        serialized_product_update = None
        if request.method == 'PUT':
            serialized_product_update = SingleProductSerializer(product, data=request.data)
        else:
            serialized_product_update = SingleProductSerializer(product, data=request.data, partial=True)

        serialized_product_update.is_valid(raise_exception=True)
        serialized_product_update.save()
        return Response(serialized_product_update.data, status=status.HTTP_200_OK)
    
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST', 'PUT', 'PATCH'])
def image_products(request):
    if request.method == 'GET':
        images = Image.objects.all()

        image_uuid = request.query_params.get('id')
        image_width = request.query_params.get('width')
        image_height = request.query_params.get('height')
        image_url = request.query_params.get('url')
        type = request.query_params.get('type')
        ordering = request.query_params.get('ordering')

        if image_uuid:
            images = images.filter(uuid__icontains=image_uuid)
        
        if image_width:
            images = images.filter(width__icontains=image_width)

        if image_height:
            images = images.filter(height__icontains=image_height)

        if image_url:
            images = images.filter(url__icontains=image_url)

        if ordering:
            images = get_ordering(images, ordering)

        serialized_image = ImageSerializer(images, many=True)
        return Response(serialized_image.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serialized_image = SingleImageSerializer(data=request.data)
        serialized_image.is_valid(raise_exception=True)
        serialized_image.save()
        return Response(serialized_image.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        image = get_object_or_404(Image, pk=request.data.get('id'))
        serialized_image_update = None
        if request.method == 'PUT':
            serialized_image_update = SingleImageSerializer(image, data=request.data)
        else:
            serialized_image_update = SingleImageSerializer(image, data=request.data, partial=True)
        serialized_image_update.is_valid(raise_exception=True)
        serialized_image_update.save()
        return Response(serialized_image_update.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def single_image_product(request, pk):
    image = get_object_or_404(Image, pk=pk)

    if request.method == 'GET':
        serialized_image = SingleImageSerializer(image)
        return Response(serialized_image.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        serialized_image_update = None
        if request.method == 'PUT':
            serialized_image_update = SingleImageSerializer(image, data=request.data)
        else:
            serialized_image_update = SingleImageSerializer(image, data=request.data, partial=True)
        serialized_image_update.is_valid(raise_exception=True)
        serialized_image_update.save()
        return Response(serialized_image_update.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        image.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    


@api_view(['GET', 'POST', 'PUT', 'PATCH'])
def colors(request):
    if request.method == 'GET':
        colors_ = Color.objects.all()

        color_id = request.query_params.get('id')
        color_value = request.query_params.get('value')
        ordering = request.query_params.get('ordering')
        
        if color_id:
            colors_ = colors_.filter(id__icontains=color_id)
        
        if color_value:
            colors_ = colors_.filter(value__icontains=color_value)

        if ordering:
            colors_ = get_ordering(colors_, ordering)

        serialized_image = ColorSerializer(colors_, many=True)
        return Response(serialized_image.data, status=status.HTTP_200_OK)
    
    elif request.method == 'POST':
        serialized_image = ColorSerializer(data=request.data)
        serialized_image.is_valid(raise_exception=True)
        serialized_image.save()
        return Response(serialized_image.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        image = get_object_or_404(Image, pk=request.data.get('id'))
        serialized_image_update = ColorSerializer(image, data=request.data)
        serialized_image_update.is_valid(raise_exception=True)
        serialized_image_update.save()
        return Response(serialized_image_update.data, status=status.HTTP_200_OK)


@api_view(['GET', 'PUT', 'PATCH', 'DELETE'])
def single_color(request, pk):
    color = get_object_or_404(Color, pk=pk)

    if request.method == 'GET':
        serialized_image = ColorSerializer(color)
        return Response(serialized_image.data, status=status.HTTP_200_OK)
    
    elif request.method == 'PUT' or request.method == 'PATCH':
        serialized_image_update = ColorSerializer(color, data=request.data)
        serialized_image_update.is_valid(raise_exception=True)
        serialized_image_update.save()
        return Response(serialized_image_update.data, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        color.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



    
    