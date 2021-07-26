import zx.Snowball as ball
import util.SysUtil as sysUtil

date = sysUtil.today()
symbol = '300418'

if __name__ == '__main__':
    # 实时信息
    print(ball.realTimeData(symbol)[1])

    # 主动资金信息
    print(ball.capitalFlow(symbol)[1])

    # 盘口信息
    print(ball.panKou(symbol)[1])

    # 成交分布
    print(ball.capitalAssort(symbol)[1])

    # 龙虎榜
    print(ball.longHuBang(date)[1])

    # 年初至今
    print(ball.pickSymbolByHistory(date))

    # 选股
    print(ball.pickSymbols(2, 5, 1.2, 10, 1, 20,
                           3, 20, 50, 1000, sortBy=2))
