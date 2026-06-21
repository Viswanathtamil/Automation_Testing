from datetime import timedelta
import datetime
from django.db import close_old_connections
from Automation.settings import logger
from automationservice.controller.backgroundschedular import BackgroundScheduler
from django import db
from automationservice.service.runservice import runserv


def automation_schedular(testcasecode,client,testcase_id,user_id):
    current_time = datetime.datetime.now() + timedelta(seconds=5)
    sched = BackgroundScheduler()
    h=current_time.hour
    m=current_time.minute
    s=current_time.second
    logger.info('trigger scheduler')
    sched.add_job(db_scheduler_process, 'cron',hour=h,minute=m,second =s,args=[testcasecode,client,testcase_id,user_id])
    sched.start()
    return [{"key": "Automation Starts"}]


def db_scheduler_process(testcasecode,client,testcase_id,user_id):
    try:
        logger.info('triggered fileinsert')
        runserv().runprocess(testcasecode,client,testcase_id,user_id)
    except Exception as e:
        logger.info('db_scheduler_process' + str(e))
        print(str(e))
    finally:
        # db.connections['scheduler'].close()
        close_old_connections()
    return
