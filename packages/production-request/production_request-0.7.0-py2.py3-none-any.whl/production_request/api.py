#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import logging
import socket
from datetime import (
    datetime,
)
from psutil import (
    Process,
)

from django.conf import (
    settings,
)

from production_request.enums import (
    SqlOperationEnum,
)
from production_request.utils import (
    clear_thread_data,
    CUSTOM_ATTR,
    generate_uuid,
    get_client_ip,
    get_custom_attrs_from_thread_data,
    get_thread_data,
    ms_from_timedelta,
    register_logger,
    SimpleRequest,
    to_MB,
)

PRODUCTION_REQUEST_LOGGER = register_logger(
    'production_request',
    formatter=logging.Formatter("%(message)s"))

PRODUCTION_REQUEST_ENTER_LOGGER = register_logger(
    'production_request_enter',
    formatter=logging.Formatter("%(message)s"))


class ProductionLogger(object):
    def __init__(self, uuid_):
        super(ProductionLogger, self).__init__()
        self.uuid = uuid_

    def log_start(self, request):
        """Начинает процесс логирования объекта"""
        request.production_request_uuid = self.uuid

        if settings.PRODUCTION_REQUEST:
            thread_data = get_thread_data()
            thread_data.production_request_uuid = self.uuid
            thread_data.production_request_original_path = self.get_path(request)

            request.started_at = datetime.now()

            if settings.PRODUCTION_REQUEST_LOG_MEMORY:
                memory = self.get_memory_info()

                request.production_request_uss = memory.uss
                request.production_request_pss = memory.pss
                request.production_request_swap = memory.swap
                request.production_request_rss = memory.rss

        if settings.PRODUCTION_REQUEST_LOG_ENTER:
            self.log_enter(self.uuid, self.get_path(request))

    def log_end(self, request, is_success):
        """Логирует параметры запроса и результаты обработки"""
        row = None

        if settings.PRODUCTION_REQUEST:
            try:
                thread_data = get_thread_data()

                process_request_time = ms_from_timedelta(
                    datetime.now() - request.started_at
                )
                process_sql_time = thread_data.sql_time.pop(
                    request.production_request_uuid, float())
                sync_sql_total = '{:.4f}'.format(process_sql_time)

                process_async_sql_time = thread_data.async_sql_time_total.pop(
                    request.production_request_uuid, float()
                )
                async_sql_total = '{:.4f}'.format(process_async_sql_time)

                sql_total = '{:.4f}'.format(process_sql_time + process_async_sql_time)

                sync_sql_count = thread_data.sql_count.pop(
                    request.production_request_uuid, 0)

                async_sql_count = thread_data.async_sql_count.pop(
                    request.production_request_uuid, 0)

                sql_duplicate_count = sync_sql_count - len(
                    thread_data.sql_uniq_hashes.pop(
                        request.production_request_uuid,
                        set()
                    )
                )

                user = getattr(request, 'user', None)
                user_id = user.id if user else ''

                path = self.get_path(request, thread_data)

                if hasattr(thread_data, 'transaction_count'):
                    transaction_count = thread_data.transaction_count[
                        request.production_request_uuid]
                else:
                    transaction_count = 0

                if hasattr(thread_data, 'transaction_total'):
                    transaction_total = thread_data.transaction_total[
                        request.production_request_uuid]
                else:
                    transaction_total = 0.0

                db_aliases = ', '.join(sorted(thread_data.sql_db_aliases))

                row = {
                    'uuid': self.uuid,
                    'is_success': json.dumps(is_success),
                    'started': str(request.started_at),
                    'path': path,
                    'user': str(user_id or ''),
                    'hostname': socket.gethostname(),
                    'total': '{:.4f}'.format(process_request_time),
                    'sql_total': sql_total,
                    'sync_sql_total': sync_sql_total,
                    'async_sql_total': async_sql_total,
                    'sql_count': str(sync_sql_count + async_sql_count),
                    'sync_sql_count': str(sync_sql_count),
                    'async_sql_count': str(async_sql_count),
                    'sql_duplicate_count': str(sql_duplicate_count),
                    'sql_transaction_count': str(transaction_count),
                    'sql_transaction_total': '{:.4f}'.format(transaction_total),
                    'sql_db_aliases': db_aliases,
                    'client_ip': get_client_ip(request),
                    'pid': str(os.getpid()),
                }

                # количество и время sql-запросов в разрезе типов
                for operator in SqlOperationEnum.values:
                    attrs = ['sync_sql_{}_count'.format(operator)]
                    attrs.extend(['async_sql_{}_count'.format(operator)])

                    if operator in SqlOperationEnum.operations:
                        attrs.append('sync_sql_{}_total'.format(operator))

                    for operator_attr in attrs:
                        counter = getattr(
                            thread_data,
                            operator_attr,
                            {}
                        )
                        _value = counter.pop(
                            request.production_request_uuid,
                            0
                        )
                        if isinstance(_value, float):
                            _value = '{:.4f}'.format(_value)
                        else:
                            _value = str(_value)

                        row[operator_attr] = _value

                # добавляем кастомные значения к общему результату
                row[CUSTOM_ATTR] = []
                for attr, value in get_custom_attrs_from_thread_data():
                    key = CUSTOM_ATTR + '_' + attr
                    row[CUSTOM_ATTR].append(key)
                    row[key] = str(value)

                if settings.PRODUCTION_REQUEST_LOG_MEMORY:
                    memory = self.get_memory_info()

                    row['uss'] = '{:.2f}'.format(
                        self.get_memory_diff(
                            request.production_request_uss,
                            memory.uss
                        )
                    )
                    row['pss'] = '{:.2f}'.format(
                        self.get_memory_diff(
                            request.production_request_pss,
                            memory.pss
                        )
                    )
                    row['swap'] = '{:.2f}'.format(
                        self.get_memory_diff(
                            request.production_request_swap,
                            memory.swap
                        )
                    )
                    row['rss'] = '{:.2f}'.format(
                        self.get_memory_diff(
                            request.production_request_rss,
                            memory.rss
                        )
                    )

                if settings.PRODUCTION_REQUEST_LOG_SERVER:
                    PRODUCTION_REQUEST_LOGGER.info(
                        json.dumps(row)
                    )
            except Exception as err:
                if settings.PRODUCTION_REQUEST_LOG_SERVER:
                    PRODUCTION_REQUEST_LOGGER.error(
                        json.dumps(
                            {
                                'error': str(err),
                            }
                        )
                    )

        if settings.PRODUCTION_REQUEST_LOG_ENTER:
            self.log_exit(self.uuid, self.get_path(request))

        clear_thread_data()

        return row

    def get_path(self, request, thread_data=None):
        """Возвращает параметр path."""

        if hasattr(thread_data, 'production_request_original_path'):
            path = thread_data.production_request_original_path
        elif hasattr(request, 'path'):
            path = request.path
        else:
            path = getattr(request, 'name', '')

        return path

    def get_memory_info(self):
        """Возвращает данные о памяти процесса"""
        return Process(os.getpid()).memory_full_info()

    def get_memory_diff(self, m_begin, m_end):
        """Возвращает разницу размера памяти в МБ"""
        return to_MB((m_end - m_begin))

    def log_enter(self, request_uuid, request_path):
        """Логирует момент входа объекта в приложение"""
        self.log_state('enter', request_uuid, request_path)

    def log_exit(self, request_uuid, request_path):
        """Логирует момент выхода запроса в приложение"""
        self.log_state('exit', request_uuid, request_path)

    def log_state(self, state, request_uuid, request_path):
        """Логирует определенный момент запроса"""
        PRODUCTION_REQUEST_ENTER_LOGGER.info(
            json.dumps(
                {
                    'uuid': request_uuid,
                    'path': request_path,
                    'state': state,
                    'pid': os.getpid(),
                    'timestamp': str(datetime.now()),
                }
            )
        )


def production_request(path=''):

    def decorator(func):

        def wrapper(*args, **kwargs):
            request = SimpleRequest(path=path)
            logger = ProductionLogger(generate_uuid())

            logger.log_start(request)
            is_success = True
            try:
                result = func(*args, **kwargs)
            except:
                is_success = False
                raise
            finally:
                logger.log_end(request, is_success)

            return result

        return wrapper

    return decorator




