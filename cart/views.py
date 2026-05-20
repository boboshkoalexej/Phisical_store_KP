from rest_framework import viewsets, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cart.models import Cart, CartItem
from cart.serializers import CartSerializer, CartItemSerializer, CartItemCreateSerializer


class CartViewSet(viewsets.ModelViewSet):
    """Вьюсет корзины"""
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    
    @action(detail=False, methods=['get'])
    def my_cart(self, request):
        """Получить корзину текущего пользователя"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        serializer = self.get_serializer(cart, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def add_item(self, request):
        """Добавить товар в корзину"""
        cart, created = Cart.objects.get_or_create(user=request.user)
        
        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)
        
        if not product_id:
            return Response({'detail': 'Необходимо указать товар'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Проверяем是否存在товар в корзине
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product_id=product_id,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += int(quantity)
            cart_item.save()
        
        serializer = self.get_serializer(cart, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def remove_item(self, request):
        """Удалить товар из корзины"""
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'detail': 'Корзина не найдена'}, status=status.HTTP_404_NOT_FOUND)
        
        product_id = request.data.get('product')
        if product_id:
            CartItem.objects.filter(cart=cart, product_id=product_id).delete()
        
        serializer = self.get_serializer(cart, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def update_item(self, request):
        """Обновить количество товара в корзине"""
        cart = Cart.objects.filter(user=request.user).first()
        if not cart:
            return Response({'detail': 'Корзина не найдена'}, status=status.HTTP_404_NOT_FOUND)
        
        product_id = request.data.get('product')
        quantity = request.data.get('quantity')
        
        if product_id and quantity:
            cart_item = CartItem.objects.filter(cart=cart, product_id=product_id).first()
            if cart_item:
                cart_item.quantity = int(quantity)
                cart_item.save()
        
        serializer = self.get_serializer(cart, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['post'])
    def clear(self, request):
        """Очистить корзину"""
        cart = Cart.objects.filter(user=request.user).first()
        if cart:
            cart.items.all().delete()
        return Response({'detail': 'Корзина очищена'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def cart_detail(request):
    """Детальная информация о корзине"""
    cart, created = Cart.objects.get_or_create(user=request.user)
    serializer = CartSerializer(cart, context={'request': request})
    return Response(serializer.data)
