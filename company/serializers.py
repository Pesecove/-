from rest_framework import serializers
from django.contrib.auth.hashers import make_password
from .models import CustomUser, Product, Warehouse, WarehouseStock

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'username', 'role']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

class WarehouseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Warehouse
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class SupplyProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

class ConsumeProductSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)

    def validate(self, data):
        warehouse_id = self.context['view'].kwargs.get('pk')
        try:
            stock = WarehouseStock.objects.get(warehouse_id=warehouse_id, product_id=data['product_id'])
            if stock.quantity < data['quantity']:
                raise serializers.ValidationError("Потребитель не может получить товара больше, чем имеется на складе!")
        except WarehouseStock.DoesNotExist:
            raise serializers.ValidationError("Данного товара нет на этом складе.")
        return data