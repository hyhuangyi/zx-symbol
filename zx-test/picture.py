import time
import zx.snowball as ball

if __name__ == '__main__':
    symbol = '300418'

    # 流水图
    ball.draw_flow(symbol)

    # 词云图
    ball.draw_word_cloud(1)

    ball.draw_table(ball.pickSymbols(), time.strftime("%Y-%m-%d", time.localtime())+"_test")
