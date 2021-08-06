import zx.Snowball as ball
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
from PIL import Image, ImageDraw, ImageFont
import const.ZxConsts as const
import util.SysUtil as sysUtil


# 词云图 type 1：大涨 2：大跌
def draw_word_cloud(type=1):
    basePath = sysUtil.download_path()
    resList = ball.getAllRealTimeSymbols()
    arr = ''
    for l in resList:
        name = l['name']
        percent = l['percent'] if l['percent'] is not None else 0
        if '退' not in l['name'] or '*ST' not in l['name']:
            if 9.8 < percent and type == 1:
                arr += ' ' + name
            elif percent < -9.8 and type == 2:
                arr += ' ' + name
            elif type != 1 and type != 2:
                raise Exception("type请传1-2")
    wordCloud = WordCloud(width=1000,  # 图片的宽度
                          height=860,  # 高度
                          margin=2,  # 边距
                          background_color='black',  # 指定背景颜色
                          font_path=const.word_cloud_font_path
                          # 指定字体文件，要有这个字体文件，自己随便想用什么字体，就下载一个，然后指定路径就ok了
                          )
    wordCloud.generate(arr)
    if type == 1:
        fName = basePath + 'up.png'
    else:
        fName = basePath + 'down.png'
    wordCloud.to_file(fName)  # 保存到图片
    return fName


# pretty table表格转化成图片
def draw_table(tab_info, name):
    basePath = sysUtil.download_path()
    space = 5
    # PIL模块中，确定写入到图片中的文本字体
    # ubuntu
    # font = ImageFont.truetype('/home/doge/YaHeiConsolas.ttf', 15, encoding='utf-8')
    # windows
    font = ImageFont.truetype(const.table_font_path, 15, encoding='utf-8')
    # Image模块创建一个图片对象
    im = Image.new('RGB', (10, 10), (0, 0, 0, 0))
    # ImageDraw向图片中进行操作，写入文字或者插入线条都可以
    draw = ImageDraw.Draw(im, "RGB")
    # 根据插入图片中的文字内容和字体信息，来确定图片的最终大小
    img_size = draw.multiline_textsize(tab_info, font=font)
    # 图片初始化的大小为10-10，现在根据图片内容要重新设置图片的大小
    im_new = im.resize((img_size[0] + space * 2, img_size[1] + space * 2))
    del draw
    del im
    draw = ImageDraw.Draw(im_new, 'RGB')
    # 批量写入到图片中，这里的multiline_text会自动识别换行符
    # python2
    # draw.multiline_text((space,space), unicode(tab_info, 'utf-8'), fill=(255,255,255), font=font)
    # python3
    draw.multiline_text((space, space), tab_info, fill=(255, 255, 255), font=font)
    fName = basePath + name + ".png"
    im_new.save(fName, "PNG")
    del draw
    return fName


# 画折线图 tick_spacing 密度  count 取数数量 type 1分钟级别 2日级别
def draw_flow(symbol=const.default_symbol, tick_spacing=10, count=15, type=1, ifShow=False):
    basePath = sysUtil.download_path()
    arr = ball.capitalFlow(symbol, count, type)[0]
    x = []
    y = []
    for r in arr:
        y.append(r['amount'])
        x.append(r['timestamp'])
    # 创建绘图对象
    fig = plt.figure(figsize=(25, 15))
    ax = fig.add_subplot(111)
    # 在当前绘图对象绘图（X轴，Y轴，蓝色虚线，线宽度）
    plt.plot(x, y, "c--", linewidth=3)
    # x轴密度
    ax.xaxis.set_major_locator(ticker.MultipleLocator(tick_spacing))
    # X轴标签
    plt.xlabel("time", fontsize=40)
    # Y轴标签
    plt.ylabel("amount", fontsize=40)
    # 图标题
    plt.title("flow")
    # 设置刻度的大小,both代表xy同时设置
    plt.tick_params(axis='both', labelsize=36)
    # y轴画0刻度线
    plt.axhline(0.00, color='r', linestyle='--', label='plane')
    plt.legend(loc='upper left')
    # 保存
    fName = basePath + symbol + ".png"
    plt.savefig(fName)
    # 显示图
    if ifShow:
        plt.show()
    return fName
