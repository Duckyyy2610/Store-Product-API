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


def run():
    url = "https://course-api.com/react-store-products"  

    try:
        response = requests.get(url)
        response.raise_for_status() 
        json_data = response.json()  
        
        Color.objects.all().delete()
        ThumbnailSize.objects.all().delete()
        Thumbnail.objects.all().delete()
        Image.objects.all().delete()
        Product.objects.all().delete()
        
        image_url_arr = []
        for data in json_data:
            image_url_arr.append(data['image'])
        print(image_url_arr)

        for data in json_data:
            image_ = create_image(data['image'], 1000, 667, 'image/jpeg')
            
            featured_value = False
            if data['name'] in ['entertainment center', 'high-back bench', 'modern bookshelf']:
                featured_value = True

            product, created =Product.objects.get_or_create(
                name=data['name'],
                stock=random.randint(1, 30),
                price=data['price'],
                featured=featured_value,
                category=data['category'],
                reviews=random.randint(10, 10000),
                stars=random.randint(1, 5),
                description=data['description'],
                company=data['company'],
            )

            for color in data['colors']:
                color_, created = Color.objects.get_or_create(value=color)
                product_color, created = ProductColor.objects.get_or_create(color=color_, product=product)
            
            image_all = Image.objects.all()
            for i in range(4):
                random_image = random.choice(image_all)
                product.images.add(random_image)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)



# The complete JSON data
    json_data = '''
        {
    "id": "001ea43c-fdaf-4cec-96ca-75995001693b",
    "name": "entertainment center",
    "stock": 30,
    "price": "59999.00",
    "shipping": false,
    "colors": [
            {"value":"#f0f"},
            {"value":"#f3f"},
            {"value":"#3f9"}
    ],
    "category": "living room",
    "images": [
        {
            "id": "cc923305-83d1-4f69-b22b-1b29dfe29c0e",
            "width": 1000,
            "height": 667,
            "url": "https://www.course-api.com/images/store/product-7.jpeg",
            "filename": null,
            "size": null,
            "type": "image/jpeg",
            "thumbnail": {
                "small": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 56,
                    "height": 36
                },
                "large": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 709,
                    "height": 512
                },
                "full": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 3000,
                    "height": 3000
                }
            }
        },
        {
            "id": "7a69a4ab-2e38-4eb4-bed6-7df644be55f0",
            "width": 1000,
            "height": 667,
            "url": "https://www.course-api.com/images/store/product-1.jpeg",
            "filename": null,
            "size": null,
            "type": "image/jpeg",
            "thumbnail": {
                "small": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 56,
                    "height": 36
                },
                "large": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 709,
                    "height": 512
                },
                "full": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 3000,
                    "height": 3000
                }
            }
        },
        {
            "id": "3fa66cfd-809f-44a4-9f1a-8bed8f0c59db",
            "width": 1000,
            "height": 667,
            "url": "https://www.course-api.com/images/store/product-4.jpeg",
            "filename": null,
            "size": null,
            "type": "image/jpeg",
            "thumbnail": {
                "small": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 56,
                    "height": 36
                },
                "large": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 709,
                    "height": 512
                },
                "full": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 3000,
                    "height": 3000
                }
            }
        },
        {
            "id": "324cdf2d-9c55-4b66-bc26-0d46b2a1e3e4",
            "width": 1000,
            "height": 667,
            "url": "https://www.course-api.com/images/store/product-20.jpeg",
            "filename": null,
            "size": null,
            "type": "image/jpeg",
            "thumbnail": {
                "small": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 56,
                    "height": 36
                },
                "large": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 709,
                    "height": 512
                },
                "full": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 3000,
                    "height": 3000
                }
            }
        },
        {
            "id": "8e19482b-227d-417d-87cf-2f93b58c402b",
            "width": 1000,
            "height": 667,
            "url": "https://www.course-api.com/images/store/product-12.jpeg",
            "filename": null,
            "size": null,
            "type": "image/jpeg",
            "thumbnail": {
                "small": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 56,
                    "height": 36
                },
                "large": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 709,
                    "height": 512
                },
                "full": {
                    "url": "https://www.course-api.com/images/store/product-7.jpeg",
                    "width": 3000,
                    "height": 3000
                }
            }
        }
    ],
    "featured": true,
    "reviews": 3947,
    "stars": 1,
    "description": "Cloud bread VHS hell of banjo bicycle rights jianbing umami mumblecore etsy 8-bit pok pok +1 wolf. Vexillologist yr dreamcatcher waistcoat, authentic chillwave trust fund. Viral typewriter fingerstache pinterest pork belly narwhal. Schlitz venmo everyday carry kitsch pitchfork chillwave iPhone taiyaki trust fund hashtag kinfolk microdosing gochujang live-edge",
    "company": "caressa"
}
    '''

    # Load the JSON data
    # product_data = json.loads(json_data)
    # # colors_data = product_data.pop('colors')
    # images_data = product_data.pop('images')
    # # Access the loaded data
    # print(product_data['colors'], len(product_data['colors']))
    # print(images_data)
    

