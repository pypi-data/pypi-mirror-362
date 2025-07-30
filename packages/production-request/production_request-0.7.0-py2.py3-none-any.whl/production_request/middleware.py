#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.conf import (
    settings,
)
from django.utils.deprecation import (
    MiddlewareMixin,
)

from production_request.api import (
    ProductionLogger,
    PRODUCTION_REQUEST_LOGGER,
)
from production_request.utils import (
    generate_uuid,
    CUSTOM_ATTR,
)


class ProductionRequestLoggingMiddleware(MiddlewareMixin):
    """
    Middleware для логирования запросов на production.
    Использует данные из production_request.database.CursorWrapper
    """
    # Атрибуты, не добавляемые в хэдеры
    exclude_attr_headers = ('uuid',)

    def process_request(self, request):
        self._start_log_request(request)

    def process_response(self, request, response):
        is_success = response.status_code == 200
        log_row = self._end_log_request(request, is_success)
        if log_row:
            self._add_response_headers(request, response, log_row)

        return response

    def _start_log_request(self, request):
        """
        Начинает процесс логирования запроса
        """
        request_uuid = request.META.get(
            'HTTP_PR_UUID',
            generate_uuid()
        )
        ProductionLogger(request_uuid).log_start(request)

    def _end_log_request(self, request, is_success):
        """Логирует параметры запроса и результаты обработки"""
        row = None
        try:
            _uuid = request.production_request_uuid
        except AttributeError:
            result = row
        else:
            result = ProductionLogger(_uuid).log_end(request, is_success)

        return result

    def _add_response_headers(self, request, response, log_row):
        if settings.PRODUCTION_REQUEST_LOG_CLIENT:
            try:
                _uuid = request.production_request_uuid
                _started = request.META.get(
                    'HTTP_PR_C_STARTED',
                )

                if _uuid and _started:
                    response['PR-UUID'] = _uuid
                    response['PR-C-STARTED'] = _started

                if log_row:
                    for key, value in log_row.items():
                        if key == CUSTOM_ATTR:
                            value = ','.join(
                                sorted(
                                    [self._create_header(x) for x in value]
                                )
                            )

                        if key not in self.exclude_attr_headers:
                            response[self._create_header(key)] = value

            except Exception as err:
                if settings.PRODUCTION_REQUEST_LOG_SERVER:
                    PRODUCTION_REQUEST_LOGGER.error(
                        json.dumps(
                            {
                                'error': str(err),
                            }
                        )
                    )

    def _create_header(self, attr):
        return 'PR-{}'.format(attr.upper().replace("_", "-"))
