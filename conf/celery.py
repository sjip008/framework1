# coding: utf-8
from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from django.conf import settings
import home_application.celeryconfig

# 单独脚本调用Django内容时，需配置脚本的环境变量
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')

app = Celery('config')

#  CELERY_ 作为前缀，在settings中写配置
# app.config_from_object(home_application.celeryconfig)

# app 扩展配置
app.conf.update(
    result_expires=3600,
    BROKER_URL='redis://192.168.243.129:6379/1',
    CELERY_RESULT_BACKEND='redis://192.168.243.129:6379/2',
    task_serializer='json',
    result_serializer='json',
    timezone='Asia/Shanghai',
)

# 到Django各个app下，自动发现tasks.py 任务脚本
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))
