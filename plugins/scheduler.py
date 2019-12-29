import random
import sqlite3
from datetime import datetime

import math
import nonebot
import pytz
from aiocqhttp import MessageSegment
from aiocqhttp.exceptions import Error as CQHttpError
from aiocqhttp.message import Message
from nonebot import on_command, CommandSession


@nonebot.scheduler.scheduled_job('cron', hour='10-22')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    remind = [
        '我是提醒喝水小助手, 别忘了喝水哦~',
        '一天八杯水，不容易生病哦~',
        '多喝热水，并不会使你长胖，而会使你健康~',
        'A glass of water per hour keeps the doctor howl~',
        '劝人喝水，如同劝人学医。医者父母心~',
        '请注意，饮用超过95摄氏度的水可能导致死亡哦~',
        '在吃希莉娅之前，最好饮用足量的水源哦~',
        '众所周知，咸鱼的产生原因之一就是缺乏水分',
    ]
    group_list = []
    try:
        for group in group_list:
            await bot.send_group_msg(group_id=group,
                                     message=f'现在时间{now.hour}点整~' + random.choice(remind))
    except CQHttpError:
        pass


@nonebot.scheduler.scheduled_job('cron', day='*')
async def _():
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))

    conn = sqlite3.connect('test.db')
    print('connected!')
    cursor = conn.cursor()

    cursor.execute('delete from daily_rp')

    cursor.close()
    conn.commit()
    conn.close()


async def auto_alarm(dungeon, group_id, qq):
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    try:
        await bot.send_group_msg(group_id=group_id,
                                 message=str(MessageSegment.at(qq)) + '!!!\n'
                                         + f'现在时间{now.hour}点{now.minute}分！\n'
                                         + "你的地城设置："
                                         + dungeon
                                         + "还没有设置或者绑定，请尽快检查\n"
                                         + str(Message("再不做设置，小心村东头王寡妇半夜踹门~"))
                                 )
    except CQHttpError:
        pass


@on_command('alarm', only_to_me=False)
async def alarm(session: CommandSession):
    dungeon = session.get('dungeon', prompt='你想催促哪个地城的设置呢？')
    group_id = session.get('group_id', prompt='您想催促哪个群里的人呢？(群号)')
    qq = session.get('qq', prompt='你想催促谁做设置呢？(QQ号)')
    interval = session.get('interval', prompt='你想多长时间提醒一次呢？(分钟数)')
    nonebot.scheduler.add_job(auto_alarm, trigger='interval',
                              kwargs={'dungeon': dungeon, 'group_id': group_id, 'qq': qq, },
                              minutes=math.ceil(float(interval)),
                              id=qq)
    bot = nonebot.get_bot()
    now = datetime.now(pytz.timezone('Asia/Shanghai'))
    await bot.send_group_msg(group_id=group_id,
                             message=str(MessageSegment.at(qq)) + ' !!!\n' + f'现在时间{now.hour}点{now.minute}分！\n'
                                     + "你的地城设置："
                                     + dungeon
                                     + "还没有设置或者绑定，请尽快检查\n"
                                     + str(Message("再不做设置，小心村东头王寡妇半夜踹门~"))
                             )
    await session.send("您已经成功设置！")


@on_command('lift', aliases='解除提醒', only_to_me=False)
async def lift(session: CommandSession):
    qq = str(session.get('qq', prompt='您想解除谁的提醒呢？(QQ号)'))
    nonebot.scheduler.remove_job(job_id=qq)
    await session.send("您已经成功解除提醒！")
