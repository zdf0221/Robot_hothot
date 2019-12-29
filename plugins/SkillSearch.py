# -*- coding: utf-8 -*-
"""
-------------------------------------------------
   File Name：     SkillSearch
   Description :
   Author :       zdf's desktop
   date：          2019/9/17
-------------------------------------------------
   Change Activity:
                   2019/9/17:22:27
-------------------------------------------------
"""

import random, sqlite3
import re

from nonebot import on_command, CommandSession


@on_command('skill', aliases=('jn', '技能'), only_to_me=False)
async def skill(session: CommandSession):
    conn = sqlite3.connect('test.db')
    print('connected!')
    cursor = conn.cursor()
    cursor.execute('select * from skill')
    result = cursor.fetchone()
    respond = "您本次抽到的技能为：" + str(result)
    await session.send(respond)


