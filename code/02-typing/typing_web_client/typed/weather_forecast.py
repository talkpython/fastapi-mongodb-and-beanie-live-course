class WeatherForecast:

    def __init__(self, data):
        self.temp = data['forecast']['temp']
        self.desc = data['weather']['description']
