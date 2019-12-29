import random, sqlite3
import re

from nonebot import on_command, CommandSession


@on_command('jrrp', only_to_me=False)
async def jrrp(session: CommandSession):

    conn = sqlite3.connect('test.db')
    print('connected!')
    cursor = conn.cursor()

    print(session.ctx['sender'])
    uid = session.ctx['user_id']
    print(type(uid))
    name = session.ctx['sender']['nickname']
    print(name)

    cursor.execute('select * from daily_rp where id=?', (uid, ))
    values = cursor.fetchone()
    print(type(values))
    if values is not None:
        # already tested
        result = values[1]
    else:
        if uid in [543112018, 630661187, 379084394, 86366094, 105766067]:
            # test VIP list: self, 嘉兰，罗伊，安康，ves
            result = 100 - random.randint(0, 5)
        else:
            result = random.randint(0, 100)
        cursor.execute('insert into daily_rp values (?, ?)', (uid, result))
    print(result)
    respond = "*" + name + '今天的运势指数是' + str(result) + '%\n' + ('|' * result)
    await session.send(respond)
    cursor.close()
    conn.commit()
    conn.close()


@on_command('r', only_to_me=False)
async def dice(session: CommandSession):
    ans = []
    offset = 0
    # pattern = r'(?P<x>[1-9]*[0-9]*)(?P<d>d)(?P<y>[1-9]*[0-9]*)(?P<offset>[\+\-][1-9]*[0-9])'
    match = re.split('d|\+', session.current_arg.replace(" ", ""))
    print(session.current_arg)
    print(match)
    x = int(match[0]) if match[0] else 1
    y = int(match[1]) if match[1] else 100
    if len(match) == 3:
        offset = int(match[2]) if match[2] else 0
    print('x = ', x, 'y = ', y, 'offset = ', offset)
    for i in range(x):
        ans.append(random.randint(1, y) + offset)
    print(ans)
    respond = "Result = " + str(ans)
    await session.send(respond)

