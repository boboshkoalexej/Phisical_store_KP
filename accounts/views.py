from rest_framework import viewsets, status, generics
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, authenticate
from accounts.serializers import UserSerializer, UserRegistrationSerializer, LoginSerializer
from orders.serializers import OrderListSerializer, DeliveryAddressSerializer
from cart.serializers import CartSerializer


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет пользователя"""
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.request.user.__class__.objects.filter(id=self.request.user.id)
    
    @action(detail=False, methods=['get'])
    def me(self, request):
        """Получить текущего пользователя"""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)
    
    @action(detail=False, methods=['put', 'patch'])
    def update_profile(self, request):
        """Обновить профиль пользователя"""
        user = request.user
        serializer = self.get_serializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Регистрация нового пользователя"""
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': UserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    """Вход пользователя"""
    serializer = LoginSerializer(data=request.data)
    if serializer.is_valid():
        user = authenticate(
            username=serializer.validated_data['username'],
            password=serializer.validated_data['password']
        )
        if user:
            login(request, user)
            token, _ = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key
            })
        return Response({'detail': 'Неверное имя пользователя или пароль'}, status=status.HTTP_400_BAD_REQUEST)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_view(request):
    """Выход пользователя"""
    try:
        request.user.auth_token.delete()
    except:
        pass
    logout(request)
    return Response({'detail': 'Вы успешно вышли из системы'})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def user_dashboard(request):
    """Дашборд пользователя"""
    from cart.models import Cart
    
    cart = Cart.objects.filter(user=request.user).first()
    cart_data = CartSerializer(cart, context={'request': request}).data if cart else None
    
    recent_orders = request.user.orders.order_by('-created_at')[:5]
    orders_data = OrderListSerializer(recent_orders, many=True).data
    
    addresses = request.user.addresses.all()
    addresses_data = DeliveryAddressSerializer(addresses, many=True).data
    
    return Response({
        'user': UserSerializer(request.user).data,
        'cart': cart_data,
        'recent_orders': orders_data,
        'addresses': addresses_data
    })
