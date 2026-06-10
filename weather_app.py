import requests
import sys

# Ваш API ключ
API_KEY = "0ec6b3abe19eb54e57481fbe2a9d626a"

def get_weather(city):

    url = "https://api.openweathermap.org/data/2.5/weather"
    
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric",   # градусы Цельсия
        "lang": "ru"         # описание погоды на русском
    }
    
    try:
        # Выполняем GET-запрос с таймаутом 5 секунд
        response = requests.get(url, params=params, timeout=5)
        
        # Обработка: неверный ключ (401)
        if response.status_code == 401:
            print("Ошибка 401: Неверный API ключ. Проверьте ключ на сайте OpenWeatherMap.")
            return None
        
        # Обработка: город не найден (404)
        if response.status_code == 404:
            print(f"Ошибка 404: Город '{city}' не найден. Проверьте название (должно быть на английском).")
            return None
        
        # Если пришёл другой код ошибки (4xx, 5xx)
        if response.status_code != 200:
            print(f"Ошибка сервера: код {response.status_code}")
            return None
        
        # Парсим JSON-ответ
        data = response.json()
        
        # Формируем результат согласно заданию
        result = {
            "город": data["name"],
            "температура": round(data["main"]["temp"]),
            "описание": data["weather"][0]["description"].capitalize(),
            "влажность": data["main"]["humidity"],
            "ветер": round(data["wind"]["speed"])
        }
        
        return result
        
    except requests.exceptions.Timeout:
        print("Ошибка: Превышен таймаут (5 секунд) при запросе к API.")
        return None
    except requests.exceptions.ConnectionError:
        print("Ошибка: Нет подключения к интернету.")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети: {e}")
        return None
    except KeyError as e:
        print(f"Ошибка парсинга данных: отсутствует поле {e}")
        return None


def main():
    print(f"Используется API ключ: {API_KEY[:10]}...")
    
    # Получаем название города из аргументов командной строки или от пользователя
    if len(sys.argv) > 1:
        city = " ".join(sys.argv[1:])
    else:
        city = input("\nВведите название города (на английском): ").strip()
    
    if not city:
        print("Название города не может быть пустым.")
        return
    
    print(f"\n Запрашиваем погоду для города: {city}...")
    print(" Ожидание ответа от сервера (максимум 5 секунд)...\n")
    
    # Вызываем функцию get_weather
    weather = get_weather(city)
    
    # Выводим результат
    if weather:
        print(f" Город: {weather['город']}")
        print(f" Температура: {weather['температура']}°C")
        print(f" Описание: {weather['описание']}")
        print(f" Влажность: {weather['влажность']}%")
        print(f" Ветер: {weather['ветер']} м/с")
        print("\n Данные успешно получены!")
    else:
        print("\n Не удалось получить информацию о погоде.")
        print("\n Возможные причины:")
        print("   • Нет доступа к интернету")
        print("   • API OpenWeatherMap недоступен в вашем регионе")
        print("   • Неверное название города")
        print("   • Превышен таймаут (медленное соединение)")


if __name__ == "__main__":
    main()