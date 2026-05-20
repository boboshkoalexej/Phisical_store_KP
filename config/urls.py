"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token

from store.views import CategoryViewSet, ProductViewSet, ReviewViewSet
from accounts.views import UserViewSet, register, login_view, logout_view, user_dashboard
from cart.views import CartViewSet, cart_detail
from orders.views import OrderViewSet, DeliveryAddressViewSet, order_detail

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'reviews', ReviewViewSet, basename='review')
router.register(r'users', UserViewSet, basename='user')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'addresses', DeliveryAddressViewSet, basename='address')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include([
        # Auth endpoints
        path('auth/register/', register, name='register'),
        path('auth/login/', login_view, name='login'),
        path('auth/logout/', logout_view, name='logout'),
        path('auth/token/', obtain_auth_token, name='obtain-token'),
        path('dashboard/', user_dashboard, name='dashboard'),
        
        # API router
        path('', include(router.urls)),
        
        # Additional endpoints
        path('cart/detail/', cart_detail, name='cart-detail'),
        path('orders/<int:pk>/', order_detail, name='order-detail'),
    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
