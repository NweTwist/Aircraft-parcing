# ✈️ Парсер авиарейсов над Черным морем

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

Проект для мониторинга воздушного движения в зоне Черного моря с использованием AviationStack API.

## 🔍 Особенности

✔️ **Реальное время** - сбор актуальных данных о рейсах  
✔️ **Геофильтрация** - автоматический отбор рейсов в зоне Черного моря  
✔️ **Кеширование** - оптимизация запросов к API  
✔️ **Автоотчеты** - генерация статистики по авиакомпаниям и моделям ВС  
✔️ **Логирование** - детальная информация о процессе работы

## ⚙️ Установка

```bash
# 1. Клонируйте репозиторий
git clone https://github.com/yourusername/black-sea-flights.git
cd black-sea-flights

# 2. Установите зависимости
pip install -r requirements.txt

# 3. Настройте конфигурацию (отредактируйте main.py)
API_KEY = "ваш_ключ_от_aviationstack"
CACHE_TIME = 300
REGION_BOUNDS = {
    "min_lat": 40.0, "max_lat": 45.0,
    "min_lon": 27.0, "max_lon": 43.0
}'
```

# 🚀 Использование

```bash
# Основной сценарий (с кешированием)
python main.py

# Без использования кеша
python main.py --no-cache

# С лимитом записей (по умолчанию 100)
python main.py --limit 50

# Генерация отчетов
python reports.py          # По умолчанию hour+daily
python reports.py --hour   # Только часовой отчет
python reports.py --daily  # Только дневной отчет
```

# 📊 Формат данных

Файл flights.csv содержит:

```bash
callsign,icao,model,airline,latitude,longitude,altitude,speed,heading,departure,arrival,timestamp
```

Пример записи:
```bash
AZV542,ACA861,BCS1,Air Canada,44.12,30.25,37000,452,215,KBP,YYZ,2024-03-15 14:30:22
```

# ⚠️ Ограничения
```bash
print("API ограничения:")
print("- Максимум 100 рейсов/запрос")
print("- ~50% рейсов без координат")
print("- 100 запросов (бесплатно)")
```
