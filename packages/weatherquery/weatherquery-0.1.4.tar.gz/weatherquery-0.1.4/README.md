# WeatherQuery
> 一个轻量快捷的天气查询Python库

中文 / [English](./docs/README-en.md)

## 安装
通过pip命令直接安装：
```bash
pip install git+https://gitee.com/xiatianxuan/weatherquery
```

## 使用
1. 导入`weatherquery`库
```python
import weatherquery as wq
```

2. 创建获取器
```python
q = wq.Querier("北京") # 将北京替换成你想查询的城市名
```

3. 查询
```python
print(q.today) # 打印今日天气
```
> 查询其他信息请参考 `src/weatherquery/core.py`

## 作者
[xiatianxuan](https://github.com/xiatianxuan)
[fexcode](https://github.com/fexcode)

## 声明
本项目使用的API由 `http://t.weather.itboy.net/api/weather/city/` 免费提供，仅供个人技术用途，禁止商用，禁止滥用。因滥用本项目而产生的任何负面影响与本项目无关！