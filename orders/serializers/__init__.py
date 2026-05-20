from rest_framework import serializers
from orders.models import Order, OrderItem, DeliveryAddress


class OrderItemSerializer(serializers.ModelSerializer):
    """Сериализатор элемента заказа"""
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total']


class OrderListSerializer(serializers.ModelSerializer):
    """Сериализатор списка заказов"""
    items_count = serializers.SerializerMethodField()
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'status_display', 
            'payment_status', 'payment_status_display',
            'total', 'items_count', 'created_at'
        ]
    
    def get_items_count(self, obj):
        return obj.items.count()


class OrderDetailSerializer(serializers.ModelSerializer):
    """Сериализатор детальной информации о заказе"""
    items = OrderItemSerializer(many=True, read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)
    payment_status_display = serializers.CharField(source='get_payment_status_display', read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'order_number', 'status', 'status_display',
            'payment_status', 'payment_status_display',
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'postal_code',
            'subtotal', 'shipping_cost', 'total',
            'comment', 'items', 'created_at', 'updated_at'
        ]


class OrderCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания заказа"""
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'email', 'phone',
            'address', 'city', 'postal_code',
            'comment'
        ]


class DeliveryAddressSerializer(serializers.ModelSerializer):
    """Сериализатор адреса доставки"""
    full_name = serializers.SerializerMethodField()
    
    class Meta:
        model = DeliveryAddress
        fields = [
            'id', 'title', 'first_name', 'last_name', 'full_name',
            'phone', 'address', 'city', 'postal_code', 'is_default', 'created_at'
        ]
        read_only_fields = ['created_at']
    
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"


class DeliveryAddressCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания адреса доставки"""
    class Meta:
        model = DeliveryAddress
        fields = [
            'title', 'first_name', 'last_name', 'phone',
            'address', 'city', 'postal_code', 'is_default'
        ]
