import os

if "tests" in os.getcwd():
    os.chdir("..")
    __import__("sys").path.append("./src")
else:
    __import__("sys").path.append("./src")
import unittest

# 定义测试目录
test_directory = "./tests"

# 使用 TestLoader 的 discover 方法来发现目录下的所有测试用例
test_suite = unittest.defaultTestLoader.discover(test_directory)

# 使用 TextTestRunner 来运行测试用例并输出结果
test_runner = unittest.TextTestRunner()
test_runner.run(test_suite)
