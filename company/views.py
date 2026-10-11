from rest_framework import viewsets, generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .models import CustomUser, Product, Warehouse, WarehouseStock
from .permissions import IsSupplier, IsConsumer
from .serializers import (
    RegisterSerializer, WarehouseSerializer, ProductSerializer,
    SupplyProductSerializer, ConsumeProductSerializer
)

class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

class WarehouseViewSet(viewsets.ModelViewSet):
    queryset = Warehouse.objects.all()
    serializer_class = WarehouseSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=True, methods=['post'], permission_classes=[IsSupplier])
    def supply(self, request, pk=None):
        warehouse = self.get_object()
        serializer = SupplyProductSerializer(data=request.data)
        if serializer.is_valid():
            stock, _ = WarehouseStock.objects.get_or_create(
                warehouse=warehouse, product_id=serializer.validated_data['product_id']
            )
            stock.quantity += serializer.validated_data['quantity']
            stock.save()
            return Response({'status': 'Товар успешно поставлен на склад'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=['post'], permission_classes=[IsConsumer])
    def consume(self, request, pk=None):
        warehouse = self.get_object()
        serializer = ConsumeProductSerializer(data=request.data, context={'view': self})
        if serializer.is_valid():
            stock = WarehouseStock.objects.get(
                warehouse=warehouse, product_id=serializer.validated_data['product_id']
            )
            stock.quantity -= serializer.validated_data['quantity']
            stock.save()
            return Response({'status': 'Товар успешно получен со склада'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]