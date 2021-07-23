from flask import Flask, render_template, request
import zx.snowball as snow
import const.ZxConsts as const
import util.SysUtil as sysUtil
import time

app = Flask(__name__)


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


@app.route('/', methods=['GET', 'POST'])
def home():
    day = time.strftime("%Y-%m-%d", time.localtime())
    res = snow.pickSymbols()
    path = snow.draw_table(res, day + '_zf_lb_ln_hs_sz')
    img_stream = sysUtil.get_img_stream(path)
    return render_template('pick.html',
                           img_stream=img_stream)


app.run()
