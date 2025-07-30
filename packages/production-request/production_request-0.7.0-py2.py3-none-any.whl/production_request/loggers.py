#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from production_request.utils import (
    register_logger,
)


PRODUCTION_REQUEST_CLIENT_LOGGER = register_logger(
    'production_request_client',
    formatter=logging.Formatter("%(message)s"))