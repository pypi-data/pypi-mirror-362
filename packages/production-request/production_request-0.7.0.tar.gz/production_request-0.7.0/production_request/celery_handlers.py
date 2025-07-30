#!/usr/bin/env python
# -*- coding: utf-8 -*-
from celery.signals import (
    task_failure,
    task_prerun,
    task_success,
)
from celery.utils.dispatch import (
    Signal,
)
from production_request.api import (
    ProductionLogger,
)
from production_request.utils import (
    generate_uuid,
)


def on_task_prerun(sender=None, task_id=None, task=None, args=None, kwargs=None, **kw):
    if task:
        logger = ProductionLogger(generate_uuid())
        logger.log_start(task)
        production_request_task_prerun.send(
            sender,
            task_id=task_id,
            task=task,
            args=args,
            kwargs=kwargs,
        )


def on_task_success(sender=None, result=None, **kw):
    on_task_end(sender, True)


def on_task_failure(
    sender=None, task_id=None, exception=None, args=None, kwargs=None, traceback=None, einfo=None, **kw
):
    on_task_end(sender, False)


def on_task_end(task, is_success):
    if task:
        try:
            _uuid = task.production_request_uuid
        except AttributeError:
            pass
        else:
            ProductionLogger(_uuid).log_end(task, is_success)


task_prerun.connect(on_task_prerun)
task_success.connect(on_task_success)
task_failure.connect(on_task_failure)


production_request_task_prerun = Signal()
