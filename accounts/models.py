from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Пользователь интернет-магазина"""
    email = models.EmailField('email', unique=True)
    phone = models.CharField('телефон', max_length=20, blank=True)
    created_at = models.DateTimeField('дата регистрации', auto_now_add=True)
    
    class Meta:
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.email or self.username
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username
