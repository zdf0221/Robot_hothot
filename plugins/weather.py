import json

import jieba.posseg as psg
import requests
from nonebot import on_command, on_natural_language, IntentCommand

from str_city import *


# on_command 装饰器将函数声明为一个命令处理器
# 这里 weather 为命令的名字，同时允许使用别名「天气」「天气预报」「查天气」
@on_command('weather', aliases=('天气', '天气预报', '查天气'))
async def weather(session):
    # print(session.state)
    # 从会话状态（session.state）中获取城市名称（city），如果当前不存在，则询问用户
    city = session.get('city', prompt='你想查询哪个城市的天气呢？')
    print(session.state, '@on_command')
    # 获取城市的天气预报
    weather_report = await get_weather_of_city(city)
    # 向用户发送天气预报
    await session.send(weather_report)


# weather.args_parser 装饰器将函数声明为 weather 命令的参数解析器
# 命令解析器用于将用户输入的参数解析成命令真正需要的数据
@weather.args_parser
async def weather_parser(session):
    # 去掉消息首尾的空白符
    stripped_arg = session.current_arg_text.strip()
    # print(stripped_arg,'@weather')

    if session.is_first_run:
        # 该命令第一次运行（第一次进入命令会话）
        if stripped_arg:
            # 第一次运行参数不为空，意味着用户直接将城市名跟在命令名后面，作为参数传入
            # 例如用户可能发送了：天气 南京
            session.state['city'] = stripped_arg
            # print(session.state)
        return

    if not stripped_arg:
        # 用户没有发送有效的城市名称（而是发送了空白字符），则提示重新输入
        # 这里 session.pause() 将会发送消息并暂停当前会话（该行后面的代码不会被运行）
        session.pause('要查询的城市名称不能为空呢，请重新输入')

    # 如果当前正在向用户询问更多信息（例如本例中的要查询的城市），且用户输入有效，则放入会话状态
    # session.state[session.current_key] = stripped_arg


async def get_weather_of_city(city):
    # 这里简单返回一个字符串
    # 实际应用中，这里应该调用返回真实数据的天气 API，并拼接成天气预报内容
    try:
        a_url = 'https://restapi.amap.com/v3/weather/weatherInfo?city='
        city_code = city_str[str(city)]
        key = '&key=' + 'cf038e879931c69b8d9fb384f67780dd'
        headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                                 'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.81 Safari/537.36'}
        respond = requests.get(a_url + str(city_code) + key)
        weather_dict = json.loads(respond.text)
        result = weather_dict['lives'][0]['city'] + '\n天气:' + weather_dict['lives'][0]['weather'] + '\n温度:' + \
                 weather_dict['lives'][0]['temperature'] + '\n风向:' + weather_dict['lives'][0][
                     'winddirection'] + '\n风力:' + weather_dict['lives'][0]['windpower'] + '\n湿度:' + \
                 weather_dict['lives'][0]['humidity'] + '\n时间:' + weather_dict['lives'][0]['reporttime']
        return '地区:' + result
    except:
        return '这位客官非常抱歉，这里的天气信息我暂时没有呢~请检查下？（比如完整輸入城市名称，后面带上“市”，“区”，“县”等等）'


@on_natural_language(keywords={'天气'})
async def natural_weather(session):
    stripped_msg = session.msg_text.strip()
    print(stripped_msg)
    words = psg.lcut(stripped_msg)
    print(words)
    city = None
    for word in words:
        if word.flag == 'ns':
            city = word.word
    return IntentCommand(90.0, 'weather', current_arg=city or ' ')
