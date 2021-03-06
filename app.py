import zx.DrawPic as draw
import zx.Snowball as snow
import zx.SymbolStore as store
import const.ZxConsts as const
import util.SysUtil as sysUtil
from flask import Flask, render_template, request

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


@app.route('/v2', methods=['GET', 'POST'])
def v2():
    res = snow.pickSymbols(5, 12, 2, 10, 0.5, 20, 1, 10, 50, 2000, sortBy=1)
    path = draw.draw_table(res, '策略2_高涨幅')
    img_stream = sysUtil.get_img_stream(path)
    return render_template('pick.html',
                           img_stream=img_stream)


@app.route('/v3', methods=['GET', 'POST'])
def v3():
    day = sysUtil.today()
    if sysUtil.is_work():
        store.saveStockHistory(day)
    res = snow.pickSymbolByHistory(day, 5, -10, 10)
    path = draw.draw_table(res, '策略3_年初至今')
    img_stream = sysUtil.get_img_stream(path)
    return render_template('pick.html',
                           img_stream=img_stream)


@app.route('/', methods=['GET', 'POST'])
def home():
    res = snow.pickSymbols()
    path = draw.draw_table(res, '策略1_量价齐升')
    img_stream = sysUtil.get_img_stream(path)
    return render_template('pick.html',
                           img_stream=img_stream)


app.run(threaded=True)
