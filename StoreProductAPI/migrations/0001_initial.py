# Generated by Django 4.2.4 on 2023-08-14 05:51

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Color',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=10, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
                ('url', models.URLField()),
                ('filename', models.CharField(max_length=50, null=True)),
                ('size', models.PositiveIntegerField(null=True)),
                ('type', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=150)),
                ('stock', models.IntegerField()),
                ('price', models.DecimalField(decimal_places=2, max_digits=9)),
                ('shipping', models.BooleanField(default=False)),
                ('category', models.CharField(max_length=100)),
                ('reviews', models.SmallIntegerField()),
                ('stars', models.SmallIntegerField()),
                ('featured', models.BooleanField(default=False)),
                ('description', models.TextField(null=True)),
                ('company', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ThumbnailSize',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField()),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Thumbnail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full', models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, related_name='full_thumbnails', to='StoreProductAPI.thumbnailsize')),
                ('large', models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='large_thumbnails', to='StoreProductAPI.thumbnailsize')),
                ('small', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='small_thumbnails', to='StoreProductAPI.thumbnailsize')),
            ],
        ),
        migrations.CreateModel(
            name='ProductImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreProductAPI.image')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreProductAPI.product')),
            ],
        ),
        migrations.CreateModel(
            name='ProductColor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('color', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreProductAPI.color')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreProductAPI.product')),
            ],
        ),
        migrations.AddField(
            model_name='product',
            name='colors',
            field=models.ManyToManyField(through='StoreProductAPI.ProductColor', to='StoreProductAPI.color'),
        ),
        migrations.AddField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(through='StoreProductAPI.ProductImage', to='StoreProductAPI.image'),
        ),
        migrations.AddField(
            model_name='image',
            name='thumbnail',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='StoreProductAPI.thumbnail'),
        ),
    ]
