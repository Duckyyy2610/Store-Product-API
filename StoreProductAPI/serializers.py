from .models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from rest_framework import serializers
import random
from scripts.load import get_image_size

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
    # colors = ColorSerializer(many=True, read_only=True)
    # images = ImageSerializer(many=True, read_only=True)

    colors = ColorSerializer(many=True)
    images = ImageSerializer(many=True)
    class Meta:
        model = Product
        fields = ['id', 'name', 'stock', 'price', 'shipping', 'colors', 'category', 'images', 'featured', 'reviews', 'stars', 'description', 'company']
    
    def create(self, validated_data):
        # Extract the colors and images data
        colors_data = validated_data.pop('colors', [])
        images_data = validated_data.pop('images', [])
        print(type(colors_data))
        # Create the product instance
        product = Product.objects.create(**validated_data)

        # Create the related colors (through the ProductColor model)
        for color_data in colors_data:
            color = Color.objects.get_or_create(**color_data)[0]
            ProductColor.objects.create(product=product, color=color)

        # Create the related images (through the ProductImage model)
        for image_data in images_data:
            width_large, height_large = get_image_size(image_data['url'])
            thumbnail_small, created = ThumbnailSize.objects.get_or_create(
                url=image_data['url'], 
                width=random.randint(50, 60),
                height=random.randint(30,40)
            )
            
            thumbnail_large, created = ThumbnailSize.objects.get_or_create(
                url=image_data['url'],
                width=width_large, 
                height=height_large
            )
            
            thumbnail_full, created = ThumbnailSize.objects.get_or_create(
                url=image_data['url'], 
                width=3000,
                height=3000
            )

            thumbnail, created = Thumbnail.objects.get_or_create(
                small=thumbnail_small, 
                large=thumbnail_large, 
                full=thumbnail_full
            )
            
            image_, created = Image.objects.get_or_create(
                width=1000,
                height=667, 
                url=image_data['url'], 
                type='image/jpeg', 
                thumbnail=thumbnail
            )
            ProductImage.objects.create(product=product, image=image_)

        return product
    
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
    