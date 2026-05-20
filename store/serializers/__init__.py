from rest_framework import serializers
from store.models import Category, Product, ProductImage, Review


class ProductImageSerializer(serializers.ModelSerializer):
    """Сериализатор изображений товара"""
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_main', 'created_at']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор категорий"""
    children_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description', 'image', 'parent', 'children_count', 'created_at']
    
    def get_children_count(self, obj):
        return obj.children.count()


class CategoryDetailSerializer(CategorySerializer):
    """Сериализатор категории с дочерними категориями и товарами"""
    children = CategorySerializer(many=True)
    products_count = serializers.SerializerMethodField()
    
    class Meta(CategorySerializer.Meta):
        fields = CategorySerializer.Meta.fields + ['children', 'products_count']
    
    def get_products_count(self, obj):
        return obj.products.filter(is_available=True).count()


class ProductListSerializer(serializers.ModelSerializer):
    """Сериализатор списка товаров"""
    category_name = serializers.CharField(source='category.name', read_only=True)
    category_slug = serializers.CharField(source='category.slug', read_only=True)
    image_url = serializers.SerializerMethodField()
    discount_percentage = serializers.ReadOnlyField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'old_price', 
            'category', 'category_name', 'category_slug',
            'image_url', 'stock', 'is_available', 'rating', 'reviews_count',
            'discount_percentage', 'created_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Сериализатор детальной информации о товаре"""
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    image_url = serializers.SerializerMethodField()
    discount_percentage = serializers.ReadOnlyField()
    reviews = serializers.SerializerMethodField()
    
    class Meta:
        model = Product
        fields = [
            'id', 'name', 'slug', 'description', 'price', 'old_price',
            'category', 'image_url', 'images', 'stock', 'is_available',
            'rating', 'reviews_count', 'discount_percentage',
            'reviews', 'created_at', 'updated_at'
        ]
    
    def get_image_url(self, obj):
        if obj.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None
    
    def get_reviews(self, obj):
        approved_reviews = obj.reviews.filter(is_approved=True)[:5]
        return ReviewSerializer(approved_reviews, many=True).data


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор отзывов"""
    user_name = serializers.CharField(source='user.full_name', read_only=True)
    
    class Meta:
        model = Review
        fields = ['id', 'user', 'user_name', 'rating', 'text', 'created_at', 'is_approved']
        read_only_fields = ['user', 'is_approved']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания отзыва"""
    class Meta:
        model = Review
        fields = ['rating', 'text']
