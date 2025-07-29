import unittest

__import__("sys").path.append("../src")

import weatherquery as wq
from weatherquery import Querier as Q

import os
import time

if "tests" in os.getcwd():
    wq.LOGGER.log("检测到正在tests目录中")
    os.chdir("..")


class TestAdd(unittest.TestCase):
    def test_get(self):
        cities = ["北京市", "上海", "香港特别行政区", "海淀区", "肥东县", "呼和浩特"]
        non_exist_cities = [
            "未知城市",
            "不存在的城市",
            "这会直接报错",
            "会有 ValueError",
        ]

        for city in cities:
            with self.subTest(city=city):
                q = Q(city)
                self.assertIsNotNone(today := q.today)
                self.assertTrue(isinstance(today.aqi, int))

            time.sleep(0.5)  # 善待免费api！

        for city in non_exist_cities:
            with self.subTest(city=city):
                with self.assertRaises(ValueError):
                    q = Q(city)
                    self.assertTrue(isinstance((today := q.today), wq.DayWeather))
                    self.assertTrue(isinstance(today.aqi, int))


if __name__ == "__main__":
    unittest.main()
