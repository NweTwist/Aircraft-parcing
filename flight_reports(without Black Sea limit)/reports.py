import pandas as pd
from datetime import datetime, timedelta
import os
import sys

# Настройки с абсолютными путями
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INPUT_CSV = os.path.join(BASE_DIR, "flights.csv")
REPORTS_DIR = os.path.join(BASE_DIR, "reports")

def generate_reports():
    try:
        os.makedirs(REPORTS_DIR, exist_ok=True)
        
        if not os.path.exists(INPUT_CSV):
            raise FileNotFoundError(f"Файл {INPUT_CSV} не найден. Разместите его в папке {BASE_DIR}")
        
        df = pd.read_csv(INPUT_CSV)
        
        # Проверка наличия колонки timestamp
        if 'timestamp' not in df.columns:
            raise ValueError("В файле отсутствует колонка 'timestamp'")
            
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Генерация отчетов
        generate_report(df[df['timestamp'] >= datetime.now() - timedelta(hours=1)], "hourly")
        generate_report(df[df['timestamp'] >= datetime.now() - timedelta(days=1)], "daily")
        
        print(f"Отчеты успешно созданы в папке {REPORTS_DIR}")
        
    except Exception as e:
        print(f"Ошибка: {e}", file=sys.stderr)
        sys.exit(1)

def generate_report(data, period):
    if data.empty:
        print(f"Нет данных за {period} период")
        return
    
    try:
        # Отчет по моделям самолетов
        models = data.groupby('model').size().reset_index(name='count')
        models.to_csv(os.path.join(REPORTS_DIR, f"models_{period}.csv"), index=False)
        
        # Отчет по авиакомпаниям
        airlines = data.groupby('airline').size().reset_index(name='count')
        airlines.to_csv(os.path.join(REPORTS_DIR, f"airlines_{period}.csv"), index=False)
        
    except Exception as e:
        print(f"Ошибка при создании отчета {period}: {e}", file=sys.stderr)

if __name__ == "__main__":
    generate_reports()
    input("Нажмите Enter для выхода...")  # Чтобы окно не закрывалось