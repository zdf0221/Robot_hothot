import random
import re
import sqlite3


import jieba.posseg as psg
from aiocqhttp import MessageSegment, ActionFailed
from nonebot import on_command, CommandSession, on_notice, NoticeSession, permission as perm
from nonebot import on_natural_language, NLPSession, IntentCommand
from nonebot.command.argfilter import validators, extractors, ValidateError

repeat_flag = 0


@on_command('help', aliases=('帮助', '机器人出来'), only_to_me=False)
async def help_fuc(session: CommandSession):
    menu = "沙雕机器人烫烫为您服务~烫烫烫……"
    menu += "现在开通的功能有：查询天气，复读机（伪），整点报时，地城提醒与解除，猜数字小游戏，每日运势骰子机等……"
    menu += "WOD便携式图书馆 V.2.0\n" \
            ".help \t//帮助，列出帮助\n" \
            ".mosaicist | xs \t//镶嵌师\n" \
            ".mosaic | xq \t//镶嵌材料及种族\n" \
            ".potion | yj \t//属性药剂&技能药剂\n" \
            ".mosaic_formula | xgs \t//镶嵌公式\n" \
            ".tune | gq \t//常用鼓励歌曲\n" \
            ".book | bo \t//常用书籍\n" \
            ".herb | cy \t//草药耗材\n" \
            ".dodge | sd \t//闪躲公式\n" \
            ".challenge | tz \t//挑战地城及准入条件（感觉没啥用，暂时没搬运）\n"\
            ".scroll | sj \t//常用卷轴支援/加持耗材\n" \
            ".gods_name | gn \t//各神名具体效果\n" \
            ".blessing | zf \t//祭祀祝福具体效果\n" \
            ".item | wp \t//查询物品（暂未搬运）\n"\
            ".skill | jn \t//查询技能(施工中)\n"
    await session.send(menu)


@on_command('mosaicist', aliases=('xs', '镶嵌师'), only_to_me=False)
async def mosaicist(session: CommandSession):
    respond = "高矮\t：[hero: “烈怒之眼”萨米尔安]\n" \
              "丘矮\t：[hero:人形战车的藤原千花]\n" \
              "半身\t：[hero: 狗头人皇家厨师长] [hero: 报丧女妖·UC]\n" \
              "林地\t：[hero: 夜神狼歌]\n" \
              "M精\t：[hero: M精射手] [hero: 戏命师·烬]\n" \
              "T精\t：[hero: 仙·道友]\n" \
              "卡拉希\t：[hero: “愚者之座”霍姆勒斯]\n" \
              "边塞\t：[hero: 基定·尤拉] [hero: 银色守卫] [hero: “红莲圣徒”玛嘉烈] [hero:护花使者的石上优]\n" \
              "丁丁\t：[hero: 梦魇异音布瑟拉] [hero: 嘉兰诺德]\n" \
              "拉沙尼\t：[hero: 伊莫拉图斯] [hero: 神·道友] [hero: 克维苏蒙的永世荒芜][hero: 万花通灵·妮蔻]\n" \
              "侏儒\t：[hero:机关算尽的四宫辉夜] [hero: “大乘金刚”钧菩提] [hero: 银羽]\n" \
              "\n" \
              "（最后更新于2019/09/14）\n"
    await session.send(respond)


@on_command('mosaic', aliases=('xq', '镶嵌'), only_to_me=False)
async def mosaic(session: CommandSession):
    respond = "高山矮人-->[*宝石砂][金属制盔甲]\n"\
              "丘陵矮人-->[*镶嵌宝石][金属制武器]\n"\
              "半身人-->[*纱线][织品]\n"\
              "林地人-->[*颜料][木制物品]\n"\
              "玛格-莫精灵-->[优质*树脂][木制武器]\n"\
              "提伦-埃精灵-->[*墨汁][羊皮纸]\n"\
              "卡拉希人-->[昂贵的*染料][皮毛]\n"\
              "边塞人-->[*金属片][奢侈装饰品]\n"\
              "丁图安蛮族-->[*浮雕指南][石制物品]\n"\
              "拉沙尼人-->[精制*白垩粉][骨头]\n"\
              "侏儒-->[*皮绑带][皮革衣服]\n"
    await session.send(respond)


@on_command('potion', aliases=('yj', '药剂'), only_to_me=False)
async def potion(session: CommandSession):
    respond = "*智者秃顶*\t智力\n" \
              "*巨魔肌腱*\t力量\n" \
              "*北境柳*\t意志\n" \
              "*铅树心木*\t体质\n" \
              "*蟹蛛丝囊*\t灵巧\n" \
              "*魔鬼爪*\t敏捷\n" \
              "*黑枭眼珠*\t感知\n" \
              "*萤火虫软壳*\t魅力+智力\n" \
              "*银刺嫩叶*\t全属性\n"\
              "----------------\n"\
              "*斑叶防风*\t远程及派生\n" \
              "*龙血树胶*\t近战及派生\n" \
              "*蓝越橘*\t教育\n" \
              "*曼陀罗*\t心灵及心灵护甲\n" \
              "*紫龙舌兰*\t爆破\n" \
              "*血榆实*\t火冰能攻四大法系及其派生\n" \
              "*雪蓟*  \t德鲁伊技能及冰伤冰甲\n" \
              "*白鬼帽*\t预知\n" \
              "*阿伊恩萿*\t领导才能\n" \
              "*毛冬青*\t勇歌嘲弄歌及心防\n" \
              "*莲花芯*\t治疗及其派生\n"
    await session.send(respond)


@on_command('mosaic_formula', aliases=('xgs', '镶嵌公式'), only_to_me=False)
async def mosaic_formula(session: CommandSession):
    respond = "（只列出额外属性增益）\n" \
              ".2s    //（2孔）\n" \
              ".3s    //（3孔）\n" \
              ".4s    //（4孔）\n" \
              ".5s    //（5孔）\n"
    await session.send(respond)


@on_command('2s', only_to_me=False)
async def two_slots(session: CommandSession):
    respond = "蓝宝=1魅力"
    await session.send(respond)


@on_command('3s', only_to_me=False)
async def three_slots(session: CommandSession):
    respond = "蓝蓝米=1智力\n" \
              "蓝蓝紫=1意志\n" \
              "蓝蓝宝=1魅力1感知\n"\
              "绿绿米=1意志\n"\
              "黛绿米=2意志\n"\
              "红红紫=1力量\n"\
              "红红米=1体质1力量\n"\
              "黛黛紫=1灵巧\n"\
              "黛黛米=1感知\n"\
              "黄黄紫=1感知\n"\
              "黄紫黛=2敏捷\n"\
              "黄紫宝=1力量\n"\
              "绿绿紫=1体质\n"\
              "黄黄米=1灵巧\n"\
              "红绿米=2力量\n"
    await session.send(respond)


@on_command('4s', only_to_me=False)
async def four_slots(session: CommandSession):
    respond = "绿绿黛米=4意志\n" \
              "黛黛黄紫=3敏捷1灵巧\n" \
              "黛A黛B黄紫=4敏捷1灵巧（仅在支持2种材料时可用）\n" \
              "黛黄黄紫=1感知2敏捷\n" \
              "蓝蓝米宝=2智力2感知1魅力\n" \
              "蓝蓝蓝宝=2感知2魅力\n" \
              "黄宝宝紫=2力量\n" \
              "黛黛黄米=1感知1意志\n" \
              "黄红黛米=2意志\n" \
              "红绿米米=3力量1灵巧\n" \
              "黄黄米米=2灵巧1智力1感知\n" \
              "红绿米黛=2力量2意志\n" \
              "绿A绿B黛米=5意志（仅在支持2种材料时可用）\n" \
              "红红米米=2体质1力量1灵巧\n "
    await session.send(respond)


@on_command('5s', only_to_me=False)
async def five_slots(session: CommandSession):
    respond = "黛A黛B黛黄紫=5敏捷1灵巧（仅在支持2种材料时可用）\n" \
              "黛黛黛黄紫=4敏捷1灵巧\n" \
              "黛A黛B宝黄紫=4敏捷1灵巧1力量1感知1意志（仅在支持2种材料时可用）\n" \
              "黛黛黄黄紫=3敏捷1灵巧1感知\n" \
              "黛黛黄米紫=3敏捷1灵巧1感知\n" \
              "黛黛黄宝紫=3敏捷1灵巧1力量1感知1意志\n" \
              "宝黄红黛紫=2敏捷2意志1力量\n" \
              "红红米A米B绿=6力量2体质（仅在支持2种材料时可用）\n" \
              "红红米米绿=4力量2灵巧2体质\n" \
              "红米米黛绿=3力量1灵巧2意志\n" \
              "宝宝宝紫黄=3力量\n"\
              "红红米米紫=2力量1灵巧2体质\n"\
              "绿绿绿黛米=5意志\n" \
              "绿绿黛黛米=4意志1感知\n" \
              "黛黛黄红宝=3意志1感知\n" \
              "黛黄红宝宝=3意志 \n" \
              "黛黄红蓝宝=2意志1魅力\n" \
              "蓝蓝紫米宝=1意志1魅力2智力2感知\n" \
              "蓝蓝蓝米宝=3感知2智力2魅力\n" \
              "蓝蓝米宝宝=3感知3智力1魅力\n" \
              "蓝蓝蓝宝紫=2感知2魅力1意志\n" \
              "黛黛黄米宝=2感知1意志\n" \
              "黄黄米米米=3灵巧2智力1感知\n" \
              "黄黄米米紫=2灵巧2感知1智力\n" \
              "米米米红红=3体质2力量1灵巧\n"
    await session.send(respond)


@on_command('tune', aliases=('gq', '歌曲'), only_to_me=False)
async def tune(session: CommandSession):
    respond = "勇气    \t[近战命中]  \n" \
              "胜利    \t[近闪]\n" \
              "顽强    \t[心防]\n" \
              "神圣    \t[心防及神圣伤]\n" \
              "精湛    \t[远程命中]\n" \
              "躲闪飞弹\t[远闪]\n" \
              "回复    \t[回蓝]\n"\
              "查桑    \t[自然防] \n" \
              "迅速    \t[加动]\n" \
              "敏捷    \t[加敏捷]\n"
    await session.send(respond)


@on_command('book', aliases=('bo', '书籍'), only_to_me=False)
async def book(session: CommandSession):
    respond = "战技    \t[近战技能]\n" \
              "穿山    \t[远程技能]\n" \
              "历法    \t[火焰能量寒冰攻击4法术]\n" \
              "集中注意力\t[先攻]\n" \
              "意志力优势\t[心防魔防]\n" \
              "高闪    \t[远近闪]\n" \
              "防魔    \t[防御魔法]\n" \
              "民兵    \t[远/近/领导技能]\n" \
              "占星    \t[预知/预感等]"
    await session.send(respond)


@on_command('herb', aliases=('cy', '草药'), only_to_me=False)
async def herb(session: CommandSession):
    respond = "*巨魔*  \t力量\n" \
              "*绿斑鸠*\t病毒防+DR\n" \
              "*红花瓣*\t敏捷先攻\n" \
              "*甜根*  \t魅力回蓝\n" \
              "*醋栗果*\t意志智力\n" \
              "*羽毛叶*\t智力感知\n" \
              "*玛丽约翰娜*\t心防\n" \
              "*薄叶*  \t回血\n" \
              "\n" \
              "[七色花]：\n" \
              "口袋: 白银向日葵 远程\n" \
              "口袋: 紫水晶蝴蝶兰 魔法\n" \
              "口袋: 翡翠秋菊 自然\n" \
              "口袋: 赤红琥珀芍药 爆破\n" \
              "口袋: 黄玉百合 近战\n" \
              "口袋: 黄金玫瑰 心理\n" \
              "口袋: 黑玛瑙郁金香 远近防+病毒\n" \
              "2=使用: 意志+3+13%SL\n" \
              "3=使用: 力/意+3+13%SL 体回/法回+17%SL\n" \
              "4=草药运用+1 使用: 灵/体/敏/力+3+13%SL\n" \
              "5=草药运用+2 使用: 灵/体/敏/感+3+13%SL\n" \
              "6=草药运用+3 使用: 魅/智/敏/感+3+13%SL\n" \
              "7=草药运用+3 草药知识+1 使用: 魅/智/感/意+3+13%SL, 先攻+20%SL\n"
    await session.send(respond)


@on_command('dodge', aliases=('sd', '闪躲'), only_to_me=False)
async def dodge(session: CommandSession):
    respond = "近战 2*敏捷+灵巧\n" \
              "远程 2*敏捷+感知\n" \
              "魔法 2*意志+智力\n" \
              "心理 2*意志+魅力\n" \
              "诅咒 2*魅力+意志\n" \
              "疾病 2*体质+魅力\n" \
              "陷阱 2*感知+敏捷\n" \
              "自然 2*意志+敏捷\n" \
              "偷袭 2*感知+智力\n" \
              "爆破 2*敏捷+感知\n" \
              "冲击 2*灵巧+力量\n" \
              "魔法弹 2*智力+敏捷\n" \
              "撞击 3*敏捷\n"
    await session.send(respond)


@on_command('scroll', aliases=('sj', '支援卷轴'), only_to_me=False)
async def scroll(session: CommandSession):
    respond = "（不包含大部分无限耗材）\n" \
              "辛努安*  近战命中\n" \
              "费欧乃*  回蓝\n" \
              "那拉许*  远程技能\n" \
              "佩雷庶安*  近闪\n" \
              "支援*   敏捷近远闪\n" \
              "精确*   远近命中\n" \
              "觉醒*   灵巧感知先攻\n" \
              "愤怒*   加动扣回血\n" \
              "孤狼*   近闪\n" \
              "迅鼬*   远闪\n" \
              "蔑视*   心防魔防\n" \
              "防毒*   毒dr\n" \
              "完全治愈*  回血\n" \
              "集中注意力* 血量力量扣先攻\n" \
              "防魔卷轴  魔防\n" \
              "防魔*  更多魔防扣回血\n" \
              "雄鹰*  感知\n" \
              "黑熊*  力量\n" \
              "躲避*  远闪\n" \
              "急速*  敏捷先攻\n" \
              "火焰*  近战火伤\n" \
              "毒蛇*  远近毒伤\n" \
              "顽强*  心防"
    await session.send(respond)


@on_command('gods_name', aliases=('gn', '神名'), only_to_me=False)
async def gods_name(session: CommandSession):
    respond = "阿克贝斯=魔法防御&心防\n" \
              "阿克雷斯=远程命中&远闪\n" \
              "迪莫桑=近战命中&近闪\n" \
              "拉尚=病毒防\n" \
              "查桑=自然防\n" \
              "[完美]\n" \
              "头部：+2 +0.34HL\n" \
              "耳环：+2 +0.10HL\n" \
              "项链：+5 +0.50HL\n" \
              "手镯：+3 +0.34HL\n" \
              "腰带：+2 +0.25HL\n" \
              "戒指：+2 +0.20HL\n" \
              "[非常优良]\n" \
              "头部：+2 +0.25HL\n" \
              "耳环：+2 +0.10HL\n" \
              "项链：+3 +0.34HL\n" \
              "手镯：+3 +0.25HL\n" \
              "腰带：+2 +0.20HL\n" \
              "戒指：+2 +0.15HL\n"\
              "--------------------"\
              "法亚培厄=魔法命中&魔防\n" \
              "火焰派生类别+1 \n" \
              "寒冰派生类别+1 \n" \
              "能量派生类别+1 \n" \
              "神圣派生类别+1 \n" \
              "\n" \
              "阿泽拉丝=心理命中&心防\n" \
              "心灵派生类别+1 \n" \
              "领导才能派生类别+1 \n" \
              "\n" \
              "费基斯=自然命中&自然防 \n" \
              "\n" \
              "耶路奇亚=病毒命中&病毒防\n" \
              "疫病派生类别+1 \n" \
              "\n" \
              "胡托=近战命中&近闪 \n" \
              "\n" \
              "古诺=远程命中&远闪\n" \
              "远程派生类别+1 \n"\
              "\n" \
              "弗拉=诅咒命中&诅咒防\n" \
              "阴影派生类别+1 \n" \
              "灵魂派生类别+1 \n"
    await session.send(respond)


@on_command('blessing', aliases=('zf', '祝福'), only_to_me=False)
async def blessing(session: CommandSession):
    respond = "爱奥拉的奉献 - 魅力，回蓝，治疗技能等级\n"\
              "爱奥拉的援助 - 回血\n"\
              "黑魔法防御术 - 魔抗，诅咒抗，元素DR\n"\
              "迪莫桑净化之火 - 火伤，神圣伤\n"\
              "阿克雷斯的保护 - 陷阱防，偷袭防，陷阱远程DR\n"\
              "阿克雷斯之艺 -  毒DR， 吹管涂毒技能等级，远程偷袭命中\n"\
              "迪莫桑之盾 - 近战DR，近战火DR\n"\
              "塞缪尔神迹 - 力量，盾挡与派生等级，粉碎等级\n"\
              "艾维斯的威信 - 心攻DR，心防技能等级，名誉技能等级\n"\
              "拉尚的平衡 - 心攻DR，病毒与治疗等级，病毒与心攻命中\n"\
              "查桑的暴风 - 动数（3%SL），近战效果，近战防御减值（25%）\n"\
              "迪莫桑的复仇 - 钝器及派生等级和效果\n"\
              "查桑的复仇 - 德鲁伊DR，命中，技能等级，自然命中防御"
    await session.send(respond)


@on_command('repeat')
async def repeat(session: CommandSession):
    global repeat_flag
    if repeat_flag:
        await session.send(session.state.get('message') or session.current_arg)


@on_command('perfunctory')
async def perfunctory(session: CommandSession):
    respond = [
        "嗯嗯，然后呢？",
        "有趣",
        "soga~",
        "嗯嗯，有意思",
        "继续继续~",
        "哈哈哈",
        "好呀好呀",
        "真的吗？",
        "不可思议",
        "太神奇了！",
        "Amazing！",
        "惊不惊喜，意不意外？",
        "恩恩额啊啊啊好啊（敷衍",
        "(光速逃跑",
        "烫烫听不懂呢……呜呜呜……",
        "你在说什么呀？我怎么不明白",
        "？",
        "啊，是说话听不懂的孩子呢……",
    ]
    await session.send(random.choice(respond))


@on_command('switch_on', aliases=('复读机启动', '开始复读', '复读机开启'), permission=perm.SUPERUSER)
async def repeat_on(session: CommandSession):
    await session.send('已开启复读模式！')
    global repeat_flag
    repeat_flag = 1


@on_command('switch_off', aliases=('复读机关闭', '停止复读', '复读机停止'), permission=perm.SUPERUSER)
async def repeat_off(session: CommandSession):
    await session.send('已关闭复读模式！')
    global repeat_flag
    repeat_flag = 0


@on_command('greeting')
async def greeting(session: CommandSession):
    respond = [
        "你好",
        "Hi~",
        "おはようございます~",
        "这位客官想聊点什么？",
        "哈罗2号机，烫烫，为您服务~"
    ]
    await session.send(random.choice(respond))


@on_command('poet')
async def poet(session: CommandSession):
    respond = [
        "苟利国家生死矣, 岂因福祸避趋之~",
        "你们还是要学习一个~",
        "不要想着整天搞个大新闻~",
        "Naive!",
        "I'm angry!",
    ]
    await session.send(random.choice(respond))


@on_command('地城提醒')
async def alarm_desc(session: CommandSession):
    respond = "命令格式：輸入!alarm, 后续根据提示輸入"
    await session.send(respond)


@on_command('提醒解除')
async def lift_desc(session: CommandSession):
    respond = "命令格式：輸入!lift, 后续根据提示輸入"
    await session.send(respond)


@on_command('counter_attack')
async def counter_attack(session: CommandSession):
    respond = [
        '呸~你才丢人，你全家都丢人！',
        '你说谁辣鸡呢，小菜鸡',
        '汝甚吊，汝母知否？',
        '我才不是弱鸡！',
        '不要骂脏话，小心被雷劈~',
        '瘪犊子（指东北话）',
        '完蛋玩意儿！',
        '呸~你才辣鸡，你全家都辣鸡！',
        '呸~你才弱鸡，你全家都弱鸡！',
        '天道好轮回~苍天饶过谁~',
        '这个人脑子what啦？',
        '帮帮忙，侬的脑子what伐啦？',
    ]
    await session.send(random.choice(respond))


@on_command('caixukun')
async def caixukun(session: CommandSession):
    respond = [

        '你才是蔡徐坤，你全家都是rapper',
        '少侠这篮球想必打的极好',
        '你会唱，跳，rap，篮球~',
        '鸡你太美，贝贝~',
        '大家好，我是练习时长两天半的个人练习生，烫烫~'
    ]
    await session.send(random.choice(respond))


@on_command('name')
async def name(session: CommandSession):
    respond = [
        '我是烫烫，是机器人哦~',
        '锟斤拷烫烫烫，就是少侠我~',
        '你们可以叫我烫哥~嘿嘿',
        '大家好，我是练习时长两天半的个人练习生，烫烫~'
    ]
    await session.send(random.choice(respond))


@on_command('encourage')
async def encourage(session: CommandSession):
    respond = [
        '谢谢夸奖~我以后会做得更好',
        '谢谢夸奖~',
        '哼哼，这只是百分之一呢',
        '我才不是弱鸡~只是小了一点而已',
        '客官过奖，嘿嘿嘿',
    ]
    await session.send(random.choice(respond))


@on_command('friends')
async def friends(session: CommandSession):
    friend_name = session.current_arg_text.strip()
    respond = '哦是' + friend_name + '老师啊，我知道我知道（翻字典）'
    await session.send(respond)


@on_command('eat')
async def eat(session: CommandSession):
    respond = [
        '不要吃烫烫呀！咿呀呀呀呀呀呀呀！~',
        '不好意思，机器人是不能吃的！',
        '吃？是说充电吗？',
    ]
    await session.send(random.choice(respond))


@on_command('beauty')
async def beauty(session: CommandSession):
    try:
        respond = MessageSegment.image('/dl/hana.jpg')
        await session.send(respond, ignore_failure=False)
    except ActionFailed as e:
        print(e.retcode)


@on_notice('group_increase')
async def _(session: NoticeSession):
    await session.send('欢迎新朋友～')


@on_natural_language(keywords={'你好', 'Hi', 'hello'})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'greeting')


@on_natural_language(keywords={'蛤', '江'}, only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(90.0, 'poet')


@on_natural_language(keywords={'丢人', '菜', '弱', '废', '辣鸡', '你妈', '尼玛', '傻', '逼',
                               '白痴', '犊子', '蠢', '二货', '智障', '制杖', '完蛋玩意'})
async def _(session: NLPSession):
    # return IntentCommand(90.0, 'greet')
    return IntentCommand(90.0, 'counter_attack')


@on_natural_language(keywords={'蔡', '徐', '坤'})
async def _(session: NLPSession):
    # return IntentCommand(90.0, 'greet')
    return IntentCommand(90.0, 'caixukun')


@on_natural_language(keywords={'不错', '厉害', '牛'})
async def _(session: NLPSession):
    # return IntentCommand(90.0, 'greet')
    return IntentCommand(90.0, 'encourage')


@on_natural_language(keywords={'名字', '烫烫'})
async def _(session: NLPSession):
    # return IntentCommand(90.0, 'greet')
    return IntentCommand(90.0, 'name')


@on_natural_language(keywords={'调戏哈罗'}, )
async def _(session: NLPSession):
    return IntentCommand(90.0, 'trick')


@on_natural_language(keywords={'认识'}, )
async def _(session: NLPSession):
    stripped_msg = session.msg_text.strip()
    words = psg.lcut(stripped_msg)
    friend_name = ""
    for word in words:
        print(word.flag)
        if word.flag in ["nr", "n"]:
            friend_name += word.word
    return IntentCommand(90.0, 'friends', current_arg=friend_name or ' ')


@on_natural_language(keywords={'吃', 'eat', '餐'})
async def _(session: NLPSession):
    return IntentCommand(90.0, 'eat')


@on_natural_language(only_to_me=True)
async def _(session: NLPSession):
    return IntentCommand(50.0, 'perfunctory', None, session.msg)


@on_natural_language(only_to_me=False)
async def _(session: NLPSession):
    return IntentCommand(30.0, 'repeat', None, session.msg)
