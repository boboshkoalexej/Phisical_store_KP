from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """Категория товаров"""
    name = models.CharField('название', max_length=200)
    slug = models.SlugField('slug', unique=True, blank=True)
    description = models.TextField('описание', blank=True)
    image = models.ImageField('изображение', upload_to='categories/', blank=True, null=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        related_name='children',
        blank=True, 
        null=True,
        verbose_name='родительская категория'
    )
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'
        ordering = ['name']
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name


class Product(models.Model):
    """Товар"""
    name = models.CharField('название', max_length=300)
    slug = models.SlugField('slug', unique=True, blank=True)
    description = models.TextField('описание', blank=True)
    price = models.DecimalField('цена', max_digits=10, decimal_places=2)
    old_price = models.DecimalField('старая цена', max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(
        Category, 
        on_delete=models.CASCADE, 
        related_name='products',
        verbose_name='категория'
    )
    image = models.ImageField('изображение', upload_to='products/', blank=True, null=True)
    images = models.ManyToManyField('ProductImage', related_name='products', blank=True, verbose_name='дополнительные изображения')
    stock = models.PositiveIntegerField('остаток на складе', default=0)
    is_available = models.BooleanField('доступен', default=True)
    rating = models.DecimalField('рейтинг', max_digits=3, decimal_places=2, default=0)
    reviews_count = models.PositiveIntegerField('количество отзывов', default=0)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    updated_at = models.DateTimeField('дата обновления', auto_now=True)
    
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['price']),
            models.Index(fields=['rating']),
        ]
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    @property
    def discount_percentage(self):
        if self.old_price and self.old_price > self.price:
            return int(((self.old_price - self.price) / self.old_price) * 100)
        return 0


class ProductImage(models.Model):
    """Изображение товара"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_images')
    image = models.ImageField('изображение', upload_to='products/')
    is_main = models.BooleanField('основное', default=False)
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    
    class Meta:
        verbose_name = 'изображение товара'
        verbose_name_plural = 'изображения товаров'
        ordering = ['-is_main', '-created_at']
    
    def __str__(self):
        return f"Изображение для {self.product.name}"


class Review(models.Model):
    """Отзыв о товаре"""
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField('рейтинг', choices=[(i, i) for i in range(1, 6)])
    text = models.TextField('текст отзыва')
    created_at = models.DateTimeField('дата создания', auto_now_add=True)
    is_approved = models.BooleanField('одобрен', default=False)
    
    class Meta:
        verbose_name = 'отзыв'
        verbose_name_plural = 'отзывы'
        ordering = ['-created_at']
        unique_together = ['product', 'user']
    
    def __str__(self):
        return f"Отзыв от {self.user.username} на {self.product.name}"
