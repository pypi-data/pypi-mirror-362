#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.urls import (
    re_path,
)
from production_request.views import (
    save_client_log,
)


production_request_url = re_path(r'^production-request', save_client_log)
