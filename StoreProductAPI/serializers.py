import random
from django.db import transaction
from scripts.load import get_image_size, create_image, create_thumbnail
from rest_framework import serializers
from .models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage

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


    def create(self, validated_data):
        image = create_image(validated_data['url'], validated_data['width'], validated_data['height'], validated_data['type'])
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
        
        # Save the updated image data
        instance.save()
      
        # Update thumbnail data if provided
        url = validated_data.get('url', None)
        if url is not None:
            thumbnail_data = create_thumbnail(url)
        
            instance.thumbnail.small.width = thumbnail_data.small.width
            instance.thumbnail.small.height = thumbnail_data.small.height
            instance.thumbnail.small.url = thumbnail_data.small.url
            instance.thumbnail.small.save()

            instance.thumbnail.large.width = thumbnail_data.large.width
            instance.thumbnail.large.height = thumbnail_data.large.height
            instance.thumbnail.large.url = thumbnail_data.large.url
            instance.thumbnail.large.save()

            instance.thumbnail.full.width = thumbnail_data.full.width
            instance.thumbnail.full.height = thumbnail_data.full.height
            instance.thumbnail.full.url = thumbnail_data.full.url
            instance.thumbnail.full.save()

            instance.save()

        return instance     

class ImageSerializer(serializers.ModelSerializer):
    thumbnail = ThumbnailSerializer()
    class Meta:
        model = Image
        fields = ['id', 'width', 'height', 'url', 'filename', 'size', 'type', 'thumbnail']
        

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

        product.save()
        return product
    
    def update(self, instance, validated_data):
        colors_data = validated_data.pop("colors", [])
        images_data = validated_data.pop("images", [])
            
        #  freq_color = dict()
        # freq_image = dict()
        # [freq_color.update({str(obj).split()[-1]: 1}) for obj in product.productcolor_set.all()] 
        # [freq_color.update({str(obj).split()[-1]: 1}) for obj in product.productcolor_set.all()] 
        
        instance.colors.clear()
        for color_data in colors_data:
            color_obj, created = Color.objects.get_or_create(**color_data)
            instance.colors.add(color_obj)

        instance.images.clear()
        for image_data in images_data:
            image_obj = create_image(image_data, image_data['width'], image_data['height'], 'image/jpeg')
            instance.images.add(image_obj)
        
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

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
    