from .getapi import GetApi
from .core import Querier
from .consts import LOGGER

def debug():
    """
    本函数用于调试 core.py 中 Querier 类的功能
    通过创建 Querier 对象并日志输出相关属性，来验证其功能是否正常
    """
    q = Querier("北京市")
    LOGGER.debug(q.forecast)
    LOGGER.debug(q.city_info)
    q = Querier("呼和浩特")
    LOGGER.debug(q.today)
    LOGGER.debug(q.city_info)