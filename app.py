import time
import zx.DrawPic as draw
import zx.Scheduler as job
import zx.Snowball as snow
import const.ZxConsts as const
import util.SysUtil as sysUtil
from flask import Flask, render_template, request
from apscheduler.schedulers.blocking import BlockingScheduler

app = Flask(__name__)


def jobs():
    scheduler = BlockingScheduler()
    # 每天3点05分跑
    scheduler.add_job(job.save_stock_day, 'cron', hour='15', minute='05')
    scheduler.start()


@app.route('/v1', methods=['GET', 'POST'])
def v1():
    stop = request.args.get("stop")
    codes = const.default_symbol
    if stop is None:
        stop = 0
    arr = snow.realTimeData(codes)[0]
    res = []
    for r in arr:
        symbol = r['symbol']
        percent = r['percent']
        avg_price = round(r['avg_price'], 2)
        plv = r['plv']
        res.append(symbol + '->' + str(percent) + ' === avg：' + str(avg_price) + ' 偏离率：' + str(plv))
    return render_template("./symbol.html", res=res, stop=int(stop))


@app.route('/v2', methods=['GET', 'POST'])
def v2():
    day = time.strftime("%Y-%m-%d", time.localtime())
    res = snow.pickSymbols(5, 10, 2, 10, 0.5, 20, 1, 10, 50, 2000)
    path = draw.draw_table(res, day + '策略2_高涨幅')
    img_stream = sysUtil.get_img_stream(path)
    return render_template('pick.html',
                           img_stream=img_stream)


@app.route('/', methods=['GET', 'POST'])
def home():
    day = time.strftime("%Y-%m-%d", time.localtime())
    res = snow.pickSymbols()
    path = draw.draw_table(res, day + '策略1_量价齐升')
    img_stream = sysUtil.get_img_stream(path)
    return render_template('pick.html',
                           img_stream=img_stream)


if __name__ == "__main__":
    app.run()
    jobs()
