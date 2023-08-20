class Person:
    def __init__(self, name):
        self.name = name
    def a (self):
        name = "Vanity Table",
        price =  498967.83,
        company = "StellarPath",
        description = "Savor the ultimate culinary experience with this collection of gourmet food and beverage selections that tantalize your taste buds and transport you to a world of flavor. From delectable treats to exotic blends, each item is a celebration of taste and craftsmanship.",
        category = "Jewelry",
        print(name, price, company, description, category)

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"'{key}' attribute not found")

class Child(Person):
    def a(self):
        super().a()
        add_images= [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQINZxVC7BbbroX2tAHXHykjTyzAyLWS7AfEVX4bmRKMAeWck0d64n5yoUvH4Qj9glM0uA&usqp=CAU"
        ],
        delete_images = [
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcS4oLH1So5ZYocGeHOgBMNyURwkmiOkX1dlOA&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSMIAG8BdpFXEbGJhS2JiBMrqysJ5Rby8mhdg&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTiKD-e8gVTgD4iQkbd_dLwoloZZrezKt1IkQ&usqp=CAU",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQeoecV6BTnIKRawD5b-yL8Cp5fQAltKGeNSg&usqp=CAU"
        ],
        add_colors = [
            "000226",
            "0001ba",
            "00030c",
            "000371",
            "00000c",
            "0002eb"
        ],
        delete_colors =  [
            "000337",
            "0001cf"
        ]
        print(add_colors, delete_colors, add_images, delete_images)


# p = Person("Duc")
# objects = {
#     "p": p
# }
# s = "name"
# var = "p"
# print(objects[var].name)
# print(p[s])


a__ = Child("Duc")
print(a__.a())

