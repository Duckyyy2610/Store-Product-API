import requests
import json
import random
import json
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


def create_thumbnail(url):
    url_exists = Image.objects.filter(url=url).first()
    if url_exists is not None:
        return url_exists.thumbnail
    
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


def create_image(image_data_url, width, height, type):

    thumbnail = create_thumbnail(image_data_url)

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

