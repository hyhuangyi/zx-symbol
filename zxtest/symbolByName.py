import zx.Snowball as ball
import zx.SymbolStore as store
import zx.Sina as sina
import zx.GuoRen as guoRen
import pyttsx3
import time


# 打印评论
def printComment(symbol):
    # 评论
    for i in range(10):
        data = ball.symbolComment(symbol=symbol, page=i + 1)
        for d in data:
            print(d)


def play(symbol='603555'):
    engine = pyttsx3.init()
    engine.setProperty('rate', 250)
    shou = ball.panKou(symbol)[0]['data']['sc1'] / 100
    jia = ball.panKou(symbol)[0]['data']['sp1']
    engine.say(str(jia) + "元," + str(shou) + "手")
    engine.runAndWait()
    engine.stop()
    return jia, shou


kg = True
# kg = False

# 贵州茅台  五粮液   st贵人
# 鸿达兴业  潍柴动力  彩虹股份   徐工机械
name = '鸿达兴业'


if __name__ == '__main__':
    symbol = store.get_symbol_by_name(name)
    if kg:
        # 实时信息
        print(ball.realTimeData(symbol)[1])

        # 主动资金信息
        print(ball.capitalFlow(symbol, count=15)[1])

        # 盘口信息
        print(ball.panKou(symbol)[1])

        # print(guoRen.getGuoRenInfo("跌停")[1])
        # print(str(len(guoRen.getGuoRenInfo("涨停")[0]))+":"+str(len(guoRen.getGuoRenInfo("跌停")[0])))

    else:

        # 评论
        printComment(symbol)

        # 组合持仓
        # print(ball.lookZhHold())

        # 行业情况
        # print(sina.getIndustryInfo())

        # 财报
        # print(ball.getSymbolReport('2021-08-31')[1])
