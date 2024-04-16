
import openmeteo_requests
from datetime import datetime

class IncreaseSpeed:
    def __init__(self, current_speed: int, max_speed: int):
        self.current_speed = current_speed
        self.max_speed = max_speed

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_speed < self.max_speed:
            self.current_speed += 10
            return self.current_speed
        else:
            raise StopIteration

class DecreaseSpeed:
    def __init__(self, current_speed: int):
        self.current_speed = current_speed

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_speed > 0:
            self.current_speed -= 10
            return self.current_speed
        else:
            raise StopIteration("Reached lower speed limit")


class Car:
    cars_on_road = 0

    def __init__(self, max_speed: int, current_speed=0, state="On road"):
        self.max_speed = max_speed
        self.current_speed = current_speed
        self.increaser = None
        self.decreaser = None
        self.state = state
        if self.state == "On road":
            Car.cars_on_road += 1

    def accelerate(self, upper_border=None):
        if self.increaser is None:
            self.increaser = IncreaseSpeed(self.current_speed, self.max_speed)
        
        if upper_border is None:
            self.current_speed = next(self.increaser)
            print(f"current speed: {self.current_speed}")
        else:
            if upper_border <= self.max_speed:
                while self.current_speed != upper_border:
                    self.current_speed = next(self.increaser)
                    print("current speed has been increased to ", self.current_speed)
                print("current speed has reached the upper border")
            else:
                while self.current_speed != self.max_speed:
                    self.current_speed = next(self.increaser)
                    print("current speed has been increased to ", self.current_speed)
                print("current speed has reached the upper border")

        return f"current speed: {self.current_speed}"

    def brake(self, lower_border=None):
        if self.decreaser is None:
            self.decreaser = DecreaseSpeed(self.current_speed)
        
        if lower_border is None:
            print(f"current speed: {next(self.decreaser)}")
        else:
            if lower_border >= 0:
                while self.current_speed != lower_border:
                    self.current_speed = next(self.decreaser)
                    print("current speed has been decreased to ", self.current_speed)
                print("current speed has reached the lower border")
            else:
                while self.current_speed != 0:
                    self.current_speed = next(self.decreaser)
                    print("current speed has been decreased to ", self.current_speed)
                print("current speed has reached the lower border")
        
        return f"current speed: {self.current_speed}"



    def parking(self):
        if self.state == "On road":
            self.state = "In the parking"
            Car.cars_on_road -= 1
        if self.state == "In the parking":
            print("car is already in the parking")

    @classmethod
    def total_cars(cls):
        print("Total amount of cars on the road is", cls.cars_on_road)

    @staticmethod
    def show_weather():
      openmeteo = openmeteo_requests.Client()
      url = "https://api.open-meteo.com/v1/forecast"
      params = {
      "latitude": 59.9386, # for St.Petersburg
      "longitude": 30.3141, # for St.Petersburg
      "current": ["temperature_2m", "apparent_temperature", "rain", "wind_speed_10m"],
      "wind_speed_unit": "ms",
      "timezone": "Europe/Moscow"
      }

      response = openmeteo.weather_api(url, params=params)[0]

      # The order of variables needs to be the same as requested in params->current!
      current = response.Current()
      current_temperature_2m = current.Variables(0).Value()
      current_apparent_temperature = current.Variables(1).Value()
      current_rain = current.Variables(2).Value()
      current_wind_speed_10m = current.Variables(3).Value()

      date_current = datetime.fromtimestamp(current.Time() + response.UtcOffsetSeconds())
      timezone_current = response.TimezoneAbbreviation().decode()
      print(f"Current time: {date_current} {timezone_current}")
      print(f"Current temperature: {round(current_temperature_2m, 0)} C")
      print(f"Current apparent_temperature: {round(current_apparent_temperature, 0)} C")
      print(f"Current rain: {current_rain} mm")
      print(f"Current wind_speed: {round(current_wind_speed_10m, 1)} m/s")
