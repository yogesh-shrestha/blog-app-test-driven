# works only on Linux..need a message broker (e.g. Redis, RabbitMQ)

import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_test_driven.settings.dev')
celery_app = Celery('blog_test_driven')
celery_app.config_from_object('django.conf:settings', namespace='CELERY')
celery_app.autodiscover_tasks()

