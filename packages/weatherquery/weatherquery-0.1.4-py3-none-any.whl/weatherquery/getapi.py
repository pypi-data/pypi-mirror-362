# -*- coding: utf-8 -*-
from . import consts
import urllib.request
from .utils import *
from .name2code import name2code
import json
from functools import lru_cache


class GetApi:
    """
    api请求工具包
    """

    @lru_cache(maxsize=16)
    @staticmethod
    @get_time
    def get_api_by_citycode(city_code: str) -> dict:
        """
        根据城市编码请求城市天气信息字典
        """
        # url = f'https://www.weather.com.cn/data/sk/{city_code}.html'
        url = f"http://t.weather.itboy.net/api/weather/city/{city_code}"

        LOGGER.debug(f"Getting Api with citycode: {city_code}, url is {url}")

        # 构造请求头，防止 301/302
        req = urllib.request.Request(
            url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
        )

        # 发送请求，拿到原始字节
        with urllib.request.urlopen(req, timeout=10) as resp:
            raw = resp.read()  # bytes

        # 手动解码(经实验，此api编码为 utf-8)
        text = raw.decode("utf-8", errors="ignore")
        data = json.loads(text)

        return data

    @staticmethod
    @get_time
    def get_citycode_from_cityname(name: str) -> str:
        """
        根据城市名获取城市编码
        """

        possibable_cities = [
            i for i in name2code if GetApi._is_the_same_city(name, i["city_name"])
        ]
        if len(possibable_cities) == 0:
            raise ValueError(f"City {name} not found!")
        citycode = possibable_cities[0]["city_code"]
        if not citycode:
            # citycode可能为空
            raise ValueError(
                "抱歉，没有找到这个地区的城市编码，试试使用更精确的地址呢？（如果你给的城市名是省级行政区，请精确到某个市级行政区）"
            )

        return citycode


    @staticmethod
    @get_time
    def get_city_weather_dict(city_name: str) -> dict:
        code = GetApi.get_citycode_from_cityname(city_name)
        return GetApi.get_api_by_citycode(code)

    @lru_cache(maxsize=16)
    @staticmethod
    def _is_the_same_city(user_cityname: str, file_cityname: str, debug: bool = False):
        """
        比较两个城市是否为同一城市
        Args:
        user_cityname: 用户指定的城市
        file_cityname: 文件里存储的城市

        此函数为了确保 (芜湖市 芜湖) (安徽省 安徽) 之类的城市可以被识别成同一个
        """
        uc = user_cityname

        ignore_list = [
            "自治区",
            "直辖市",
            "特别行政区",  # 带有“区”，放在开头，以免被误判
            "省",
            "市",
            "区",
            "县",
            "村",
            "乡",
            "旗",
        ]
        for ig in ignore_list:
            if debug:
                print("!!!", ig, uc)

            # 去掉结尾的行政区级别
            if uc.endswith(ig):
                uc = uc[: (0 - len(ig))]

                if debug:
                    print("!!!", ig, uc)
                break

        return file_cityname.startswith(uc)


if __name__ == "__main__":
    print(GetApi.get_api_by_citycode("101010100"))
