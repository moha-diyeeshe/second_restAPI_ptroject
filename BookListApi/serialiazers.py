from decimal import Decimal
from rest_framework import serializers
from .models import MenuItem,Category



class CategorySerialiazers(serializers.Serializer):
    class Mets:
        model = Category
        fields = [ 'id','slug','title']

class MenuItemSerialiazers(serializers.ModelSerializer):
    stock = serializers.IntegerField(source = 'inventory')
    price_after_tags = serializers.SerializerMethodField(method_name='calculate_tax',)
    category = serializers.StringRelatedField(read_only = True)
    category_id = serializers.IntegerField(write_only =True)

    class Meta:
        model = MenuItem
        fields = ['id','title','price','stock','price_after_tags','category','category_id']



    def calculate_tax(self,a:MenuItem):
        return a.price*Decimal(1.1)
