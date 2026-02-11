import requests, json, math

actions_rule = {
    "прогулка": {"temp": (-5,30), "rain": False, "wind_max": 8},
    "пикник": {"temp": (15,30), "rain": False, "wind_max": 5},
    "катание на лыжах": {"temp": (-20,5), "rain": None, "wind_max": 10},
    "пляж": {"temp": (22,40), "rain": False, "wind_max": 8},
}

def get_city(city):
    url = f'http://api.openweathermap.org/data/2.5/weather?q={city}&appid=04c9a2fe64449b0348eb38d5920909f2&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data["coord"]["lat"], data["coord"]["lon"]
    else:
        return None

def get_weather(lat, lon):
    url = f'http://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid=04c9a2fe64449b0348eb38d5920909f2&units=metric'
    response = requests.get(url)
    data = response.json()
    if response.status_code == 200:
        return data
    else:
        return None

def apply_weather(weather, rules):
    temp = weather["main"]["temp"]
    wind = weather["wind"]["speed"]
    rain = weather["weather"][0]["main"]
    temp_min, temp_max = rules["temp"]

    if temp < temp_min or temp > temp_max:
        return False
    if rules["rain"] == False and rain == "Rain":
        return False
    if wind > rules["wind_max"]:
        return False
    return True

def distance(lat1, lon1, lat2, lon2):
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

def main(current_city, action):
    global actions_rule
    lat, lon = get_city(current_city)
    weather = get_weather(lat, lon)
    if apply_weather(weather, actions_rule[action]):
        return True
    else:
        with open("data.json", "r") as f:
            cities = json.loads(f.read())
            best = None
            best_distance = math.inf
            best_country = None
            for city in cities:
                city_lat, city_lon = city["lat"], city["lon"]
                city_weather = get_weather(city_lat, city_lon)
                if apply_weather(city_weather, actions_rule[action]):
                    city_distance = distance(lat, lon, city_lat, city_lon)
                    if city_distance < best_distance:
                        best_distance = city_distance
                        best = city["city"]
                        best_country = city["country"]
            return best, best_country, best_distance

city = input("Введите город: ")
action = input("Напишите активность (прогулка, пикник, катание на лыжах, пляж): ")
answer = main(city, action)
print("Город подходит") if answer == True else [print(x, end=" ") for x in answer]
