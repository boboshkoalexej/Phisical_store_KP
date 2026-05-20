# Интернет-магазин физических товаров

Курсовая работа по разработке интернет-магазина с использованием архитектуры Backend-for-Frontend (BfF).

## 📋 Описание

Проект представляет собой полнофункциональный интернет-магазин физических товаров с:
- Каталогами и категориями товаров
- Корзиной покупок
- Системой заказов
- Пользовательскими аккаунтами
- Отзывами и рейтингами
- REST API для взаимодействия с фронтендом

## 🚀 Быстрый старт с Docker

### Предварительные требования

- Docker (версия 20.10+)
- Docker Compose (версия 2.0+)

### Установка и запуск

#### Вариант 1: Использование SQLite (рекомендуется для разработки)

```bash
# Клонирование репозитория
git clone <repository-url>
cd <project-directory>

# Запуск контейнеров (backend + frontend)
docker-compose up --build

# Или в фоновом режиме
docker-compose up -d --build
```

**Важно:** Главная страница теперь доступна непосредственно через Django backend на порту 8000.

После запуска:
- **Главная страница**: http://localhost:8000/ (красивый HTML интерфейс)
- **Frontend (Nginx)**: http://localhost (проксирует запросы к backend)
- **Backend API**: http://localhost:8000/api/
- **Django Admin**: http://localhost:8000/admin/

#### Вариант 2: Использование PostgreSQL

```bash
# Запуск с PostgreSQL вместо SQLite
docker-compose --profile postgres up --build
```

### Создание суперпользователя

```bash
# Выполнение команды в контейнере backend
docker-compose exec backend python manage.py createsuperuser
```

### Применение миграций

```bash
# Если миграции не применились автоматически
docker-compose exec backend python manage.py migrate
```

### Сбор статических файлов

```bash
docker-compose exec backend python manage.py collectstatic --noinput
```

### Пошаговая инструкция по подключению Docker

#### Шаг 1: Подготовка проекта

Убедитесь, что у вас установлена актуальная версия Docker и Docker Compose:

```bash
docker --version
docker-compose --version
```

#### Шаг 2: Проверка структуры проекта

Проект должен иметь следующую структуру:
```
.
├── config/              # Настройки Django проекта
│   ├── settings.py     # Основные настройки
│   ├── urls.py         # URL маршруты (включая home view)
│   └── ...
├── templates/          # HTML шаблоны Django
│   └── home.html       # Главная страница
├── store/              # Приложение товаров
├── accounts/           # Приложение пользователей
├── cart/               # Приложение корзины
├── orders/             # Приложение заказов
├── frontend/
│   ├── dist/          # Собранные статические файлы (опционально)
│   └── nginx.conf     # Конфигурация nginx
├── docker-compose.yml
└── README.md
```

**Примечание:** Главная страница (`home.html`) теперь рендерится непосредственно через Django и не требует отдельного frontend/dist для базовой работы.

#### Шаг 3: Настройка переменных окружения (опционально)

Создайте файл `.env` в корне проекта:

```env
DEBUG=1
SECRET_KEY=your-secret-key-here
DB_NAME=shopdb
DB_USER=shopuser
DB_PASS=shoppass123
```

#### Шаг 4: Запуск контейнеров

```bash
# Первый запуск с пересборкой
docker-compose up --build

# Последующие запуски
docker-compose up -d
```

#### Шаг 5: Проверка работы

Откройте браузер и перейдите по адресу:
- http://localhost - фронтенд
- http://localhost:8000/api/ - API бэкенда
- http://localhost:8000/admin/ - админ панель Django

#### Шаг 6: Управление контейнерами

```bash
# Просмотр логов
docker-compose logs -f

# Остановка
docker-compose down

# Перезапуск
docker-compose restart

# Удаление всех контейнеров и томов
docker-compose down -v
```

### Решение проблем

#### Ошибка: "failed to resolve source metadata"

Эта ошибка возникает при проблемах с сетью или DNS. Решения:

1. Проверьте подключение к интернету
2. Используйте зеркало Docker Hub:
```bash
# В docker-compose.yml замените образы на локальные зеркала
```

3. Очистите кэш Docker:
```bash
docker system prune -a
```

#### Ошибка: "directory not found"

Если у вас нет frontend/dist, это не критично - главная страница теперь рендерится через Django. Nginx будет проксировать запросы на backend.

При необходимости создать тестовую страницу:

```bash
mkdir -p frontend/dist
echo '<h1>Магазин работает!</h1>' > frontend/dist/index.html
```

Или закомментируйте volumes в секции frontend в docker-compose.yml:

```yaml
frontend:
  image: nginx:alpine
  # volumes:
  #   - ./frontend/dist:/usr/share/nginx/html:ro
  #   - ./frontend/nginx.conf:/etc/nginx/conf.d/default.conf:ro
```

#### Фронтенд не отображается

Проверьте, что:
1. Файл `frontend/dist/index.html` существует
2. Nginx конфигурация правильная
3. Порты не заняты другими приложениями

```bash
# Проверка занятых портов
lsof -i :80
lsof -i :8000

# Остановка других процессов
kill -9 <PID>
```

## 🛠 Локальная разработка (без Docker)

### Требования

- Python 3.10+
- Node.js 18+ (для фронтенда)
- PostgreSQL или SQLite

### Установка зависимостей

```bash
# Backend
pip install -r requirements.txt

# Frontend (в папке frontend/)
cd frontend
npm install
```

### Запуск сервера разработки

```bash
# Backend
python manage.py migrate
python manage.py runserver

# Frontend (в отдельном терминале)
cd frontend
npm run dev
```

## 📁 Структура проекта

```
.
├── config/                 # Настройки Django проекта
│   ├── settings.py        # Основные настройки
│   ├── urls.py            # URL маршруты
│   └── wsgi.py           # WSGI конфигурация
├── store/                 # Приложение товаров
│   ├── models.py         # Модели Category, Product, Review
│   ├── views.py          # ViewSet для API
│   └── serializers/      # Сериализаторы
├── accounts/             # Приложение пользователей
│   ├── models.py         # Модель User
│   ├── views.py          # Авторизация, регистрация
│   └── serializers/      # Сериализаторы
├── cart/                 # Приложение корзины
│   ├── models.py         # Модели Cart, CartItem
│   ├── views.py          # Операции с корзиной
│   └── serializers/      # Сериализаторы
├── orders/               # Приложение заказов
│   ├── models.py         # Модели Order, OrderItem, DeliveryAddress
│   ├── views.py          # Управление заказами
│   └── serializers/      # Сериализаторы
├── frontend/             # Фронтенд приложение
│   ├── Dockerfile        # Docker конфигурация
│   └── nginx.conf        # Nginx конфигурация
├── Dockerfile            # Backend Dockerfile
├── docker-compose.yml    # Docker Compose конфигурация
├── requirements.txt      # Python зависимости
└── README.md            # Документация
```

## 🔌 API Endpoints

### Авторизация и пользователи
- `POST /api/auth/register/` - Регистрация
- `POST /api/auth/login/` - Вход
- `POST /api/auth/logout/` - Выход
- `GET /api/users/me/` - Текущий пользователь
- `PUT /api/users/update_profile/` - Обновление профиля

### Товары
- `GET /api/products/` - Список товаров
- `GET /api/products/{slug}/` - Детали товара
- `GET /api/categories/` - Список категорий
- `GET /api/categories/{slug}/products/` - Товары категории
- `POST /api/products/{slug}/add_review/` - Добавить отзыв

### Корзина
- `GET /api/cart/my_cart/` - Получить корзину
- `POST /api/cart/add_item/` - Добавить товар
- `POST /api/cart/remove_item/` - Удалить товар
- `POST /api/cart/update_item/` - Обновить количество
- `POST /api/cart/clear/` - Очистить корзину

### Заказы
- `GET /api/orders/my_orders/` - Мои заказы
- `POST /api/orders/` - Создать заказ
- `GET /api/orders/{id}/` - Детали заказа
- `GET /api/addresses/` - Адреса доставки
- `POST /api/addresses/` - Добавить адрес

## 🔧 Конфигурация Docker

### Переменные окружения

| Переменная | Описание | Значение по умолчанию |
|------------|----------|----------------------|
| DEBUG | Режим отладки | 1 |
| DJANGO_SETTINGS_MODULE | Путь к настройкам | config.settings |
| SECRET_KEY | Секретный ключ | django-insecure-... |
| POSTGRES_DB | Имя БД | shopdb |
| POSTGRES_USER | Пользователь БД | shopuser |
| POSTGRES_PASSWORD | Пароль БД | shoppass123 |

### Docker команды

```bash
# Просмотр логов
docker-compose logs -f backend
docker-compose logs -f frontend

# Остановка контейнеров
docker-compose down

# Остановка с удалением томов
docker-compose down -v

# Пересборка контейнеров
docker-compose build --no-cache

# Выполнение команд в контейнере
docker-compose exec backend python manage.py shell
docker-compose exec backend python manage.py test

# Мониторинг ресурсов
docker stats
```

## 🧪 Тестирование

```bash
# Запуск тестов backend
docker-compose exec backend python manage.py test

# Запуск тестов с покрытием
docker-compose exec backend coverage run manage.py test
docker-compose exec backend coverage report
```

## 📊 Администрирование

Для доступа к Django Admin:

1. Создайте суперпользователя:
```bash
docker-compose exec backend python manage.py createsuperuser
```

2. Откройте http://localhost:8000/admin/

## 🔐 Безопасность

- Все пароли хешируются
- Используется токеновая аутентификация
- CORS настроен для взаимодействия с фронтендом
- CSRF защита включена

## 📝 Лицензия

Учебный проект для курсовой работы.

## 👥 Авторы

Студент [Ваше ФИО]
Группа [Ваша группа]
