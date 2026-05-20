from django.db import models
from django.conf import settings


class Order(models.Model):
    """Заказ"""
    STATUS_CHOICES = [
        ('pending', 'Ожидает подтверждения'),
        ('confirmed', 'Подтвержден'),
        ('processing', 'В обработке'),
        ('shipped', 'Отправлен'),
        ('delivered', 'Доставлен'),
        ('cancelled', 'Отменен'),
    ]
    
    PAYMENT_STATUS_CHOICES = [
        ('pending', 'Ожидает оплаты'),
        ('paid', 'Оплачен'),
        ('refunded', 'Возвращен'),
    ]
    
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='orders',
        verbose_name='пользователь'
    )
    order_number = models.CharField('номер заказа', max_length=50, unique=True)
    status = models.CharField('статус', max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField('статус оплаты', max_length=20, choices=PAYMENT_STATUS_CHOICES, default='pending')
    
    # Контактная информация
    first_name = models.CharField('имя', max_length=100)
    last_name = models.CharField('фамилия', max_length=100)
    email = models.EmailField('email')
    phone = models.CharField('телефон', max_length=20)
    
    # Адрес доставки
    address = models.TextField('адрес доставки')
    city = models.CharField('город', max_length=100)
    postal_code = models.CharField('почтовый индекс', max_length=20)
    
    # Стоимость
    subtotal = models.DecimalField('сумма товаров', max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField('стоимость доставки', max_digits=10, decimal_places=2, default=0)
    total = models.DecimalField('итоговая сумма', max_digits=10, decimal_places=2)
    
    comment = models.TextField('комментарий к заказу', blank=True)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'заказ'
        verbose_name_plural = 'заказы'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Заказ №{self.order_number} от {self.user.username}"
    
    def save(self, *args, **kwargs):
        if not self.order_number:
            from datetime import datetime
            self.order_number = f"ORD-{datetime.now().strftime('%Y%m%d%H%M%S')}-{self.pk or '000'}"
        super().save(*args, **kwargs)


class OrderItem(models.Model):
    """Элемент заказа"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('store.Product', on_delete=models.SET_NULL, null=True)
    product_name = models.CharField('название товара', max_length=300)
    quantity = models.PositiveIntegerField('количество', default=1)
    price = models.DecimalField('цена на момент покупки', max_digits=10, decimal_places=2)
    total = models.DecimalField('сумма', max_digits=10, decimal_places=2)
    
    class Meta:
        verbose_name = 'элемент заказа'
        verbose_name_plural = 'элементы заказов'
    
    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
    
    def save(self, *args, **kwargs):
        self.total = self.price * self.quantity
        super().save(*args, **kwargs)


class DeliveryAddress(models.Model):
    """Адрес доставки пользователя"""
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='addresses')
    title = models.CharField('название', max_length=50, default='Дом')
    first_name = models.CharField('имя', max_length=100)
    last_name = models.CharField('фамилия', max_length=100)
    phone = models.CharField('телефон', max_length=20)
    address = models.TextField('адрес')
    city = models.CharField('город', max_length=100)
    postal_code = models.CharField('почтовый индекс', max_length=20)
    is_default = models.BooleanField('адрес по умолчанию', default=False)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'адрес доставки'
        verbose_name_plural = 'адреса доставки'
        ordering = ['-is_default', '-created_at']
    
    def __str__(self):
        return f"{self.city}, {self.address} ({self.first_name} {self.last_name})"
