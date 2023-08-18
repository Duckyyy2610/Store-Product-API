import random
from StoreProductAPI.models import *
from scripts.function import get_or_create_image, get_or_create_thumbnail
from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from StoreProductAPI.serializers import ColorSerializer, SingleImageSerializer, ImageSerializer, ThumbnailSizeSerializer, ThumbnailSerializer, SingleProductSerializer, ProductSerializer

i = Image.objects.filter(url="").first()
i = Image.objects.get(id="61585626-96a3-49fa-9d34-4fb244ab6766") 
i.thumbnail
# <Thumbnail: Thumbnail object (653)>
i.thumbnail.small
# <ThumbnailSize: ThumbnailSize object (1038)>
i.thumbnail.small.width
# 58
i.thumbnail.small.height
# 34
type(get_or_create_thumbnail("https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg")) 
# <class 'StoreProductAPI.models.Thumbnail'>
type(i.thumbnail)
# <class 'StoreProductAPI.models.Thumbnail'>
t = get_or_create_thumbnail("https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg")
t.small.url 
# 'https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg'
tserializer = ThumbnailSerializer(t)
tserializer.data

i.thumbnail.delete()
i.thumbnail = get_or_create_thumbnail("https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg")
type(ThumbnailSerializer(i.thumbnail).data)

# {'small': OrderedDict([('url', 'https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg'), ('width', 60), ('height', 39)]), 
# 'large': OrderedDict([('url', 'https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg'), ('width', 700), ('height', 852)]), '
# full': OrderedDict([('url', 'https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg'), ('width', 3000), ('height', 3000)])}

import re

example_string = "asd///adsadasd...sddsf||sfsdf"


result = re.split('[|, /._+]+', example_string)
print(result)
# ['-company', 'price']
re.split('[/.]+', "-company//////////////price.asfsd") 
# ['-company', 'price', 'asfsd']
re.split('[/.]+', "-company//////..////////price.asfsd") 
# ['-company', 'price', 'asfsd']
re.split('[/. ]+', "-company//  ////..////////p   rice.asfsd") 
# ['-company', 'p', 'rice', 'asfsd']
re.split('[|, /._+]+', "-company//  ////..////////p   rice.asfsd") 
# ['-company', 'p', 'rice', 'asfsd']
re.split('[|, /._+]+', "-compa|,/.+ny//  ////..////////p   rice.|, /._+sfsd") 
# ['-compa', 'ny', 'p', 'rice', 'sfsd']

import random
from StoreProductAPI.models import *
from scripts.function import get_or_create_image, get_or_create_thumbnail
from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from StoreProductAPI.serializers import ColorSerializer, SingleImageSerializer, ImageSerializer, ThumbnailSizeSerializer, ThumbnailSerializer, SingleProductSerializer, ProductSerializer


images = Image.objects.all()

image_url_freq = dict()

[image_url_freq.update({image.url: 1}) for image in images]

for k, v in image_url_freq.items():
    k, v

[print(image) for image in Image.objects.all()]
images[0].url
image_url_freq[images[0]]


import random
from StoreProductAPI.models import *
from scripts.function import get_or_create_image, get_or_create_thumbnail
from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from StoreProductAPI.serializers import ColorSerializer, SingleImageSerializer, ImageSerializer, ThumbnailSizeSerializer, ThumbnailSerializer, SingleProductSerializer, ProductSerializer


product = Product.objects.get(id="2ecfedc0-7b78-4800-972e-117edd9f4adc")
images_from_this_product = product.images.all()
image_url_freq = {image.url: 1 for image in images_from_this_product}
len(images_from_this_product)

images_url_add = ["https://www.course-api.com/images/store/product-2.jpeg", "https://www.course-api.com/images/store/product-7.jpeg"]
images_url_delete = ["https://www.course-api.com/images/store/product-2.jpeg", "https://www.course-api.com/images/store/product-7.jpeg"]

# for k, v in image_url_freq.items():
#     print(k, v)

for image_url in images_url_add:
    if image_url not in image_url_freq:
        image_created = get_or_create_image(image_url, random.randint(900, 1000), random.randint(600, 700), 'image/jpeg')
        product.images.add(image_created)
        image_url_freq[image_url] = 1

# for image_url in images_url_delete:
#     if image_url_freq[image_url]:
#         p.images.remove(p.images.get(url=image_url))

len(images_from_this_product)



import random
from StoreProductAPI.models import *
from scripts.function import get_or_create_image, get_or_create_thumbnail
from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from StoreProductAPI.serializers import ColorSerializer, SingleImageSerializer, ImageSerializer, ThumbnailSizeSerializer, ThumbnailSerializer, SingleProductSerializer, ProductSerializer

p = Product.objects.get(id="2ecfedc0-7b78-4800-972e-117edd9f4adc")
p1 = p.images.all()
p2 = p.productimage_set.all()

print(type(p1[0]), p1.query)
# <class 'django.db.models.query.QuerySet'> SELECT `StoreProductAPI_image`.`id`, `StoreProductAPI_image`.`width`, `StoreProductAPI_image`.`height`, 
# `StoreProductAPI_image`.`url`, 
# `StoreProductAPI_image`.`filename`, `StoreProductAPI_image`.`size`, `StoreProductAPI_image`.`type`, `StoreProductAPI_image`.`thumbnail_id`
# FROM `StoreProductAPI_image` INNER JOIN `StoreProductAPI_productimage` ON (`StoreProductAPI_image`.`id` = `StoreProductAPI_productimage`.`image_id`) 
# WHERE `StoreProductAPI_productimage`.`product_id` = 2ecfedc07b784800972e117edd9f4adc
print(type(p2[0]), p2.query)
# <class 'django.db.models.query.QuerySet'> SELECT `StoreProductAPI_productimage`.`id`, `StoreProductAPI_productimage`.`product_id`, 
# `StoreProductAPI_productimage`.`image_id` FROM `StoreProductAPI_productimage` WHERE `StoreProductAPI_productimage`.`product_id` = 2ecfedc07b784800972e117edd9f4adc




import random
from StoreProductAPI.models import *
from scripts.function import get_or_create_image, get_or_create_thumbnail
from django.shortcuts import render, get_object_or_404
from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from StoreProductAPI.serializers import ColorSerializer, SingleImageSerializer, ImageSerializer, ThumbnailSizeSerializer, ThumbnailSerializer, SingleProductSerializer, ProductSerializer

# url_exists = Image.objects.filter(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-YMONwPlKxEKXfAzkLl5KIieiIaXFl3eL8g&usqp=CAU").first()
# image = Image.objects.get(url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-YMONwPlKxEKXfAzkLl5KIieiIaXFl3eL8g&usqp=CAU")
# image = get_object_or_404(Image, url="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-YMONwPlKxEKXfAzkLl5KIieiIaXFl3eL8g&usqp=CAU")

# url_exists = get_or_create_image("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR-YMONwPlKxEKXfAzkLl5KIieiIaXFl3eL8g&usqp=CAU", 1000, 667, 'image/jpeg')