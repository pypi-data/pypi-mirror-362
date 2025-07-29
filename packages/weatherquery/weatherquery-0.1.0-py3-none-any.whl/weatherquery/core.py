from .getapi import GetApi
from dataclasses import dataclass


@dataclass
class CityInfo:
    """
    城市信息数据类

    属性：
    city (str): 城市名称
    city_key (str): 城市行政代码
    parent (str): 城市所属的上级行政区划
    update_ime (str): 上一次更新的时间
    """
    city: str
    city_key: str
    parent: str
    update_time: str


@dataclass
class DayWeather:
    """
    一日天气信息数据类

    属性：
    data (str): 日期
    high (str): 最高温度
    low (str): 最低温度
    ymd (str): 日期，采用YYYY-MM-DD格式
    week (str): 星期几
    sunrise (str): 日出时间
    sunset (str): 日落时间
    aqi (int): 空气指数
    wind_direction (str): 风向
    wind_force (str): 风力
    weather_type (str): 天气
    notice (str): 温馨提示
    """
    date: str
    high: str
    low: str
    ymd: str
    week: str
    sunrise: str
    sunset: str
    aqi: int
    wind_direction: str
    wind_force: str
    weather_type: str
    notice: str


@dataclass
class WeatherData:
    """
    天气数据类

    属性：
    humidity (str): 湿度，百分数字符串
    pm25 (int): PM2.5指数
    pm10 (int): PM10指数
    quality (str): 空气质量
    temperature (str): 温度
    cold_index (str): 感冒指数
    forecast (list[DayWeather]): 未来天气预测
    yesterday (DayWeather): 昨日天气
    """
    humidity: str
    pm25: int
    pm10: int
    quality: str
    temperature: str
    cold_index: str
    forecast: list[DayWeather]
    yesterday: DayWeather


@dataclass
class MainData:
    """
    主数据类，用于封装城市信息和天气数据。

    属性:
    cityInfo: CityInfo类型，存储城市信息。
    data: WeatherData类型，存储天气数据。
    """
    cityInfo: CityInfo
    data: WeatherData


class Querier:
    """
    天气查询类，用于查询指定城市的天气信息。
    """
    def __init__(self, city_name):
        self._data = GetApi.get_city_weather_dict(city_name=city_name)
        self._data_data = self._data["data"]
        self._main_data = MainData(cityInfo=self.city_info, data=self.weather_data)

    @property
    def city_info(self) -> CityInfo:
        api_city_info = self._data["cityInfo"]
        return CityInfo(
            city=api_city_info["city"],
            city_key=api_city_info["citykey"],
            parent=api_city_info["parent"],
            update_time=api_city_info["updateTime"]
        )



    @property
    def weather_data(self) -> WeatherData:
        return WeatherData(
            humidity=self._data_data["shidu"],
            pm25=int(self._data_data["pm25"]),
            pm10=int(self._data_data["pm10"]),
            quality=self._data_data["quality"],
            temperature=self._data_data["wendu"],
            cold_index=self._data_data["ganmao"],
            forecast=self.forecast,
            yesterday=self.yesterday,
        )

    @property
    def forecast(self) -> list[DayWeather]:
        return [
            DayWeather(
                date=day["date"],
                high=day["high"],
                low=day["low"],
                ymd=day["ymd"],
                week=day["week"],
                sunrise=day["sunrise"],
                sunset=day["sunset"],
                aqi=day["aqi"],
                wind_direction=day["fx"],  # 改为 "fx"
                wind_force=day["fl"],  # 这个是对的
                weather_type=day["type"],  # 这个是对的
                notice=day["notice"],
            )
            for day in self._data_data["forecast"]
        ]

    @property
    def today(self) -> DayWeather:
        return self.forecast[0]

    @property
    def yesterday(self):
        return DayWeather(
            date=self._data_data["yesterday"]["date"],
            high=self._data_data["yesterday"]["high"],
            low=self._data_data["yesterday"]["low"],
            ymd=self._data_data["yesterday"]["ymd"],
            week=self._data_data["yesterday"]["week"],
            sunrise=self._data_data["yesterday"]["sunrise"],
            sunset=self._data_data["yesterday"]["sunset"],
            aqi=self._data_data["yesterday"]["aqi"],
            wind_direction=self._data_data["yesterday"]["fx"],  # 改为 "fx"
            wind_force=self._data_data["yesterday"]["fl"],
            weather_type=self._data_data["yesterday"]["type"],
            notice=self._data_data["yesterday"]["notice"],
        )

    @property
    def main_data(self):
        return self._main_data
