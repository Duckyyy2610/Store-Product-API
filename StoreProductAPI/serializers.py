from .models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from rest_framework import serializers
import random
from django.db import transaction
from scripts.load import get_image_size, create_image, update_product

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['value']

class ThumbnailSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailSize
        fields = ['url', 'width', 'height']

class ThumbnailSerializer(serializers.ModelSerializer):
    small = ThumbnailSizeSerializer()
    large = ThumbnailSizeSerializer()
    full = ThumbnailSizeSerializer()
    class Meta:
        model = Thumbnail
        fields = ['small', 'large', 'full']

class SingleImageSerializer(serializers.ModelSerializer):
    thumbnail = ThumbnailSerializer()
    class Meta:
        model = Image
        fields = ['id', 'width', 'height', 'url', 'filename', 'size', 'type', 'thumbnail']

class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['url']
        

class SingleProductSerializer(serializers.ModelSerializer):
    # colors = ColorSerializer(many=True)
    # images = ImageSerializer(many=True, read_only=True)

    colors = serializers.SerializerMethodField()
    images = SingleImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'stock', 'price', 'shipping', 'colors', 'category', 'images', 'featured', 'reviews', 'stars', 'description', 'company']
    
    def get_colors(self, obj):
        return [color.value for color in obj.colors.all()]
    
    def create(self, validated_data):
        colors_data = validated_data.pop('colors', [])
        images_data = validated_data.pop('images', [])
        
        product = Product.objects.create(**validated_data)

        
        for color_data in colors_data:
            color_ = Color.objects.get_or_create(**color_data)[0]
            ProductColor.objects.create(product=product, color=color_)

        
        for image_data in images_data:
            image_ = create_image(image_data)
            ProductImage.objects.create(product=product, image=image_)

        return product
    
    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
class ProductSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(source="images")
    # colors = ColorSerializer(many=True)
    # images = SingleImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'image', 'featured',  'colors', 'company', 'description', 'category',  'shipping']
    
    def get_image(self, obj):
        images = obj.images.all()
        if images.exists():
            return images[0].url
        return None 
    
    def get_colors(self, obj):
        return [color.value for color in obj.colors.all()]
    
    def to_representation(self, instance):
        data = super().to_representation(instance)
        if not instance.featured:
            data.pop('featured')
        return data        
    