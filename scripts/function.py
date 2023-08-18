import requests
import json
import random
import json
import re
from django.db import connection
from PIL import Image as img
from io import BytesIO
from rest_framework.response import Response
from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage

def get_image_size(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        image = img.open(BytesIO(response.content))
        width, height = image.size
        return width, height
    except requests.exceptions.RequestException as e:
        print("An error occurred while fetching the image:", e)
    except (IOError, OSError) as e:
        print("Error opening the image:", e)
    except Exception as e:
        print("An unexpected error occurred:", e)


def get_or_create_thumbnail(url):
    
    thumbnail_small, created = ThumbnailSize.objects.get_or_create(
        url=url, 
        width=random.randint(50, 60),
        height=random.randint(30, 40)
    )

    width_large, height_large = get_image_size(url)
    thumbnail_large, created = ThumbnailSize.objects.get_or_create(
        url=url,
        width=width_large, 
        height=height_large
    )

    thumbnail_full, created = ThumbnailSize.objects.get_or_create(
        url=url, 
        width=3000,
        height=3000
    )
    
    thumbnail, _ = Thumbnail.objects.get_or_create(
        small=thumbnail_small,
        large=thumbnail_large,
        full=thumbnail_full
    )
    return thumbnail


def get_or_create_image(image_data_url, width, height, type):
    
    url_exists = Image.objects.filter(url=image_data_url).first()
    if url_exists:
        return url_exists

    thumbnail = get_or_create_thumbnail(image_data_url)

    image_obj, created = Image.objects.get_or_create(
        thumbnail=thumbnail,
        width=width,
        height=height,
        url=image_data_url,
        filename=None,
        size=None,
        type=type,
    )
    return image_obj


def get_ordering(instance, ordering_data):
    ordering_fields = re.split('[|, /._+]+', ordering_data)
    return instance.order_by(*ordering_fields)

def add_or_delete(instance, instance_related, add_data, delete_data):
    instance_related_for_this_instance = instance[instance_related].all() 
    data_freq = dict()
    instance__ = instance[instance_related]

    for data in instance_related_for_this_instance:
        if instance_related == 'images':    
            data_freq.update({data.url: 1})
        elif instance_related == 'colors':
            data_freq.update({data.value: 1})

    for data in add_data:
        if data not in data_freq:
            instance_created = None
            
            if instance_related == 'images':
                instance_created = get_or_create_image(data, random.randint(900, 1000), random.randint(600, 700), 'image/jpeg')

            elif instance_related == 'colors':
                instance_created, _ = Color.objects.get_or_create(value=data)

            instance__.add(instance_created)
            data_freq[data] = 1
    

    for data in delete_data:
        if data_freq.get(data, 0):
            get_instance = None
            if instance_related == 'images':
                get_instance = instance__.filter(url=data).first()
            elif instance_related == 'colors':
                get_instance = instance__.filter(value=data).first()


            if len(instance_related_for_this_instance) and get_instance is not None:
                instance__.remove(get_instance)
            else:
                break
            data_freq[data] = 0
            
    return instance 