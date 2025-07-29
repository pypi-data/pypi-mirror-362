GLOBAL_DEBUG = False  # 全局调试标志
PRINT_TIME = False if GLOBAL_DEBUG else False  # 函数运行耗时 是否输出
CITIES_FILE_PATH = "src/weatherquery/assets/citycodes.json"


class Logger:
    def __init__(self, is_debug: bool):
        self.__is_debug = is_debug

    def log(self, text: str, flag: str = "LOG") -> None:
        if self.__is_debug:
            print(f"{flag}:\t{text}")

    def debug(self, text: str):
        self.log(text, "DEBUG")

LOGGER = Logger(GLOBAL_DEBUG)