from schedule import every, run_pending
from time import sleep
from datetime import datetime, time as dt_time
from logging import getLogger, INFO, info
from app.src.run import job


logger = getLogger()
logger.setLevel(INFO)

START = dt_time(5, 0)
END = dt_time(20, 0) 

def limited_job():
    now = datetime.now()
    if START <= now.time() <= END:
        info(f'Podejmowanie działania: {now}')
        job()


def run():
    every(10).minutes.do(limited_job)
    while True:
        run_pending()
        sleep(1)


if __name__ == "__main__":
    run()
