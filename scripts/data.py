import random
import json

def generate_rgb_hex_list(a, b):
    rgb_hex_list = []
    
    for i in range(a, b):
        rgb_hex = format(i, '06x')
        rgb_hex_list.append(rgb_hex)
                
    return rgb_hex_list

hex_value_colors = generate_rgb_hex_list(1, 1000)
images = [
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
    add_images.append(random.choice(images))

for i in range(random.randint(1, 6)):  
    delete_images.append(random.choice(images))

for i in range(random.randint(5, 6)):   
    add_colors.append(random.choice(hex_value_colors))

for i in range(random.randint(1, 5)):   
    delete_colors.append(random.choice(hex_value_colors))

data = {
    # "add_images": add_images,
    # "delete_images": delete_images,
    "add_colors": add_colors,
    "delete_colors": delete_colors
}

print(json.dumps(data))