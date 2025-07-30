#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from django.conf import (
    settings,
)
from django.http.response import (
    HttpResponse,
)

from production_request.loggers import (
    PRODUCTION_REQUEST_CLIENT_LOGGER,
)


def save_client_log(request):
    """
    Сохраняет собранные данные с клиента в лог
    """
    if request.user.is_authenticated and settings.PRODUCTION_REQUEST_LOG_CLIENT:
        logs = request.POST.get('logs', '[]')
        for log_str in json.loads(logs):
            PRODUCTION_REQUEST_CLIENT_LOGGER.info(json.dumps(log_str))
        success = True
    else:
        success = False

    response = HttpResponse(
        json.JSONEncoder().encode({
            'message': '',
            'success': success
        })
    )

    return response