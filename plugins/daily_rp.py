import math
import random
import sqlite3

from nonebot import on_command, CommandSession


@on_command('jrrp', only_to_me=False)
async def jrrp(session: CommandSession):

    conn = sqlite3.connect('test.db')
    print('connected!')
    cursor = conn.cursor()

    print(session.ctx['sender'])
    uid = session.ctx['user_id']

    name = session.ctx['sender']['nickname']
    print(name)

    cursor.execute('select * from daily_rp where id=?', (uid, ))
    values = cursor.fetchone()
    print(type(values))
    if uid in [602729577, 379084394, 105766067]:
        result = 100 - random.randint(0, 10)
    elif values:
        result = values[1]
    else:
        result = int(math.sqrt(random.randint(0, 100)) * 10)
    cursor.execute('insert into daily_rp values (?, ?)', (uid, result))
    print(result)
    respond = "*" + name + '今天的运势指数是' + str(result) + '%\n' + ('|' * result)
    await session.send(respond)
    cursor.close()
    conn.commit()
    conn.close()
