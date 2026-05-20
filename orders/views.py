from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.db import transaction
from orders.models import Order, OrderItem, DeliveryAddress
from orders.serializers import (
    OrderListSerializer, OrderDetailSerializer, OrderCreateSerializer,
    DeliveryAddressSerializer, DeliveryAddressCreateSerializer
)
from cart.models import Cart


class OrderViewSet(viewsets.ModelViewSet):
    """Вьюсет заказов"""
    serializer_class = OrderDetailSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        elif self.action == 'create':
            return OrderCreateSerializer
        return OrderDetailSerializer
    
    @action(detail=False, methods=['get'])
    def my_orders(self, request):
        """Получить заказы текущего пользователя"""
        orders = self.get_queryset().order_by('-created_at')
        serializer = OrderListSerializer(orders, many=True)
        return Response(serializer.data)
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        """Создать заказ из корзины"""
        cart = Cart.objects.filter(user=request.user).first()
        
        if not cart or not cart.items.exists():
            return Response({'detail': 'Корзина пуста'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Создаем заказ
        order_data = request.data.copy()
        order_data['user'] = request.user.id
        
        subtotal = sum(item.total_price for item in cart.items.all())
        shipping_cost = 500 if subtotal < 5000 else 0  # Бесплатная доставка от 5000
        total = subtotal + shipping_cost
        
        order_data['subtotal'] = subtotal
        order_data['shipping_cost'] = shipping_cost
        order_data['total'] = total
        
        serializer = self.get_serializer(data=order_data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(user=request.user)
        
        # Создаем элементы заказа
        for cart_item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=cart_item.product,
                product_name=cart_item.product.name,
                quantity=cart_item.quantity,
                price=cart_item.product.price,
                total=cart_item.total_price
            )
            
            # Уменьшаем остаток на складе
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        # Очищаем корзину
        cart.items.all().delete()
        
        return Response(OrderDetailSerializer(order).data, status=status.HTTP_201_CREATED)


class DeliveryAddressViewSet(viewsets.ModelViewSet):
    """Вьюсет адресов доставки"""
    serializer_class = DeliveryAddressSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return DeliveryAddress.objects.filter(user=self.request.user)
    
    def get_serializer_class(self):
        if self.action == 'create':
            return DeliveryAddressCreateSerializer
        return DeliveryAddressSerializer
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def default(self, request):
        """Получить адрес по умолчанию"""
        address = DeliveryAddress.objects.filter(user=request.user, is_default=True).first()
        if address:
            serializer = self.get_serializer(address)
            return Response(serializer.data)
        return Response(None)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def order_detail(request, pk):
    """Детальная информация о заказе"""
    try:
        order = Order.objects.get(pk=pk, user=request.user)
        serializer = OrderDetailSerializer(order)
        return Response(serializer.data)
    except Order.DoesNotExist:
        return Response({'detail': 'Заказ не найден'}, status=status.HTTP_404_NOT_FOUND)
