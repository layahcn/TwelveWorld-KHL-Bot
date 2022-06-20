# 开黑啦机器人SDK
from xmlrpc.client import boolean
from khl import Bot, Message, EventTypes, Event
from khl.card import CardMessage, Card, Module, Element, Types

# 解析Html网页标签
from bs4 import BeautifulSoup

# 输出系统日志
import logging

# 读取配置文件
import json

# 随机数
import random

# 正则表达式
import re

# 时间戳转换
import time

# 发起网络连接
import requests as req

# 初始化机器人
with open('config/config.json', 'r', encoding='utf-8') as f:
    config = json.load(f)
bot = Bot(token=config['token'])


@bot.command(name='roll')
async def roll(msg: Message, t_min: int = 1, t_max: int = 100):
    result = random.randint(t_min, t_max)
    await msg.reply(str(result))
# 指令1【/roll min max】经典roll


@bot.command(name='bd')
async def bd(msg: Message, str: str):
    cm = CardMessage(Card(
        Module.Section(
            Element.Text(f'需要我帮您百度一下【{str}】吗？', Types.Text.PLAIN),
            Element.Button(
                '百度一下', f'https://www.baidu.com/s?wd={str}', Types.Click.LINK, theme=Types.Theme.INFO)
        )
    ))
    await msg.ctx.channel.send(cm)
# 指令2【/bd string】百度搜索


@bot.command(name='bl')
async def bl(msg: Message, str: str):
    cm = CardMessage(Card(
        Module.Section(
            Element.Text(f'需要我帮您哔哩哔哩一下【{str}】吗？', Types.Text.PLAIN),
            Element.Button(
                '哔哩哔哩', f'https://search.bilibili.com/all?keyword={str}', Types.Click.LINK, theme=Types.Theme.DANGER)
        )
    ))
    await msg.ctx.channel.send(cm)
# 指令3【/bl string】b站搜索


@bot.on_event(EventTypes.JOINED_GUILD)
async def joined_guild(b: Bot, event: Event):
    channel = await b.fetch_public_channel('8407342412718220')  # 欢迎频道id
    number = random.randint(1, 11)
    if number == 1:
        welcome = f'整个嘘独王国都在低语呼唤着(met){event.body["user_id"]}(met)……'
    if number == 2:
        welcome = f'(met){event.body["user_id"]}(met)坐上了人间大炮！直上云霄！'
    if number == 3:
        welcome = f'(met){event.body["user_id"]}(met)非常慷慨地带着十万卡玛来了！大家鼓掌欢迎！'
    if number == 4:
        welcome = f'(met){event.body["user_id"]}(met)乘着龙鸟快线大驾光临！'
    if number == 5:
        welcome = f'械勒神不小心对(met){event.body["user_id"]}(met)用了个传送之术……'
    if number == 6:
        welcome = f'子曾经曰过，天上不会掉馅饼，只会掉下个(met){event.body["user_id"]}(met)！'
    if number == 7:
        welcome = f'嘿，(met){event.body["user_id"]}(met)，尝尝新摘下来的苹朵吧？'
    if number == 8:
        welcome = f'奥古之乱的大洪水把(met){event.body["user_id"]}(met)冲到这儿来了~'
    if number == 9:
        welcome = f'一只野生的(met){event.body["user_id"]}(met)出现了！'
    if number == 10:
        # 此条作者为酸涩酱
        welcome = f'因卡纳姆掉下来一个(met){event.body["user_id"]}(met)，贝老伯家房顶又塌了！'
    if number == 11:
        # 此条作者为破翅膀
        welcome = f'撒迪达之神撒下了一粒种子，长出了个(met){event.body["user_id"]}(met)！'
    await b.send(channel, welcome)
# 事件1【JOINED_GUILD】欢迎新人


@bot.task.add_interval(hours=6)
async def checkwx():
    dateset = wxgethtml(1)
    with open('wx.json', 'r', encoding='utf-8') as f:
        wxjson = json.load(f)
    judge = dateset in wxjson.get('datetitle')
    print(judge)
    if not judge:
        wxjson.get('datetitle').append(dateset)
        with open('wx.json', 'w') as write_f:
            write_f.write(json.dumps(wxjson))
        wximg = wxgethtml(2, wxtitle)
        cm = stdcard('wx', wxtitle, wxgethtml(
            2, wxtitle, 'false'), wximg, wxdate)
        channel = await bot.fetch_public_channel('3446958221309451')
        await bot.send(channel, cm)
# 定时检测1【checkwx】微信最新文章


def stdcard(mode: str, title: str, link: str, img: str, date: str):
    if mode == 'wx':
        btn = '搜索文章'
        avatar = 'http://wx.qlogo.cn/mmhead/Q3auHgzwzM7ZnPbIDnIibUDKyzYRAagHD1Q3lWfeq7TZRnyW4ABYiacg/0'
        author = 'Wakfu真好玩'
        icon = 'https://weixin.qq.com/zh_CN/htmledition/images/wechat_logo_109.2x219536.png'
        media = '微信公众平台'
    cm = CardMessage(Card(
        Module.Section(
            Element.Text(f'**{title}**', Types.Text.KMD),
            Element.Button(btn, link, Types.Click.LINK,
                           theme=Types.Theme.SUCCESS)
        ),
        Module.Context(
            Element.Image(avatar),
            Element.Text(author)
        ),
        Module.Container(
            Element.Image(img)
        ),
        Module.Context(
            Element.Image(icon),
            Element.Text(f'{media} · {date}')
        )
    ))
    return cm
# 函数1【stdcard】标准卡片格式一：最新资讯


def wxgethtml(type: int, title: str = '', onlyurl: boolean = 'true'):
    global wxtitle, wxdate
    url = f'http://weixin.sogou.com/weixin?type={type}&s_from=input&query=Wakfu%E7%9C%9F%E5%A5%BD%E7%8E%A9+{title}&ie=utf8&_sug_=n'
    if onlyurl == 'true':
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.114 Safari/537.36'}
        html = req.get(url, headers=header)
        soup = BeautifulSoup(html.text, 'html.parser')
        if type == 1:
            articletag = soup.find_all(
                'a', attrs={'uigs': 'account_article_0'})[0]
            wxtitle = articletag.string
            date = int(re.findall(
                r"\d+", str(articletag.next_element.next_element))[0])
            wxdate = time.strftime("%Y-%m-%d %H:%M", time.localtime(date))
            return {"date": wxdate, "title": wxtitle}
        if type == 2:
            articletag = soup.find(
                'img', attrs={'onerror': 'errorImage(this)'})['src']
            return f'https:{articletag}'
    else:
        return url
# 函数2【wxgethtml】搜狗微信获取链接


# 系统日志，随便写一个，那就都写吧
logging.getLogger().setLevel(logging.INFO)
logging.basicConfig(level='INFO')

# 万事俱备，机械虫出发！
bot.run()
