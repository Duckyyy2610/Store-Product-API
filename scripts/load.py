import requests
import json
import random
import json
from django.db import connection
from PIL import Image as img
from io import BytesIO
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


def run():

    # with connection.cursor() as cursor:
    #     cursor.execute("SELECT setval(pg_get_serial_sequence('StoreProductAPI_color_id_seq'), 1, false);")

    url = "https://course-api.com/react-store-products"  # Replace with the actual URL

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception if the HTTP request returns an error
        json_data = response.json()  # Parse the JSON content from the response
        
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
            width_large, height_large = get_image_size(data['image'])
            thumbnail_small, created = ThumbnailSize.objects.get_or_create(
                url=data['image'], 
                width=random.randint(50, 60),
                height=random.randint(30,40)
            )
            
            thumbnail_large, created = ThumbnailSize.objects.get_or_create(
                url=data['image'],
                width=width_large, 
                height=height_large
            )
            
            thumbnail_full, created = ThumbnailSize.objects.get_or_create(
                url=data['image'], 
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
                url=data['image'], 
                type='image/jpeg', 
                thumbnail=thumbnail
            )
           
            product, created =Product.objects.get_or_create(
                name=data['name'],
                stock=random.randint(1, 30),
                price=data['price'],
                category=data['category'],
                reviews=random.randint(10, 10000),
                stars=random.randint(1, 5),
                description=data['description'],
                company=data['company'],
            )

            for color in data['colors']:
                color_, created = Color.objects.get_or_create(value=color)
                product_color, created = ProductColor.objects.get_or_create(color=color_, product=product)
            
            product_color, created = ProductImage.objects.get_or_create(image=image_, product=product)
            for i in range(random.randint(1, len(image_url_arr))):
                random_url_image = random.choice(image_url_arr)
                print(random_url_image)
                image_, created = Image.objects.get_or_create(
                    width=1000,
                    height=667, 
                    url=random_url_image, 
                    type='image/jpeg', 
                    thumbnail=thumbnail
                )
                product_color, created = ProductImage.objects.get_or_create(image=image_, product=product)

    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
    except json.JSONDecodeError as e:
        print("Error decoding JSON:", e)



# The complete JSON data
    # json_data = '''
    #     {
    #     "id": "rec1Ntk7siEEW9ha1",
    #     "stock": 0,
    #     "price": 23999,
    #     "shipping": true,
    #     "colors": [
    #         "#0000ff",
    #         "#000"
    #     ],
    #     "category": "bedroom",
    #     "images": [
    #         {
    #             "id": "attub6EG88kJKuYs8",
    #             "width": 1000,
    #             "height": 667,
    #             "url": "https://www.course-api.com/images/store/product-6.jpeg",
    #             "filename": "product-4.jpeg",
    #             "size": 49641,
    #             "type": "image/jpeg",
    #             "thumbnails": {
    #                 "small": {
    #                     "url": "https://www.course-api.com/images/store/product-6.jpeg",
    #                     "width": 54,
    #                     "height": 36
    #                 },
    #                 "large": {
    #                     "url": "https://www.course-api.com/images/store/product-6.jpeg",
    #                     "width": 768,
    #                     "height": 512
    #                 },
    #                 "full": {
    #                     "url": "https://www.course-api.com/images/store/product-6.jpeg",
    #                     "width": 3000,
    #                     "height": 3000
    #                 }
    #             }
    #         },
    #         {
    #             "id": "attaeT2Dex98o2jfW",
    #             "width": 1000,
    #             "height": 667,
    #             "url": "https://www.course-api.com/images/store/extra-product-1.jpeg",
    #             "filename": "extra-1.jpeg",
    #             "size": 102108,
    #             "type": "image/jpeg",
    #             "thumbnails": {
    #                 "small": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-1.jpeg",
    #                     "width": 54,
    #                     "height": 36
    #                 },
    #                 "large": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-1.jpeg",
    #                     "width": 768,
    #                     "height": 512
    #                 },
    #                 "full": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-1.jpeg",
    #                     "width": 3000,
    #                     "height": 3000
    #                 }
    #             }
    #         },
    #         {
    #             "id": "attWsZasaaRD1P7mm",
    #             "width": 1000,
    #             "height": 714,
    #             "url": "https://www.course-api.com/images/store/extra-product-2.jpeg",
    #             "filename": "extra-2.jpeg",
    #             "size": 84418,
    #             "type": "image/jpeg",
    #             "thumbnails": {
    #                 "small": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-2.jpeg",
    #                     "width": 50,
    #                     "height": 36
    #                 },
    #                 "large": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-2.jpeg",
    #                     "width": 717,
    #                     "height": 512
    #                 },
    #                 "full": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-2.jpeg",
    #                     "width": 3000,
    #                     "height": 3000
    #                 }
    #             }
    #         },
    #         {
    #             "id": "attTvaiDcADaAItLw",
    #             "width": 1000,
    #             "height": 650,
    #             "url": "https://www.course-api.com/images/store/extra-product-3.jpeg",
    #             "filename": "extra-3.jpeg",
    #             "size": 107838,
    #             "type": "image/jpeg",
    #             "thumbnails": {
    #                 "small": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-3.jpeg",
    #                     "width": 55,
    #                     "height": 36
    #                 },
    #                 "large": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-3.jpeg",
    #                     "width": 788,
    #                     "height": 512
    #                 },
    #                 "full": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-3.jpeg",
    #                     "width": 3000,
    #                     "height": 3000
    #                 }
    #             }
    #         },
    #         {
    #             "id": "attdxQmF0aCH5I32F",
    #             "width": 1000,
    #             "height": 667,
    #             "url": "https://www.course-api.com/images/store/extra-product-4.jpeg",
    #             "filename": "extra-4.jpeg",
    #             "size": 99481,
    #             "type": "image/jpeg",
    #             "thumbnails": {
    #                 "small": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-4.jpeg",
    #                     "width": 54,
    #                     "height": 36
    #                 },
    #                 "large": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-4.jpeg",
    #                     "width": 768,
    #                     "height": 512
    #                 },
    #                 "full": {
    #                     "url": "https://www.course-api.com/images/store/extra-product-4.jpeg",
    #                     "width": 3000,
    #                     "height": 3000
    #                 }
    #             }
    #         }
    #     ],
    #     "reviews": 60,
    #     "stars": 5,
    #     "name": "emperor bed",
    #     "description": "Cloud bread VHS hell of banjo bicycle rights jianbing umami mumblecore etsy 8-bit pok pok +1 wolf. Vexillologist yr dreamcatcher waistcoat, authentic chillwave trust fund. Viral typewriter fingerstache pinterest pork belly narwhal. Schlitz venmo everyday carry kitsch pitchfork chillwave iPhone taiyaki trust fund hashtag kinfolk microdosing gochujang live-edge",
    #     "company": "ikea"
    # }
    # '''

    # # Load the JSON data
    # product_data = json.loads(json_data)
    # colors_data = product_data.pop('colors')
    # images_data = product_data.pop('images')
    # # Access the loaded data
    # print(colors_data)
    # print(images_data)
    # ... and so on for other attributes

