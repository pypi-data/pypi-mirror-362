#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging
import uuid
import os
from logging.handlers import (
    TimedRotatingFileHandler,
)
from collections import (
    defaultdict,
)
from contextlib import (
    contextmanager,
)
from datetime import (
    datetime,
)
from threading import (
    local,
)

from django.conf import (
    settings,
)

from production_request.enums import (
    SqlOperationEnum,
)


_t_locals = local()
CUSTOM_ATTR = 'custom'


class ProductionRequestData(object):

    def __init__(self):
        super(ProductionRequestData, self).__init__()
        self.sql_time = defaultdict(float)
        self.async_sql_time_start = {}
        self.async_sql_time_total = {}
        self.sql_count = defaultdict(int)
        self.sql_uniq_hashes = defaultdict(set)
        self.sql_db_aliases = set()
        self.async_sql_count = defaultdict(int)

    def has_write_queries(self):
        """
        Проверка на наличие в данных потока пишущих SQL-запросов
        """
        return any(
            getattr(self, 'sql_{}_count'.format(operation))
            for operation in SqlOperationEnum.write_operations
            if hasattr(self, 'sql_{}_count'.format(operation))
        )


def get_thread_data():
    """Возвращает thread-данные"""
    if not hasattr(_t_locals, 'production_request_data'):
        _data = ProductionRequestData()
        _t_locals.production_request_data = _data

    return _t_locals.production_request_data


def clear_thread_data():
    """Очищает данные в треде"""
    if hasattr(_t_locals, 'production_request_data'):
        del _t_locals.production_request_data


def add_custom_attr_to_thread_data(attr, value):
    """Добавляет кастомный атрибут в thread-данные"""
    data = get_thread_data()

    if not hasattr(data, CUSTOM_ATTR):
        setattr(data, CUSTOM_ATTR, {})

    getattr(data, CUSTOM_ATTR)[attr] = value


def get_custom_attrs_from_thread_data():
    """Возвращает кастомные атрибуты из thread-данных"""
    data = get_thread_data()

    return getattr(data, CUSTOM_ATTR, {}).items()


def ms_from_timedelta(td):
    """
    Получает дельту, возвращает миллисекунды
    """
    return (td.seconds * 1000) + (td.microseconds / 1000.0)


@contextmanager
def calc_sql_metrics(cursor, sql):
    """
    Контекстный менеджер для подсчета времени выполнения SQL-запроса
    """
    start = datetime.now()

    yield

    thread_data = get_thread_data()
    request_uuid = getattr(thread_data, 'production_request_uuid', None)

    if request_uuid:
        # подсчет времени выполнения sql-запроса
        duration = ms_from_timedelta(datetime.now() - start)
        thread_data.sql_time[request_uuid] += duration

        for key, operation in SqlOperationEnum.operations_items():
            if operation in sql:
                sql_operation_attr = 'sync_sql_{}_total'.format(key)

                if not hasattr(thread_data, sql_operation_attr):
                    setattr(
                        thread_data, sql_operation_attr,
                        defaultdict(type(duration))
                    )

                getattr(thread_data, sql_operation_attr)[request_uuid] += duration

                break

        # подсчет количества sql-запросов
        thread_data.sql_count[request_uuid] += 1

        # коллекция хэшей уникальных запросов
        thread_data.sql_uniq_hashes[request_uuid].add(hash(sql))

        # подсчет количества sql-операторов определенного типа
        for key, operator in SqlOperationEnum.operators_items():
            count = sql.count(operator)
            if not count:
                continue

            sql_operator_attr = 'sync_sql_{}_count'.format(key)

            if not hasattr(thread_data, sql_operator_attr):
                setattr(thread_data, sql_operator_attr, defaultdict(int))

            getattr(thread_data, sql_operator_attr)[request_uuid] += count

        # запоминаем базу, в которую прошел запрос
        thread_data.sql_db_aliases.add(cursor.db.alias)


def calc_async_sql_metrics(sql):
    """
    Метод перехватывает асинхронно выполняющиеся запросы и разбирает их для статистики
    """
    thread_data = get_thread_data()
    request_uuid = getattr(thread_data, 'production_request_uuid', None)

    if request_uuid:
        # подсчет количества sql-запросов
        thread_data.async_sql_count[request_uuid] += 1

        # подсчет количества sql-операторов определенного типа
        for key, operator in SqlOperationEnum.operators_items():
            count = sql.count(operator)
            if not count:
                continue

            sql_operator_attr = f'async_sql_{key}_count'

            if not hasattr(thread_data, sql_operator_attr):
                setattr(thread_data, sql_operator_attr, defaultdict(int))

            getattr(thread_data, sql_operator_attr)[request_uuid] += count


def start_metric_timer_for_async_pool():
    """
    Метод фиксирует время открытия Pool для asyncpg
    """
    thread_data = get_thread_data()
    request_uuid = getattr(thread_data, 'production_request_uuid', None)
    thread_data.async_sql_time_start[request_uuid] = datetime.now()


def stop_metric_timer_for_async_pool():
    """
    Метод фиксирует время закрытия Pool для asyncpg
    """
    thread_data = get_thread_data()
    request_uuid = getattr(thread_data, 'production_request_uuid', None)
    async_sql_time_total = ms_from_timedelta(datetime.now() - thread_data.async_sql_time_start[request_uuid])
    thread_data.async_sql_time_total[request_uuid] = async_sql_time_total


@contextmanager
def calc_transaction_metrics(autocommit):
    data = get_thread_data()
    request_uuid = getattr(data, 'production_request_uuid', None)
    if request_uuid:
        if not hasattr(data, 'transaction_timestamps'):
            data.transaction_timestamps = defaultdict(list)

        if not autocommit:
            data.transaction_timestamps[request_uuid].append(datetime.now())

    yield

    if request_uuid and autocommit:
        now = datetime.now()
        if not hasattr(data, 'transaction_timestamps'):
            data.transaction_timestamps = defaultdict(list)
        else:
            try:
                timestamp = data.transaction_timestamps[request_uuid].pop()
            except IndexError:
                pass
            else:
                if not hasattr(data, 'transaction_count'):
                    data.transaction_count = defaultdict(int)
                data.transaction_count[request_uuid] += 1

                if not hasattr(data, 'transaction_total'):
                    data.transaction_total = defaultdict(float)
                data.transaction_total[request_uuid] += ms_from_timedelta(
                    now - timestamp)


def get_client_ip(request):
    """
    Возвращает IP-адрес клиента, от которого пришел запрос
    """
    if hasattr(request, 'META'):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR', '')
    else:
        ip = ''

    return ip


def register_logger(
        lname, log_file=None, log_level=logging.INFO, formatter=None):
    """
    Регистрирует логгер
    """
    log_file = log_file or u'{0}.log'.format(lname)
    log_dir = settings.LOG_PATH
    log_path = os.path.join(log_dir, log_file)

    if formatter is None:
        formatter = logging.Formatter(
            "\n%(pathname)s:%(lineno)d\n[%(asctime)s] %(levelname)s: "
            "%(message)s")
    formatter.datefmt = '%Y-%m-%d %H:%M:%S'

    l = logging.getLogger(lname)
    l.setLevel(log_level)

    # Защита от reload()
    if not l.handlers:
        handler = TimedRotatingFileHandler(
            log_path, when='D', encoding='utf-8')
        handler.setFormatter(formatter)
        l.addHandler(handler)

    return l


def to_MB(value):
    """Приводит биты в МБ"""
    return value / 1024.0 / 1024.0


class SimpleRequest(object):
    def __init__(self, path=''):
        super(SimpleRequest, self).__init__()
        self.path = path


def generate_uuid():
    return str(uuid.uuid4())[-12:]