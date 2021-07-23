import comm.snowball as ball

percent_pre = 5
percent_post = 10
volume_ratio_pre = 2
volume_ratio_post = 10
amount_pre = 3
amount_post = 20
turnover_rate_pre = 3
turnover_rate_post = 20
market_capital_pre = 50
market_capital_post = 1000

if __name__ == '__main__':
    symbol = '300418'

    # 实时信息
    # print(ball.realTimeData(symbol)[1])

    # 主动资金信息
    # print(ball.capitalFlow(symbol)[1])

    # 盘口信息
    # print(ball.panKou(symbol)[1])

    # 流水图
    # ball.draw_flow(symbol)

    # 成交分布
    # print(ball.capitalAssort(symbol)[1])

    # 词云图
    # ball.draw_word_cloud(1)

    tb = ball.pickSymbols(percent_pre, percent_post, volume_ratio_pre, volume_ratio_post, amount_pre, amount_post,
                          turnover_rate_pre, turnover_rate_post, market_capital_pre, market_capital_post)
    print(tb)
