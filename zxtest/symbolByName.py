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
kg = False

# 鸿达兴业  三元股份   海容冷链   紫光股份
name = '诺德股份'


if __name__ == '__main__':
    symbol = store.get_symbol_by_name(name)
    if kg:
        # 实时信息
        print(ball.realTimeData(symbol)[1])

        # 主动资金信息
        print(ball.capitalFlow(symbol, count=15)[1])

        # 盘口信息
        print(ball.panKou(symbol)[1])
        # print(ball.pickSymbols(2, 5, 1.2, 10, 1, 20,
        #                        3, 20, 50, 1000, sortBy=2))


        # 财报
        # print(ball.getSymbolReport('2021-10-30')[1])

        # print(guoRen.getGuoRenInfo("跌停")[1])
        # print(str(len(guoRen.getGuoRenInfo("涨停")[0]))+":"+str(len(guoRen.getGuoRenInfo("跌停")[0])))

    else:
        # 评论
        printComment(symbol)

        # print(ball.getSymbolReport('2022-08-11',sortBy=2)[1])

        # 组合持仓
        # print(ball.lookZhHold())

        # 行业情况
        # print(sina.getIndustryInfo())


