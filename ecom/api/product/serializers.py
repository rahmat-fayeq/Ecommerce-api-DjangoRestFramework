from rest_framework import serializers
from .models import Product

class ProductSerializers(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','description','image','price','stock','is_active','category')