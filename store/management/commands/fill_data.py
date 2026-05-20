import os
import django
import random
from decimal import Decimal

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from store.models import Category, Product
from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Администратор',
            last_name='Магазина'
        )
        print("Суперпользователь admin/admin123 создан.")
    else:
        print("Суперпользователь уже существует.")

def create_categories():
    categories_data = [
        {"name": "Электроника", "slug": "electronics", "description": "Смартфоны, ноутбуки, планшеты и аксессуары"},
        {"name": "Одежда и обувь", "slug": "clothing", "description": "Мужская, женская и детская одежда"},
        {"name": "Дом и сад", "slug": "home-garden", "description": "Мебель, декор, инструменты и садовая техника"},
        {"name": "Книги", "slug": "books", "description": "Художественная литература, учебники, бизнес-книги"},
        {"name": "Спорт и отдых", "slug": "sports", "description": "Тренажеры, велосипеды, туристическое снаряжение"},
        {"name": "Красота и здоровье", "slug": "beauty", "description": "Косметика, витамины, товары для гигиены"},
        {"name": "Детские товары", "slug": "kids", "description": "Игрушки, одежда, питание и уход за детьми"},
    ]
    
    created_categories = {}
    for cat_data in categories_data:
        cat, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'description': cat_data['description']
            }
        )
        if created:
            print(f"Категория '{cat.name}' создана.")
        created_categories[cat.slug] = cat
    
    return created_categories

def create_products(categories):
    products_data = [
        # Электроника
        {"name": "Смартфон SuperPhone X12", "price": 79990, "category": "electronics", "description": "Флагманский смартфон с камерой 108 Мп и экраном 120 Гц.", "stock": 50, "image": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=500&h=500&fit=crop"},
        {"name": "Ноутбук ProWork 15", "price": 125000, "category": "electronics", "description": "Мощный ноутбук для работы и творчества. Процессор M2, 16 ГБ RAM.", "stock": 20, "image": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&h=500&fit=crop"},
        {"name": "Наушники SoundMax Pro", "price": 15990, "category": "electronics", "description": "Беспроводные наушники с активным шумоподавлением.", "stock": 100, "image": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop"},
        {"name": "Умные часы FitWatch 5", "price": 24990, "category": "electronics", "description": "Спортивные часы с мониторингом здоровья и GPS.", "stock": 75, "image": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop"},
        {"name": "Планшет TabUltra 11", "price": 45000, "category": "electronics", "description": "Планшет с большим экраном и поддержкой стилуса.", "stock": 30, "image": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&h=500&fit=crop"},
        {"name": "Камера PhotoPro 4K", "price": 89990, "category": "electronics", "description": "Профессиональная беззеркальная камера для видео и фото.", "stock": 15, "image": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500&h=500&fit=crop"},
        
        # Одежда
        {"name": "Футболка Basic Cotton", "price": 1200, "category": "clothing", "description": "Классическая хлопковая футболка унисекс.", "stock": 200, "image": "https://images.unsplash.com/photo-1521572163474-6864f9cf17ab?w=500&h=500&fit=crop"},
        {"name": "Джинсы Slim Fit", "price": 3500, "category": "clothing", "description": "Стильные джинсы классического кроя.", "stock": 150, "image": "https://images.unsplash.com/photo-1542272617-08f08630329e?w=500&h=500&fit=crop"},
        {"name": "Кроссовки RunFast Pro", "price": 8900, "category": "clothing", "description": "Легкие беговые кроссовки с амортизацией.", "stock": 80, "image": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=500&h=500&fit=crop"},
        {"name": "Куртка Winter Warm", "price": 12500, "category": "clothing", "description": "Теплая зимняя куртка с капюшоном.", "stock": 40, "image": "https://images.unsplash.com/photo-1551028919-ac66e624ec99?w=500&h=500&fit=crop"},
        {"name": "Рюкзак City Travel", "price": 4200, "category": "clothing", "description": "Вместительный городской рюкзак с отделением для ноутбука.", "stock": 90, "image": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=500&h=500&fit=crop"},
        {"name": "Шапка Wool Soft", "price": 900, "category": "clothing", "description": "Мягкая шерстяная шапка.", "stock": 120, "image": "https://images.unsplash.com/photo-1576871337632-b9aef4c17ab9?w=500&h=500&fit=crop"},

        # Дом и сад
        {"name": "Лампа настольная LED", "price": 2500, "category": "home-garden", "description": "Светодиодная лампа с регулировкой яркости.", "stock": 60, "image": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=500&h=500&fit=crop"},
        {"name": "Набор кастрюль Premium", "price": 8900, "category": "home-garden", "description": "Набор из 5 кастрюль с антипригарным покрытием.", "stock": 25, "image": "https://images.unsplash.com/photo-1584992236310-6eddd744f6d7?w=500&h=500&fit=crop"},
        {"name": "Плед плетеный Large", "price": 3200, "category": "home-garden", "description": "Уютный плед большого размера.", "stock": 45, "image": "https://images.unsplash.com/photo-1580480055273-228ff5388ef8?w=500&h=500&fit=crop"},
        {"name": "Ваза керамическая", "price": 1800, "category": "home-garden", "description": "Стильная ваза для цветов ручной работы.", "stock": 30, "image": "https://images.unsplash.com/photo-1581783342308-f792ca11df53?w=500&h=500&fit=crop"},
        {"name": "Инструменты садовые Set", "price": 4500, "category": "home-garden", "description": "Набор основных садовых инструментов.", "stock": 35, "image": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=500&h=500&fit=crop"},
        {"name": "Подушка ортопедическая", "price": 2900, "category": "home-garden", "description": "Подушка с эффектом памяти для здорового сна.", "stock": 55, "image": "https://images.unsplash.com/photo-1584100936595-c0654b55a2e6?w=500&h=500&fit=crop"},

        # Книги
        {"name": "Книга 'Мастер и Маргарита'", "price": 650, "category": "books", "description": "Классическое произведение М.А. Булгакова.", "stock": 100, "image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=500&h=500&fit=crop"},
        {"name": "Учебник по Python", "price": 1200, "category": "books", "description": "Полное руководство по программированию на Python.", "stock": 80, "image": "https://images.unsplash.com/photo-1515879218367-8466d910aaa4?w=500&h=500&fit=crop"},
        {"name": "Атлас мира", "price": 2500, "category": "books", "description": "Подробный иллюстрированный атлас.", "stock": 40, "image": "https://images.unsplash.com/photo-1524995997946-a1c2e315a42f?w=500&h=500&fit=crop"},
        {"name": "Бизнес-мышление", "price": 950, "category": "books", "description": "Книга о стратегиях успешного бизнеса.", "stock": 70, "image": "https://images.unsplash.com/photo-1554774853-719586f8c277?w=500&h=500&fit=crop"},
        {"name": "Сказки народов мира", "price": 800, "category": "books", "description": "Сборник лучших сказок со всего света.", "stock": 60, "image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?w=500&h=500&fit=crop"},
        {"name": "Энциклопедия космоса", "price": 3200, "category": "books", "description": "Иллюстрированная энциклопедия о вселенной.", "stock": 25, "image": "https://images.unsplash.com/photo-1514632537423-1e6c2e7e0aab?w=500&h=500&fit=crop"},

        # Спорт
        {"name": "Гантели разборные 20кг", "price": 4500, "category": "sports", "description": "Набор гантелей с регулируемым весом.", "stock": 30, "image": "https://images.unsplash.com/photo-1583454110551-21f2fa2afe61?w=500&h=500&fit=crop"},
        {"name": "Коврик для йоги", "price": 1800, "category": "sports", "description": "Не скользящий коврик для занятий йогой.", "stock": 90, "image": "https://images.unsplash.com/photo-1592432678016-e910b452f9a2?w=500&h=500&fit=crop"},
        {"name": "Велосипед горный", "price": 25000, "category": "sports", "description": "Надежный горный велосипед для трейла.", "stock": 15, "image": "https://images.unsplash.com/photo-1532298229144-0ec0c57e30eb?w=500&h=500&fit=crop"},
        {"name": "Мяч футбольный Pro", "price": 2200, "category": "sports", "description": "Профессиональный мяч для футбола.", "stock": 50, "image": "https://images.unsplash.com/photo-1614632537423-1e6c2e7e0aab?w=500&h=500&fit=crop"},
        {"name": "Теннисная ракетка", "price": 3800, "category": "sports", "description": "Легкая ракетка для большого тенниса.", "stock": 40, "image": "https://images.unsplash.com/photo-1530915512336-d948e1579c27?w=500&h=500&fit=crop"},
        {"name": "Рюкзак туристический 60л", "price": 7500, "category": "sports", "description": "Вместительный рюкзак для походов.", "stock": 25, "image": "https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=500&h=500&fit=crop"},

        # Красота
        {"name": "Крем увлажняющий FaceCare", "price": 1500, "category": "beauty", "description": "Увлажняющий крем для лица с SPF.", "stock": 80, "image": "https://images.unsplash.com/photo-1556228720-1987594a8a37?w=500&h=500&fit=crop"},
        {"name": "Шампунь Natural Hair", "price": 650, "category": "beauty", "description": "Натуральный шампунь без сульфатов.", "stock": 120, "image": "https://images.unsplash.com/photo-1535585209827-a15fcdbc4c2d?w=500&h=500&fit=crop"},
        {"name": "Набор кистей для макияжа", "price": 2100, "category": "beauty", "description": "Профессиональный набор из 12 кистей.", "stock": 45, "image": "https://images.unsplash.com/photo-1596462502278-c31d21fd1273?w=500&h=500&fit=crop"},
        {"name": "Парфюм Eau de Parfum", "price": 5500, "category": "beauty", "description": "Стойкий парфюм с цветочным ароматом.", "stock": 30, "image": "https://images.unsplash.com/photo-1541643600914-78b084683601?w=500&h=500&fit=crop"},
        {"name": "Витамины MultiVita", "price": 900, "category": "beauty", "description": "Комплекс витаминов для иммунитета.", "stock": 150, "image": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=500&h=500&fit=crop"},
        {"name": "Маска для лица глиняная", "price": 850, "category": "beauty", "description": "Очищающая маска с голубой глиной.", "stock": 70, "image": "https://images.unsplash.com/photo-1596755389378-c31d21fd1273?w=500&h=500&fit=crop"},

        # Дети
        {"name": "Конструктор Building Blocks", "price": 3200, "category": "kids", "description": "Большой набор конструктора (500 деталей).", "stock": 40, "image": "https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=500&h=500&fit=crop"},
        {"name": "Плюшевый мишка", "price": 1800, "category": "kids", "description": "Мягкая игрушка, гипоаллергенный материал.", "stock": 60, "image": "https://images.unsplash.com/photo-1559454403-b8fb88521f11?w=500&h=500&fit=crop"},
        {"name": "Кукла Fashion Girl", "price": 2400, "category": "kids", "description": "Кукла с набором одежды и аксессуаров.", "stock": 35, "image": "https://images.unsplash.com/photo-1558711768-bb2f991f0b9c?w=500&h=500&fit=crop"},
        {"name": "Машинка радиоуправляемая", "price": 4500, "category": "kids", "description": "Быстрая машинка с пультом ДУ.", "stock": 25, "image": "https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=500&h=500&fit=crop"},
        {"name": "Настольная игра 'Монополия'", "price": 2800, "category": "kids", "description": "Классическая экономическая игра для семьи.", "stock": 50, "image": "https://images.unsplash.com/photo-1610890716271-e745895d9525?w=500&h=500&fit=crop"},
        {"name": "Развивающий планшет KidsTab", "price": 3900, "category": "kids", "description": "Обучающий планшет для детей от 3 лет.", "stock": 30, "image": "https://images.unsplash.com/photo-1596462502278-c31d21fd1273?w=500&h=500&fit=crop"},
    ]

    count = 0
    for prod_data in products_data:
        cat_slug = prod_data.pop('category')
        category = categories.get(cat_slug)
        if category:
            product, created = Product.objects.get_or_create(
                name=prod_data['name'],
                defaults={
                    **prod_data,
                    'category': category,
                    'price': Decimal(str(prod_data['price']))
                }
            )
            if created:
                count += 1
                print(f"Товар '{product.name}' добавлен в категорию '{category.name}'.")
    
    print(f"\nВсего создано товаров: {count}")

if __name__ == '__main__':
    print("Начало наполнения базы данных...")
    create_superuser()
    categories = create_categories()
    create_products(categories)
    print("База данных успешно наполнена!")
