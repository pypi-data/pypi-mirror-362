#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import sys
import time
from datetime import (
    datetime,
)

import psutil

from production_request.utils import (
    register_logger,
    to_MB,
)


PRODUCTION_REQUEST_PROCESSES_LOGGER = register_logger(
    'production_request_processes',
    formatter=logging.Formatter("%(message)s"))


def get_processes(process_name):
    """Возвращает все процессы, которые содержат указанное имя"""
    for process in psutil.process_iter():
        if process_name in process.name():
            yield process


def log_process(process):
    """Логирует процесс"""
    memory_info = process.memory_full_info()

    row = {
        'pid': str(process.pid),
        'timestamp': str(datetime.now()),
        'cpu': '{:.2f}'.format(process.cpu_percent()),
        'uss': '{:.2f}'.format(to_MB(memory_info.uss)),
        'pss': '{:.2f}'.format(to_MB(memory_info.pss)),
        'swap': '{:.2f}'.format(to_MB(memory_info.swap)),
        'rss': '{:.2f}'.format(to_MB(memory_info.rss)),
    }
    PRODUCTION_REQUEST_PROCESSES_LOGGER.info(row)


def log_processes(process_name):
    for process in get_processes(process_name):
        log_process(process)


def loop(process_name, loop_period):
    """Основной цикл приложения"""
    start_time = time.time()
    loop_period = float(loop_period)

    while True:
        log_processes(process_name)
        time.sleep(loop_period - ((time.time() - start_time) % loop_period))


if __name__ == '__main__':
    loop(*sys.argv[1:])