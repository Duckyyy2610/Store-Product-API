from StoreProductAPI.models import *
from scripts.load import create_thumbnail
from StoreProductAPI.models import Color, ThumbnailSize, Thumbnail, Image, Product, ProductColor, ProductImage
from StoreProductAPI.serializers import ColorSerializer, SingleImageSerializer, ImageSerializer, ThumbnailSizeSerializer, ThumbnailSerializer, SingleProductSerializer, ProductSerializer

i = Image.objects.filter(url="https://pic-bstarstatic.akamaized.net/ugc/461972f0effcf587313ccd4b8de8fea6.jpeg").first()
i = Image.objects.get(id="61585626-96a3-49fa-9d34-4fb244ab6766") 
i.thumbnail
# <Thumbnail: Thumbnail object (653)>
i.thumbnail.small
# <ThumbnailSize: ThumbnailSize object (1038)>
i.thumbnail.small.width
# 58
i.thumbnail.small.height
# 34
type(create_thumbnail("https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg")) 
# <class 'StoreProductAPI.models.Thumbnail'>
type(i.thumbnail)
# <class 'StoreProductAPI.models.Thumbnail'>
t = create_thumbnail("https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg")
t.small.url 
# 'https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg'
tserializer = ThumbnailSerializer(t)
tserializer.data

i.thumbnail.delete()
i.thumbnail = create_thumbnail("https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg")
type(ThumbnailSerializer(i.thumbnail).data)

# {'small': OrderedDict([('url', 'https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg'), ('width', 60), ('height', 39)]), 
# 'large': OrderedDict([('url', 'https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg'), ('width', 700), ('height', 852)]), '
# full': OrderedDict([('url', 'https://img-cdn.2game.vn/2022/07/18/MinionsSuTroiDayCuaGru-1.jpg'), ('width', 3000), ('height', 3000)])}


