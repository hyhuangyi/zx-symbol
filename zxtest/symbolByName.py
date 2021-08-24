import zx.Snowball as ball
import zx.SymbolStore as store
import zx.Sina as sina


# 打印评论
def printComment(symbol):
    # 评论
    for i in range(10):
        data = ball.symbolComment(symbol=symbol, page=i + 1)
        for d in data:
            print(d)


kg = True
# kg = False
name = '安泰科技'
name = 'st贵人'

if __name__ == '__main__':
    symbol = store.get_symbol_by_name(name)
    if kg:
        # 实时信息
        print(ball.realTimeData(symbol)[1])

        # 主动资金信息
        print(ball.capitalFlow(symbol, count=15)[1])

        # 盘口信息
        print(ball.panKou(symbol)[1])

        # print(ball.getSymbolReport('2021-08-18')[1])
    else:

        # 评论
        printComment(symbol)

        # 组合持仓
        # print(ball.lookZhHold())

        # 行业情况
        # print(sina.getIndustryInfo())
