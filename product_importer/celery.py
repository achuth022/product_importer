from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'product_importer.settings')

app = Celery('product_importer')

# Use Redis Cloud as the broker and result backend
app.conf.broker_url = 'redis://default:ppQsL9nMnXnJUMV4pkGMGyh3GHRuZnDF@redis-10235.c84.us-east-1-2.ec2.cloud.redislabs.com:10235'
app.conf.result_backend = 'redis://default:ppQsL9nMnXnJUMV4pkGMGyh3GHRuZnDF@redis-10235.c84.us-east-1-2.ec2.cloud.redislabs.com:10235'

app.autodiscover_tasks()



