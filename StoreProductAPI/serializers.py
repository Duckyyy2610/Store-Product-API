import random
from django.db import transaction
from scripts.function import get_image_size, get_or_create_image, get_or_create_thumbnail, add_or_delete, get_ordering
from rest_framework import serializers
from .models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage

class ColorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Color
        fields = ['id', 'value']

class ThumbnailSizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ThumbnailSize
        fields = ['url', 'width', 'height']

class ThumbnailSerializer(serializers.ModelSerializer):
    small = ThumbnailSizeSerializer(read_only=True, required=False)
    large = ThumbnailSizeSerializer(read_only=True, required=False)
    full = ThumbnailSizeSerializer(read_only=True, required=False)
    class Meta:
        model = Thumbnail
        fields = ['small', 'large', 'full']

class SingleImageSerializer(serializers.ModelSerializer):
    thumbnail = ThumbnailSerializer(required=False, read_only=True)
    class Meta:
        model = Image
        fields = ['id', 'width', 'height', 'url', 'filename', 'size', 'type', 'thumbnail']
        # extra_kwargs = {'thumbnail': {'required': False}}

    def create(self, validated_data):
        image = get_or_create_image(validated_data['url'], validated_data['width'], validated_data['height'], validated_data['type'])
        image.save()
        return image
        

    def update(self, instance, validated_data):
        # Update the main image data
        instance.width = validated_data.get('width', instance.width)
        instance.height = validated_data.get('height', instance.height)
        instance.url = validated_data.get('url', instance.url)
        instance.filename = validated_data.get('filename', instance.filename)
        instance.size = validated_data.get('size', instance.size)
        instance.type = validated_data.get('type', instance.type)
      
        url = validated_data.get('url', None)

        if url is not None:
            instance.thumbnail = get_or_create_thumbnail(url)
        
        instance.save()
        return instance     

class ImageSerializer(serializers.ModelSerializer):
    thumbnail = ThumbnailSerializer(read_only=True, required=False)
    class Meta:
        model = Image
        fields = ['id', 'width', 'height', 'url', 'filename', 'size', 'type', 'thumbnail']
        

class SingleProductSerializer(serializers.ModelSerializer):
    # colors = ColorSerializer(many=True)
    # images = ImageSerializer(many=True, read_only=True)

    colors = serializers.SerializerMethodField(required=False)
    images = SingleImageSerializer(many=True, required=False)
    class Meta:
        model = Product
        fields = ['id', 'name', 'stock', 'price', 'shipping', 'colors', 'category', 'images', 'featured', 'reviews', 'stars', 'description', 'company']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Allow partial updates (PATCH) without requiring certain fields
        self.partial = kwargs.get('partial', False)
        if self.partial:
            for field_name in ['name', 'stock', 'price', 'category', 'company']:
                self.fields.pop(field_name)

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
            image_ = get_or_create_image(image_data)
            ProductImage.objects.create(product=product, image=image_)
    
        product.save()
        return product
    
    def update(self, instance, validated_data):
        # Override the update method to handle partial updates
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    

class PartialProductSerializer(SingleProductSerializer):
    def update(self, instance, validated_data):
        # Override the update method to handle partial updates
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        colors_data = validated_data.pop("colors", [])
        images_data = validated_data.pop("images", [])

        if 'add_colors' in self.initial_data or 'delete_colors' in self.initial_data:
            add_colors = self.initial_data.get('add_colors', [])
            delete_colors = self.initial_data.get('delete_colors', [])
            instance = add_or_delete(instance, 'colors', add_colors, delete_colors)

        if 'add_images' in self.initial_data or 'delete_images' in self.initial_data:
            add_images = self.initial_data.get('add_images', [])
            delete_images = self.initial_data.get('delete_images', [])
            instance = add_or_delete(instance, 'images', add_images, delete_images)

        instance.save()
        return instance
class ProductSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(source="images")
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
    