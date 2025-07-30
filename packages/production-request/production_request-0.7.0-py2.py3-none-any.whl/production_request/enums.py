#!/usr/bin/env python
# -*- coding: utf-8 -*-


class SqlOperationEnum(object):
    u"""Типы операций в sql"""
    SELECT = 's'
    INSERT = 'i'
    UPDATE = 'u'
    DELETE = 'd'
    COMMIT = 'c'
    SAVEPOINT = 'sp'
    JOIN = 'j'
    DISTINCT = 'di'
    GROUP_BY = 'gb'

    values = {
        SELECT: 'SELECT',
        INSERT: 'INSERT',
        UPDATE: 'UPDATE',
        DELETE: 'DELETE',
        COMMIT: 'COMMIT',
        SAVEPOINT: 'SAVEPOINT',
        JOIN: 'JOIN',
        DISTINCT: 'DISTINCT',
        GROUP_BY: 'GROUP BY',
    }

    operations = (
        SELECT,
        INSERT,
        UPDATE,
        DELETE,
        COMMIT,
    )

    write_operations = (
        DELETE,
        INSERT,
        UPDATE,
    )

    @classmethod
    def operations_items(cls):
        for key in cls.values:
            if key in cls.operations:
                yield key, cls.values[key]

    @classmethod
    def operators_items(cls):
        return cls.values.items()
