from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q, Avg, Count
from store.models import Category, Product, ProductImage, Review
from store.serializers import (
    CategorySerializer, CategoryDetailSerializer,
    ProductListSerializer, ProductDetailSerializer,
    ReviewSerializer, ReviewCreateSerializer
)


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет категорий"""
    queryset = Category.objects.all()
    lookup_field = 'slug'
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return CategoryDetailSerializer
        return CategorySerializer
    
    @action(detail=True, methods=['get'])
    def products(self, request, slug=None):
        """Получить товары категории"""
        category = self.get_object()
        products = category.products.filter(is_available=True)
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет товаров"""
    queryset = Product.objects.filter(is_available=True)
    lookup_field = 'slug'
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'description', 'category__name']
    ordering_fields = ['price', 'rating', 'created_at', 'name']
    
    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProductDetailSerializer
        return ProductListSerializer
    
    def get_queryset(self):
        queryset = Product.objects.filter(is_available=True)
        
        # Фильтрация по категории
        category_slug = self.request.query_params.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Фильтрация по цене
        min_price = self.request.query_params.get('min_price')
        max_price = self.request.query_params.get('max_price')
        if min_price:
            queryset = queryset.filter(price__gte=min_price)
        if max_price:
            queryset = queryset.filter(price__lte=max_price)
        
        # Фильтрация по наличию скидок
        if self.request.query_params.get('on_sale'):
            queryset = queryset.filter(old_price__isnull=False)
        
        return queryset.select_related('category').prefetch_related('images')
    
    @action(detail=True, methods=['post'])
    def add_review(self, request, slug=None):
        """Добавить отзыв к товару"""
        product = self.get_object()
        
        if not request.user.is_authenticated:
            return Response(
                {'detail': 'Необходимо авторизоваться для добавления отзыва'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        # Проверка, не оставлял ли пользователь уже отзыв
        if product.reviews.filter(user=request.user).exists():
            return Response(
                {'detail': 'Вы уже оставляли отзыв на этот товар'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ReviewCreateSerializer(data=request.data)
        if serializer.is_valid():
            review = serializer.save(product=product, user=request.user)
            return Response(ReviewSerializer(review).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Популярные товары"""
        products = self.get_queryset().filter(rating__gte=4.0)[:8]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def new(self, request):
        """Новинки"""
        products = self.get_queryset().order_by('-created_at')[:8]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def on_sale(self, request):
        """Товары со скидкой"""
        products = self.get_queryset().filter(old_price__isnull=False)[:8]
        serializer = ProductListSerializer(products, many=True, context={'request': request})
        return Response(serializer.data)


class ReviewViewSet(viewsets.ModelViewSet):
    """Вьюсет отзывов"""
    queryset = Review.objects.filter(is_approved=True)
    serializer_class = ReviewSerializer
    
    def get_permissions(self):
        from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAuthenticated()]
        return [IsAuthenticatedOrReadOnly()]
    
    def get_queryset(self):
        queryset = Review.objects.filter(is_approved=True)
        product_id = self.request.query_params.get('product')
        if product_id:
            queryset = queryset.filter(product_id=product_id)
        return queryset.select_related('user', 'product')
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user, is_approved=False)
