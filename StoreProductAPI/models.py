from django.db import models
import uuid

class Color(models.Model):
    value = models.CharField(max_length=10)

    def __str__(self):
        return self.value

    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"'{key}' attribute not found")   

class ThumbnailSize(models.Model):
    url = models.URLField(max_length=900, null=True)
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)

class Thumbnail(models.Model):
    small = models.OneToOneField(ThumbnailSize, on_delete=models.CASCADE, related_name='small_thumbnails', default=1)
    large = models.OneToOneField(ThumbnailSize, on_delete=models.CASCADE, related_name='large_thumbnails', default=2)
    full = models.OneToOneField(ThumbnailSize, on_delete=models.CASCADE, related_name='full_thumbnails', default=3)

class Image(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    width = models.PositiveIntegerField(null=False)
    height = models.PositiveIntegerField(null=False)
    url = models.URLField(max_length=900, null=False)
    filename = models.CharField(max_length=50, null=True)
    size = models.PositiveIntegerField(null=True)
    type = models.CharField(max_length=50)
    thumbnail = models.OneToOneField(Thumbnail, on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.filename} + {self.width} + {self.height}'
    
    def save(self, *args, **kwargs):
        self.thumbnail.save()
        super().save(*args, **kwargs)
    
    def __getitem__(self, key):
        if hasattr(self, key):
            return getattr(self, key)
        else:
            raise KeyError(f"'{key}' attribute not found")

class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=150)
    stock = models.IntegerField(null=False)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    shipping = models.BooleanField(default=False)
    category = models.CharField(max_length=100)
    colors = models.ManyToManyField(Color, through='ProductColor')
    images = models.ManyToManyField(Image, through='ProductImage')
    reviews = models.SmallIntegerField(default=0)
    stars = models.SmallIntegerField(default=0)
    featured = models.BooleanField(default=False)
    description = models.TextField(null=True)
    company = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class ProductColor(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} - {self.color.value}'
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image = models.ForeignKey(Image, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.product.name} - {self.image.filename}'
    


    