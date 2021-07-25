import zx.DrawPic as draw
import zx.Snowball as ball

date = '2021-07-23'

if __name__ == '__main__':
    # 流水图
    draw.draw_flow()

    # 词云图
    draw.draw_word_cloud(1)

    # 选股图
    draw.draw_table(ball.pickSymbols(), "pickSymbols_test")

    # 年初至今亏损 当日大涨图
    draw.draw_table(ball.pickSymbolByHistory(date), "pickSymbolByHistory_test")

    # 龙虎榜图
    draw.draw_table(ball.longHuBang(date)[1], "龙虎榜")
