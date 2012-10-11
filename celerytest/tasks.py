from celery import task, Task
from celery.registry import tasks
from celery.task.sets import TaskSet
from celery.exceptions import TaskRevokedError
from django.db.models import Q
from celerytest.models import SimpleEntry, ContentProducer, \
                                SimpleUser
from celery.utils.log import get_task_logger
from datetime import datetime, timedelta

from time import sleep

logger = get_task_logger(__name__)

@task()
def send_sms(text, user):
    logger.info('Running SMS sender')
    SimpleEntry(body='Sending "{0}" to {1} ({2})'.format(text, user.phone_number, user.name)).save()

class ContentProducerTask(Task):
    def run(self, content_producer_pk):
        content = ContentProducer.objects.get(pk=content_producer_pk)
        self.text = content.text_body
        conditions = content.conditions.all()
        end_execution = datetime.now() + timedelta(seconds=15)

        users = SimpleUser.objects.all()
        # Build the query with the given conditions
        for condition in conditions:
            filters = Q(**{condition.field: condition.value})
            users = users.filter(filters)

        jobs = TaskSet(tasks=[send_sms.subtask((content.text_body, user,), expires=end_execution) for user in users])
        jobs.apply_async()

        # Check for time limit exceeded
        # Then, revoke evey task waiting for execution

tasks.register(ContentProducerTask)
