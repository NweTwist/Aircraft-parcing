import requests
import pandas as pd
from datetime import datetime, timedelta
import os
import time
import json

# Конфигурация
API_KEY = "6f553cf6fd01a0c3053449c40b2834cb"
BASE_URL = "http://api.aviationstack.com/v1"
CACHE_FILE = "flights_cache.json"
MIN_REQUEST_INTERVAL = 300

def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Ошибка загрузки кеша: {e}")
            return None
    return None

def save_cache(data):
    try:
        with open(CACHE_FILE, 'w') as f:
            json.dump({
                "last_update": datetime.now().isoformat(),
                "data": data
            }, f)
    except Exception as e:
        print(f"Ошибка сохранения кеша: {e}")

def fetch_live_flights():
    cache = load_cache()
    
    if cache and (datetime.now() - datetime.fromisoformat(cache["last_update"])) < timedelta(seconds=MIN_REQUEST_INTERVAL):
        print(f"Используем кешированные данные ({len(cache['data'])} рейсов)")
        return cache["data"]
    
    params = {
        "access_key": API_KEY,
        "flight_status": "active",
        "limit": 100
    }
    
    try:
        print("Запрос к AviationStack API...")
        response = requests.get(f"{BASE_URL}/flights", params=params, timeout=15)
        print(f"URL запроса: {response.url}")
        print(f"Код статуса: {response.status_code}")
        
        response.raise_for_status()
        data = response.json()
        
        if 'data' not in data:
            print("Ошибка: в ответе отсутствует ключ 'data'")
            print("Пример ответа:", {k: data[k] for k in list(data.keys())[:2]})
            return cache["data"] if cache else []
        
        print(f"Получено {len(data['data'])} рейсов от API")
        save_cache(data['data'])
        return data['data']
        
    except Exception as e:
        print(f"Ошибка при запросе: {e}")
        return cache["data"] if cache else []

def process_flights(flights_data):
    if not flights_data or not isinstance(flights_data, list):
        print("Нет данных для обработки или неверный формат")
        return []
    
    processed = []
    flights_with_coords = 0
    
    for flight in flights_data:
        # Пропускаем None и не-словари
        if not isinstance(flight, dict):
            continue
            
        try:
            # Безопасное извлечение данных
            flight_info = {
                "callsign": str(flight.get("flight", {}).get("iata", "") or 
                           flight.get("flight", {}).get("icao", "UNKNOWN")),
                "icao": str(flight.get("flight", {}).get("icao", "UNKNOWN")),
                "model": str(flight.get("aircraft", {}).get("icao24", "UNKNOWN")),
                "airline": str(flight.get("airline", {}).get("name", "UNKNOWN")),
                "departure": str(flight.get("departure", {}).get("airport", "UNKNOWN")),
                "arrival": str(flight.get("arrival", {}).get("airport", "UNKNOWN")),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Обработка координат
            if isinstance(flight.get("live"), dict):
                live = flight["live"]
                if "latitude" in live and "longitude" in live:
                    flight_info.update({
                        "latitude": live["latitude"],
                        "longitude": live["longitude"],
                        "altitude": live.get("altitude"),
                        "speed": live.get("speed"),
                        "heading": live.get("direction")
                    })
                    flights_with_coords += 1
            
            processed.append(flight_info)
            
        except Exception:
            continue
    
    print(f"\nСтатистика обработки:")
    print(f"Всего получено: {len(flights_data)}")
    print(f"Успешно обработано: {len(processed)}")
    print(f"Рейсов с координатами: {flights_with_coords}")
    print(f"Пропущено некорректных записей: {len(flights_data) - len(processed)}")
    
    return processed

def save_to_csv(data, filename="flights.csv"):
    if not data:
        print("Нет данных для сохранения")
        return
    
    try:
        df = pd.DataFrame(data)
        header = not os.path.exists(filename) or os.path.getsize(filename) == 0
        df.to_csv(filename, mode='a', index=False, header=header)
        print(f"Сохранено {len(data)} записей в {filename}")
    except Exception as e:
        print(f"Ошибка сохранения CSV: {e}")

if __name__ == "__main__":
    print("=== Запуск сбора данных ===")
    start_time = time.time()
    
    flights_data = fetch_live_flights()
    
    if flights_data:
        print(f"Всего получено рейсов: {len(flights_data)}")
        processed_flights = process_flights(flights_data)
        save_to_csv(processed_flights)
    else:
        print("Не удалось получить данные о рейсах")
    
    elapsed = time.time() - start_time
    print(f"=== Завершено за {elapsed:.2f} сек ===")
    
    if elapsed < MIN_REQUEST_INTERVAL:
        wait_time = MIN_REQUEST_INTERVAL - elapsed
        print(f"Ждем {wait_time/60:.1f} мин до следующего запроса...")
        time.sleep(wait_time)