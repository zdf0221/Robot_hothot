import random

from nonebot import on_command, CommandSession
from nonebot.command.argfilter import validators, extractors, ValidateError


@on_command('guess_number', aliases=('猜数字', '猜数游戏'))
async def guess_number(session: CommandSession):

    a = 0  # correct digit
    b = 0  # correct digit in wrong place

    print('target = ', session.state.get('target'))

    async def custom_validator(value):
        s = set(list(value))
        if len(value) != len(s):
            raise ValidateError('请不要輸入重复数字~')
        return value

    while not session.state['bingo'] and session.state['current_tries']:
        parm = 'guess' + str(session.state['current_tries'])
        guess = session.get(parm, prompt="请做出你的猜测", arg_filters=[
                extractors.extract_text,  # 提取纯文本部分
                str.strip,  # 去掉两边的空白
                validators.not_empty(),
                validators.match_regex(r'[0-9]{5}', '必须为5位数字'),
                custom_validator,
                # validators.ensure_true(lambda x: 9999 < int(x) < 100000, '必须猜测10000 ~ 99999中的数字')
            ], at_sender=True)

        guess_time = "这是第" + str(session.state['total_chances'] + 1 - session.state['current_tries']) + '次猜测:\n'
        for i in range(len(session.state.get('target'))):
            if guess[i] == session.state.get('target')[i]:
                a += 1
        for c in guess:
            if c in session.state.get('target'):
                b += 1
        b -= a
        # b = random.randint(1, 4)
        if a == session.state['length']:
            res = guess_time
            res += "恭喜你回答正确！\n"
            res += '你也可以百度搜索‘1A2B’获取移动端程式,祝您游戏愉快~'
            await session.send(res)
            session.state['bingo'] = True
            return
        res = guess_time
        res += "结果是："
        res += str(a) + 'A ' + str(b) + 'B'
        await session.send(res)
        session.state['current_tries'] -= 1
        a = b = 0

        if session.state['current_tries'] == 0:
            res = guess_time
            res += "抱歉，挑战失败，正确答案是"
            res += session.state.get('target')
            res += '\n你也可以百度搜索‘1A2B’获取移动端程式,祝您游戏愉快~'
            await session.send(res)
    return


@guess_number.args_parser
async def _(session: CommandSession):

    if session.is_first_run:

        session.state['length'] = 5
        session.state['bingo'] = False
        # print(type(session.state['length']))
        session.state['total_chances'] = 8
        session.state['current_tries'] = session.state['total_chances']

        number_list = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        target = ''
        menu = '我已经想好了一个'
        menu += str(session.state['length'])
        menu += '位的数字，你现在可以猜了(0-9, 不会出现重复数字,一共有'
        menu += str(session.state['total_chances'])
        menu += '次机会~）\n'
        menu += '在返回的结果中，A代表数字和位置均匹配，B代表存在该数字，但位置不正确'
        await session.send(menu)
        while len(target) < session.state['length']:
            temp = random.randint(0, 9)
            if number_list[temp] != -1:
                target += str(number_list[temp])
                number_list[temp] = -1
        session.state['target'] = target
