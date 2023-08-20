import random
import json
import io
import os
import sys
import django

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "StoreProduct.settings") 
# from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
# from StoreProductAPI.serializers import ColorSerializer, SingleImageSerializer, ImageSerializer, ThumbnailSizeSerializer, ThumbnailSerializer, SingleProductSerializer, ProductSerializer

def generate_rgb_hex_list(a, b):
    rgb_hex_list = []
    
    for i in range(a, b):
        rgb_hex = format(i, '06x')
        rgb_hex_list.append(rgb_hex)
                
    return rgb_hex_list

hex_value_colors = generate_rgb_hex_list(1, 1000)
product_images = [
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMIAG8BdpFXEbGJhS2JiBMrqysJ5Rby8mhdg&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS5GuGTdeY8MTGuJ6r2zywehrbVIFlJgMBUsEhiL93phYeeGQidzHPSScixwVprt-KQKZQ&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYR8a7PDmL6mGtD6HSZNmQbMwF0mXanru9rZjuNq4O4QiNRkwUgBV7Dfrx7nk46wGzaHY&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRlylhHb85zbbiNRGpGTbQbMSTAHo80RVWkOQ&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYJ2oM4DJYwTlqzrATnF7HAJ1kAxysg27MjQ&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSbsCEOUSzTnjyiiStU-kRmVRJLCQEi1rQdaQ&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS73UmP_-lBjG7oBLDBuv6fQDlKtiOa2CrxPA&usqp=CAU",
    "https://pgdphurieng.edu.vn/wp-content/uploads/2023/05/minions-rise-of-gru-7.jpg",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTuw8aXHeJjdE_7bIqXJU16js5ETNJMZki2Nvs_rH13k2sWQmKIjhpdI5bGKwmu7K1x1Cs&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ7pfiaAJBtY20UGL_195ubi3QprOL1-qSOEA&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiKD-e8gVTgD4iQkbd_dLwoloZZrezKt1IkQ&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS8_K6GNojjsAh-MYkHbU4rYuX6VOV_e4a6-g&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTow4Zh-5-lY2zLb0i4tFwRGI33WsVKUKl50g&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcStD0CzPQkf6rpbSFX1EbDVqXIXnASx1tGIXQ&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQ041Gpm8K4dVhKcGHUIjwMTlV3ISCZgMVvRg&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTfoj_XCIoJJa4VKRC0nqTNvoo1aXRU9p9Mdv1sedfaseq_rYKl6iinF_LEh_6Aewh9rD8&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQINZxVC7BbbroX2tAHXHykjTyzAyLWS7AfEVX4bmRKMAeWck0d64n5yoUvH4Qj9glM0uA&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcR6KBV2ANxkvQxK3LtQDF2SveLUvk5a2OdA_g&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTQ5ctqhLPNS1IZPUwOxNWMwy52iQyHGYUgKw&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTe5yES6ZB-9W8avq31Jp1g2vd1z7eo7GeNqA&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeoecV6BTnIKRawD5b-yL8Cp5fQAltKGeNSg&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4oLH1So5ZYocGeHOgBMNyURwkmiOkX1dlOA&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSELTg-NKPCjZym0dwx1Z4WntNDSofMO7dRLQ&usqp=CAU"
]
# copy ở trong này
add_images, delete_images, add_colors, delete_colors = [], [], [], []
for i in range(random.randint(1, 6)):  
    add_images.append(random.choice(product_images))

for i in range(random.randint(1, 6)):  
    delete_images.append(random.choice(product_images))

for i in range(random.randint(5, 6)):   
    add_colors.append(random.choice(hex_value_colors))

for i in range(random.randint(1, 5)):   
    delete_colors.append(random.choice(hex_value_colors))


product_name=["Sofa", "Dining Table", "Bed", "Bookshelf", "Coffee Table", "Armchair", 
               "Wardrobe", "TV Stand", "Nightstand", "Desk", "Sectional Sofa", 
               "Cabinet", "Ottoman", "Console Table", "End Table", "Rocking Chair", 
               "Dresser", "Bunk Bed", "Chaise Lounge", "Folding Chair", "Bar Stool", 
               "Sideboard", "Futon", "Accent Chair", "Credenza", "Hall Tree", "Lounge Chair", 
               "Platform Bed", "Recliner", "Vanity Table", "Hammock", "Bean Bag", "Shoe Rack", 
               "Pouf", "Bookcase", "Buffet Table", "Chesterfield Sofa", "Folding Table", 
               "Murphy Bed", "Chandelier", "Nesting Tables", "Storage Bench", "Step Stool", 
               "Gaming Chair", "Daybed", "Bar Cart", "Love Seat", "Room Divider"]

product_price = []

for i in range(100):
    price = round(random.uniform(10000, 1000000), 2)  # Generating random price between 100 and 1000
    product_price.append(price)

product_company = ["StellarTech", "QuantumSolutions", "SwiftFusion", "InnovateWave", "NexusIndustries", "FusionSynergy", 
                   "ApexDynamics", "QuantumCore", "PrimeInnovations", "NovaVentures", "ProdigySystems", "AlphaSolutions",
                    "InfinityEnterprises", "SpectrumTech", "VanguardGroup", "VisionaryIndustries", "AlphaWave", "DynamoInnovations", 
                    "QuantumHorizon", "VertexGlobal", "NebulaDynamics", "EchelonSolutions", "OmegaInnovate", "QuantumStride", 
                    "SynergyWorks", "ZenithEnterprises", "FusionX", "OptimaTech", "PinnacleInnovations", "OrionIndustries",
                    "HyperionSolutions", "InnovateAxis", "QuantumNexa", "AlphaPrime", "SpectrumVentures", "EonSynergy", 
                    "InnovareTech", "StellarPath", "ProximaIndustries", "VelocityWave", "FusionInnovations", "QuantumQuest", 
                    "AstralEnterprises", "VisionWave", "InnovateFusion", "SynergeticSystems", "AlphaDynamics", "QuantumStrive", "NebulaNex", "ApexInnovations"]

product_description = [
    "Elevate your living space with this exquisite and modern home decor piece that seamlessly combines form and function. Crafted with attention to detail, its intricate design and premium materials add a touch of sophistication to any room, creating an ambiance of elegance and style.",
    "Experience the epitome of technological advancement with this cutting-edge electronics device. Designed to push the boundaries of innovation, it delivers unparalleled performance, seamless connectivity, and a user-friendly interface that puts the power of the future in your hands.",
    "Step into the world of high fashion with this meticulously designed clothing item that captures the latest trends and reflects your individual style. Its timeless elegance and superior craftsmanship ensure both comfort and confidence, making it the perfect addition to your wardrobe.",
    "Indulge in a luxurious self-care routine with this premium health and beauty product that pampers your senses and revitalizes your skin. Infused with natural ingredients and advanced formulations, it promises a rejuvenating experience that leaves you feeling refreshed and radiant.",
    "Ignite your passion for adventure with this high-performance sports and outdoors equipment that's built to withstand the elements and conquer new horizons. Whether you're a seasoned athlete or a weekend explorer, this gear empowers you to push your limits and embrace the thrill of the outdoors.",
    "Transform your vehicle into a masterpiece of engineering with this top-of-the-line automotive accessory. Engineered for both style and functionality, it enhances your driving experience while making a bold statement on the road.",
    "Immerse yourself in a captivating world of storytelling with this thought-provoking book that delves deep into the human experience. Its eloquent prose and intricate plot twists keep you engaged from cover to cover, leaving you inspired and introspective.",
    "Nurture creativity and imagination with this meticulously crafted toy or game that sparks joy across generations. Designed to be both entertaining and educational, it encourages interactive play and exploration, fostering a sense of wonder and learning.",
    "Savor the ultimate culinary experience with this collection of gourmet food and beverage selections that tantalize your taste buds and transport you to a world of flavor. From delectable treats to exotic blends, each item is a celebration of taste and craftsmanship.",
    "Adorn yourself with timeless elegance by wearing this exquisite piece of jewelry that encapsulates the essence of luxury. Meticulously designed and crafted, it embodies sophistication and grace, making it the perfect accent for any occasion.",
    "Elevate your living space with this meticulously crafted furniture item that marries functionality with aesthetics. Its ergonomic design and premium materials ensure comfort and durability, while its versatile style effortlessly complements your interior decor.",
    "Effortlessly simplify your daily routine with this innovative and reliable appliance that streamlines tasks and enhances efficiency. Engineered for convenience, it takes care of household chores, giving you more time to focus on what matters most.",
    "Stay organized and productive with this comprehensive collection of office supply essentials that cater to your professional needs. From sleek writing instruments to ergonomic accessories, these items are designed to optimize your workspace and enhance productivity.",
    "Show your furry friend some love with these premium pet supplies that prioritize comfort, safety, and happiness. From cozy beds to interactive toys, each item is thoughtfully chosen to enhance your pet's well-being and bring joy to their everyday life.",
    "Embark on a journey of gardening success with this essential set of tools that empowers you to create a flourishing oasis in your own backyard. From planting to nurturing, these tools ensure a rewarding and satisfying gardening experience.",
    "Embark on new adventures with confidence using this versatile and durable travel and luggage item. Designed for convenience and functionality, it offers ample storage space and innovative features that simplify your travel experience, making every journey memorable.",
    "Unleash your creativity and skills with this comprehensive collection of crafting and hobby materials that cater to enthusiasts of all levels. From DIY projects to intricate creations, these materials provide the foundation for endless artistic exploration.",
    "Cater to your baby's needs with this comprehensive collection of safe and comfortable baby products that prioritize their well-being and comfort. From soothing essentials to practical accessories, each item is designed to make parenting a joyful and rewarding experience.",
    "Achieve your fitness goals with this state-of-the-art fitness equipment that brings the gym experience to the comfort of your home. Designed for maximum effectiveness and versatility, it empowers you to embrace an active lifestyle and pursue your health aspirations.",
]

product_category = ["Home Decor", "Electronics", "Fashion", "Health & Beauty", "Sports & Outdoors", "Automotive", 
                     "Books", "Toys & Games", "Food & Beverages", "Jewelry", "Furniture", "Appliances", "Office Supplies", 
                     "Pet Supplies", "Gardening", "Travel & Luggage", "Crafts & Hobbies", "Baby Products", "Fitness", 
                     "Music", "Movies", "Art & Collectibles", "Electrical", "Outdoor Gear", "Kitchenware", "Party Supplies", 
                     "Tools & Hardware", "Stationery", "Personal Care", "Footwear", "Watches", "Home Improvement", "Cookware", 
                     "Gadgets", "Stationery", "Gifts", "Accessories", "Lifestyle", "Electrical", "Bed & Bath", "Stationery", 
                     "Entertainment", "Home Organization", "Home Cleaning", "Home Textiles", "Cosmetics", "Fashion Accessories", "Pet Care", "DIY Kits"]
# product_id = [product.id for product in Product.objects.all()]
# image_id = [image.id for image in Image.objects.all()]
product_id = ['05e56409-f6ce-4d83-b4c1-fcecfbd6371e', '0c19b568-70ab-47c2-9844-03f45b45fc5a', 
              '1da4e9f6-e0b9-4c20-8668-4389d3ca1355', '2ecfedc0-7b78-4800-972e-117edd9f4adc', 
              '302f8315-5784-4838-ad1d-b9b21cdd8314', '30f95257-c3b5-4783-a9f8-7bea6f6b3eb0', 
              '3995d9dc-c898-4d08-bc61-ddf4853fbc68', '3ee777bf-6a7e-47a5-a1f3-06f9e9cf8a0a', 
              '42c14be0-64f1-4bee-8bd7-31b10f29d7fa', '48fc0b3c-ac0c-45d1-881c-2866a73a28a2', 
              '518fe6c2-59d8-4029-aa8b-b00cec96a95d', '8655a5f3-7721-4afd-8152-d4f080be3d84', 
              '8751a3f0-d9f2-4087-b858-36cb9309ea07', '8fb2d527-50d4-4f11-8929-8787f6b3ef67', 
              '9658a42e-c401-4600-ba1f-476a4e6e084b', '98718eb8-db8a-4c86-8b02-f6b3974deabf', 
              '9b1e2e6f-fc53-4ea4-b15c-dab5bff451a4', 'a7107f67-ea6f-4a11-8809-219ff6306f59', 
              'c48cbf49-0b8d-4209-a9dd-2af9b8c573c6', 'cf056f3a-27c8-45cf-a0c0-fce6fd92fff0', 
              'e813c460-35be-494c-9d2c-fcee50fb7e4d', 'fe854d54-ebab-4281-b187-4331762c9aa0']

image_id = ['05e2745e-e87a-491a-a9f6-f7f638da1be1', '0a2ff626-4b75-4fac-bb87-43c783a1698a', '0bf4a0ad-6010-4c69-8655-2b5abfe600fd', 
            '0fc8b159-b9a4-4b3f-bd99-1436b1662deb', '11be4072-5dcf-4427-8924-8952722a56f2', '1e62141f-da2b-4332-adec-a64d604f1c04', 
            '1e8257be-306e-48c0-866e-d623c10a88dc', '1fefde03-84ec-4ebd-b18d-e82bebdb05e7', '21acc31b-85e6-4fed-a8fc-61b3f58ad639', 
            '2ccf89dd-a9a7-4117-8fc7-efb9e36c383d', '321a6569-1e40-4e47-8834-0e50cb46cde2', '362ed3b5-dfaf-488a-bc7b-c56f34bdd1ba', 
            '3b0ec889-41a7-422e-841a-1747978c9a64', '51ef20a7-080b-4d4e-8816-357b5ae5cb2a', '545c2328-5757-42a1-ad2e-e209c89aaa79', 
            '69750286-50bf-4093-93ae-f9c102c4ed8a', '6a7b77bb-e63e-4b40-80f9-e0f12058b368', '6e169951-ce62-4231-9338-7a74364b8af0', 
            '759113cf-7c65-46d9-b07b-000ad19f9615', '773f97c6-cf21-457c-bec2-49572551f6ab', '78541e1a-05e1-41c9-bef7-e89266aab8c8', 
            '7c70db88-6ad9-4b18-816f-38c7a749b0aa', '821fe7b6-94af-4ac3-a116-4383dac6854c', '85500de8-73f1-40b4-b06d-41187593b3b1', 
            '8681fac2-055d-4b8f-ba12-6e779f509991', '8954cd58-f543-4532-bd7e-b84e77df8b8d', '9592a967-f0a0-409f-ae7a-8049300e7b6b', 
            '964884e2-f920-4d80-a555-5e985c3f2cc5', '98c9882a-489f-4805-88b9-83ee6e4bf957', 'a1f3daeb-d858-4f74-a2cc-caa794f22502', 'a38f9bb5-1a23-4233-a6b9-5124c932e3ce', 'a655e815-feff-4a61-be53-8f84c292f026', 'a9a7219a-da0a-4648-8326-76de95107d08', 'aaf66bb5-bf3c-4d11-9909-ceda4e3cd5d3', 'b8c7f1ec-fbaf-4f44-8d96-fcfc1bf88ad7', 'b9bf9f80-0748-4cbc-b9fb-9e6dae83bd40', 'c3473382-eca5-424b-b017-4e287580e0ce', 'cf995124-6484-431b-b0ad-823df3dd9e66', 'db7159da-f8ea-428a-9a0e-0911ceb9b4f7', 'db76434e-d93c-4386-b212-3080634ebc93', 'dcda953e-1f4c-4248-bfee-eb26ab3a728a', 'df8813f9-3626-4c09-aeac-0575b524f3dd', 'ebdebf25-0383-40a6-9236-dfd834e4dba0']

apiendpoints = []
product_modify = []

url = "# /store/store-products/<uuid:pk> patch"
product = {
    "add_images": add_images,
    "delete_images": delete_images,
    "add_colors": add_colors,
    "delete_colors": delete_colors
}
product_modify.append(product)
apiendpoints.append(url)

url = "# /store/store-products/<uuid:pk> put"
product = {
    "name": random.choice(product_name),
    "price": random.choice(product_price),
    "company": random.choice(product_company),
    "description": random.choice(product_description),
    "category": random.choice(product_category),
    # option
    # "add_images": add_images,
    # "delete_images": delete_images,
    # "add_colors": add_colors,
    # "delete_colors": delete_colors
}
product_modify.append(product)
apiendpoints.append(url)

url = "#/store/store-products/ patch"
product = {
    "id": random.choice(product_id),
    "add_images": add_images,
    "delete_images": delete_images,
    "add_colors": add_colors,
    "delete_colors": delete_colors
}
product_modify.append(product)
apiendpoints.append(url)

url = "#/store/store-products/ put"
product = {
    "id": random.choice(product_id),
    "name": random.choice(product_name),
    "price": random.choice(product_price),
    "company": random.choice(product_company),
    "description": random.choice(product_description),
    "category": random.choice(product_category),
}
product_modify.append(product)
apiendpoints.append(url)

url = "#/store/store-products/ put" 
product = {
    "id": random.choice(product_id), # post thì k cần id
    "name": random.choice(product_name),
    "price": random.choice(product_price),
    "company": random.choice(product_company),
    "description": random.choice(product_description),
    "category": random.choice(product_category),
    "add_images": add_images,
    "delete_images": delete_images,
    "add_colors": add_colors,
    "delete_colors": delete_colors
}
product_modify.append(product)
apiendpoints.append(url)

url = "#/store/store-products/<uuid:pk> put  #/store/store-products/ post"
product = {
    "name": random.choice(product_name),
    "price": random.choice(product_price),
    "company": random.choice(product_company),
    "description": random.choice(product_description),
    "category": random.choice(product_category),
    "add_images": add_images,
    "delete_images": delete_images,
    "add_colors": add_colors,
    "delete_colors": delete_colors
}
product_modify.append(product)
apiendpoints.append(url)

url = "/store/image-products/ put" 
image = {
    "id": random.choice(image_id),
    "width": random.randint(900, 1000),
    "height": random.randint(600, 700),
    "url": random.choice(product_images),
    "type": "image/jpeg"
}
product_modify.append(image)
apiendpoints.append(url)

url = "/store/image-products/ put" 
image = {
    "width": random.randint(900, 1000),
    "height": random.randint(600, 700),
    "url": random.choice(product_images),
    "type": "image/jpeg"
}
product_modify.append(image)
apiendpoints.append(url)

url = "/store/image-products/<uuid:pk> post"
image = {
    "width": random.randint(900, 1000),
    "height": random.randint(600, 700),
    "url": random.choice(product_images),
    "type": "image/jpeg"
}
product_modify.append(image)
apiendpoints.append(url)

flag = ''
for i in range(len(product_modify)):
    flag = 'w' if i==0 else 'a'
    with open('scripts/data.json', flag) as json_file:
        json.dump({"URL to modify": apiendpoints[i]}, json_file, indent=5)
        json_file.write('\n')
        json.dump(product_modify[i], json_file, indent=5)
        json_file.write("\n\n")