import time
import zx.Snowball as snow
import util.SysUtil as sysUtil
import util.DingdingNotifyUtil as notifyUtil

codes = '000858,002185'
time_sleep = 5

if __name__ == '__main__':

    while 1:
        # 日期
        day = sysUtil.today()
        # 文件地址
        path = sysUtil.download_path()+"record.txt"
        f = open(path, 'a+')
        # 时间戳
        timStr = time.strftime("%H:%M:%S", time.localtime())
        time.sleep(int(time_sleep))
        arr = snow.realTimeData(codes)[0]
        res = []
        for r in arr:
            symbol = r['symbol']
            percent = r['percent']
            if abs(percent) > 3:
                notifyUtil.send_ding_message(symbol + "-->" + str(percent) + "%", False)
            res.append(symbol + '->' + str(percent))
        print(res)
        # sysUtil.play_symbols(arr)
        # 存到文件
        if sysUtil.is_trade_time():
            print(timStr, res, file=f)
