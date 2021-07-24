import time
import zx.DrawPic as draw
import zx.Snowball as ball

if __name__ == '__main__':
    # 流水图
    draw.draw_flow()

    # 词云图
    draw.draw_word_cloud(1)

    # 选股图
    draw.draw_table(ball.pickSymbols(), time.strftime("%Y-%m-%d", time.localtime()) + "_test")
