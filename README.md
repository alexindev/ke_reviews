## Описание проекта:

KE SERVICES - это набор инструментов для продавцов маркетплейса KazanExpress, которые хотят улучшить свой бизнес и эффективность.

### 1. Статистика продаж

Добавляйте магазины для отслеживания продаж

Просматривайте подробную статистику по продажам каждого товара в добавленных магазине за последние 7 дней

### 2. Генератор отзывов (в разработке)

Автоматический генератор отзывов для своих магазинов

Быстрая генерация готовых ответов для отзывов с использованием AI


## Подготовка:

#### 1. Обновить список пакетов:
```
sudo apt update
```

#### 2. Установить необходимые пакеты 
```
sudo apt-get install -y apt-transport-https ca-certificates curl git software-properties-common
```

#### 3. Добавить официальный ключ Docker GPG
```
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
```

#### 4. Добавить репозиторий Docker
```
sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

#### 5. Установка Docker
```
sudo apt-get update
sudo apt-get install -y docker-ce docker-compose
```

## Установка:

#### 1. Клонировать репозиторий
```
git clone https://github.com/alexindev/ke_services.git
```
#### 2. Перейти в рабочую директорию
```
cd ke_services
```

#### 3. Переменные окружения

Создать файл **.env**, заполнить данные по шаблону **.env.template**


## Запуск:

```
sudo docker compose up --build -d
```

## Стек технологий:

```
Python, Django, DRF, Redis, Celery, Playwright, JavaScript, HTML, Bototstrap, CSS, Docker
```
