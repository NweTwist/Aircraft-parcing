import pandas as pd
from datetime import datetime, timedelta
import os

# Настройки
INPUT_CSV = "flights.csv"
REPORTS_DIR = "reports"

def generate_reports():
    # Создаем папку для отчетов
    os.makedirs(REPORTS_DIR, exist_ok=True)
    
    # Читаем данные
    if not os.path.exists(INPUT_CSV):
        print(f"Файл {INPUT_CSV} не найден")
        return
    
    try:
        df = pd.read_csv(INPUT_CSV)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Отчет за последний час
        hourly_report = df[df['timestamp'] >= datetime.now() - timedelta(hours=1)]
        generate_report(hourly_report, "hourly")
        
        # Отчет за последние 24 часа
        daily_report = df[df['timestamp'] >= datetime.now() - timedelta(days=1)]
        generate_report(daily_report, "daily")
        
        print("Отчеты успешно созданы")
    except Exception as e:
        print(f"Ошибка: {e}")

def generate_report(data, period):
    if data.empty:
        print(f"Нет данных за {period} период")
        return
    
    # Отчет по моделям
    models = data.groupby('model').size().reset_index(name='count')
    models.to_csv(f"{REPORTS_DIR}/models_{period}.csv", index=False)
    
    # Отчет по авиакомпаниям
    airlines = data.groupby('airline').size().reset_index(name='count')
    airlines.to_csv(f"{REPORTS_DIR}/airlines_{period}.csv", index=False)

if __name__ == "__main__":
    generate_reports()