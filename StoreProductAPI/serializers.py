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
            instance.thumbnail.save()
        
        instance.save()
        return instance     

class ImageSerializer(serializers.ModelSerializer):
    thumbnail = ThumbnailSerializer(read_only=True, required=False)
    class Meta:
        model = Image
        fields = ['id', 'width', 'height', 'url', 'filename', 'size', 'type', 'thumbnail']
        

class SingleProductSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField(required=False)
    images = SingleImageSerializer(many=True, required=False)
    # shipping = serializers.Serializer(required=False)
    class Meta:
        model = Product
        fields = ['id', 'name', 'stock', 'price', 'shipping', 'colors', 'category', 'images', 'featured', 'reviews', 'stars', 'description', 'company']

    def get_colors(self, obj):
        return [color.value for color in obj.colors.all()]
    
    def validate(self, data):
        super().validate(data)
        # Include the 'add_images' and 'add_colors' fields in validated_data
        data['add_images'] = self.initial_data.get('add_images', [])
        data['add_colors'] = self.initial_data.get('add_colors', [])
        data['delete_images'] = self.initial_data.get('delete_images', [])
        data['delete_colors'] = self.initial_data.get('delete_colors', [])

        return data

    def create(self, validated_data):
        
        """
        validated_data in create method is different from the update method
        This behavior can be explained by how DRF handles updates. When you perform a PUT request, 
        DRF attempts to validate the data by running the validation methods, but it also merges the incoming data with the instance data. 
        This means that the PUT request data contains all fields for the instance, including the additional fields like add_images, delete_images, etc.,
        that you're processing in the validate method. Since the fields are being passed to the serializer, 
        they are still available during the update process even if the validate method is removed.

        The PUT request in DRF effectively does a full update of the instance, 
        meaning it takes the incoming data and replaces the existing instance data with it. 
        As a result, if you're not actually using the data processed in the validate method during the update process, 
        you might not see any issues even if you remove the validate method.

        On the other hand, the POST request doesn't have this merging behavior; it's creating a new instance from scratch. 
        That's why the validate method is crucial in your case to properly process the additional fields and include them in the data when creating a new instance.

        If you intend to continue using these additional fields for updates and want to ensure their proper handling and validation, 
        it's recommended to keep the validate method in place. This way, your code will remain consistent and maintainable in both POST and PUT scenarios.
        """

        add_images = validated_data.pop('add_images', [])
        delete_images = validated_data.pop('delete_images', [])

        add_colors = validated_data.pop('add_colors', [])
        delete_colors = validated_data.pop('delete_colors', [])

        product = Product.objects.create(**validated_data)
        product_ = add_or_delete(product, 'images', add_images, delete_images)
        product_ = add_or_delete(product, 'colors', add_colors, delete_colors)

        product.save()
        return product
    
    def update(self, instance, validated_data):
        add_images = validated_data.pop('add_images', [])
        delete_images = validated_data.pop('delete_images', [])

        add_colors = validated_data.pop('add_colors', [])
        delete_colors = validated_data.pop('delete_colors', [])
        
        íntance_ = add_or_delete(instance, 'images', add_images, delete_images)
        instance_ = add_or_delete(instance, 'colors', add_colors, delete_colors)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance
    
class ProductSerializer(serializers.ModelSerializer):
    colors = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField(source="images")
    # shipping = serializers.Serializer(required=False)
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
    