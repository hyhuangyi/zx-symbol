import zx.Snowball as ball
import zx.SymbolStore as store
import zx.Sina as sina
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

name = '陕西黑猫'
# name = '天下秀'

if __name__ == '__main__':
    symbol = store.get_symbol_by_name(name)
    if kg:
        # 实时信息
        print(ball.realTimeData(symbol)[1])

        # 主动资金信息
        print(ball.capitalFlow(symbol, count=15)[1])

        # 盘口信息
        print(ball.panKou(symbol)[1])

        # print(ball.getSymbolReport('2021-08-31')[1])
    else:

        # 评论
        printComment(symbol)

        # 组合持仓
        # print(ball.lookZhHold())

        # 行业情况
        # print(sina.getIndustryInfo())

    # while 1:
    #     # time.sleep(2)
    #     print(play('600176'))
