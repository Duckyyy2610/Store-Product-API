class Person:
    def __init__(self, name):
        self.name = name
    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"'{key}' attribute not found")

p = Person("Duc")

objects = {
    "p": p
}
s = "name"
var = "p"
print(objects[var].name)
print(p[s])

