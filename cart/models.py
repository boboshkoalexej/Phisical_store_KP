from django.db import models
from django.conf import settings


class Cart(models.Model):
    """Корзина пользователя"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='cart',
        blank=True, 
        null=True,
        verbose_name='пользователь'
    )
    session_key = models.CharField('ключ сессии', max_length=100, blank=True, null=True)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'корзина'
        verbose_name_plural = 'корзины'
    
    def __str__(self):
        return f"Корзина {self.user.email if self.user else self.session_key}"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())


class CartItem(models.Model):
    """Элемент корзины"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('store.Product', on_delete=models.CASCADE, related_name='cart_items')
    quantity = models.PositiveIntegerField('количество', default=1)
    created_at = models.DateTimeField('дата добавления', auto_now_add=True)
    updated_at = models.DateTimeField('дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'элемент корзины'
        verbose_name_plural = 'элементы корзины'
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.product.name} x {self.quantity}"
    
    @property
    def total_price(self):
        return self.product.price * self.quantity
