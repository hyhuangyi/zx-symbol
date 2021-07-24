import zx.DrawPic as draw
import zx.Snowball as ball
import util.SysUtil as sysUtil

if __name__ == '__main__':
    # 流水图
    draw.draw_flow()

    # 词云图
    draw.draw_word_cloud(1)

    # 选股图
    draw.draw_table(ball.pickSymbols(), sysUtil.today() + "_test")

    # 龙虎榜图
    draw.draw_table(ball.longHuBang('2021-07-23')[1], sysUtil.today() + "_龙虎榜")
