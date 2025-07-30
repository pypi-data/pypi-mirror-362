import unittest

__import__("sys").path.append("../src")

import weatherquery as wq
from weatherquery import GetApi as GApi

import os

if "tests" in os.getcwd():
    os.chdir("..")


class TestAdd(unittest.TestCase):
    def test_get_api_type(self):
        self.assertEqual(isinstance(GApi.get_api_by_citycode("101010100"), dict), True)
        self.assertEqual(
            isinstance(GApi.get_citycode_from_cityname("芜湖市"), str), True
        )

        try:
            int(GApi.get_citycode_from_cityname("芜湖市"))
        except TypeError as t:
            self.fail(
                f"GetApi.get_citycode_from_cityname() 返回的城市编码无法转换成整数: {t}"
            )
        except Exception as e:
            self.fail(f"预期外的错误：{e}")

        self.assertEqual(isinstance(GApi.get_city_weather_dict("芜湖市"), dict), True)

    def test_fuzzy_mathcing_citynames(self):
        f = GApi._is_the_same_city

        self.assertEqual(f("芜湖", "芜湖市"), True)
        self.assertEqual(f("安徽省", "安徽"), True)
        self.assertEqual(f("内蒙古自治区", "内蒙古"), True)
        self.assertEqual(f("澳门特别行政区", "澳门"), True)
        self.assertEqual(f("某个", "某个县"), True)
        self.assertEqual(f("北京", "北京市"), True)


if __name__ == "__main__":
    unittest.main()
