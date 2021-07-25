import time
import util.SysUtil as sysUtil
import zx.SymbolStore as store


# 输出时间
def save_stock_day():
    if sysUtil.is_work():
        start = time.time()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + " 开始执行任务")
        store.saveStockHistory()
        print("任务执行结束:用时" + str(round(time.time() - start, 2)) + "秒")


