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


name = '安泰科技'
# name = '荃银高科'

if __name__ == '__main__':
    symbol = store.get_symbol_by_name(name)
    # 实时信息
    print(ball.realTimeData(symbol)[1])

    # 主动资金信息
    print(ball.capitalFlow(symbol, count=15)[1])

    # 盘口信息
    print(ball.panKou(symbol)[1])

    # # 评论
    # printComment(symbol)

    # 行业情况
    # print(sina.getIndustryInfo())
