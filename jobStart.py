import zx.Scheduler as job
from apscheduler.schedulers.blocking import BlockingScheduler


def jobs():
    print("启动job")
    scheduler = BlockingScheduler()
    # 每天3点05分跑
    scheduler.add_job(job.save_stock_day, 'cron', hour='15', minute='01')
    scheduler.start()


if __name__ == '__main__':
    jobs()
