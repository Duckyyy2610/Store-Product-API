from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from StoreProductAPI.serializers import ColorSerializer, SingleImageSerializer, ImageSerializer, ThumbnailSizeSerializer, ThumbnailSerializer, SingleProductSerializer, ProductSerializer
# Create your views here.

@api_view(['GET', 'POST'])
def store_products(request):
    if request.method == 'GET':
        products = Product.objects.all()
        serialized_products = ProductSerializer(products, many=True)
        return Response(serialized_products.data)
    
    if request.method == 'POST':
        serializer_product = SingleProductSerializer(data=request.data)
        if serializer_product.is_valid():
            serializer_product.save()
            return Response(serializer_product.data ,status=status.HTTP_201_CREATED)
        return Response(serializer_product.errors, status=status.HTTP_400_BAD_REQUEST)
