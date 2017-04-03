#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging

from flask import Flask

app = Flask(__name__, static_url_path="")

# Setup logging
_log_handler = logging.StreamHandler()
_log_handler.setLevel(logging.INFO)
app.logger.addHandler(_log_handler)

# Register views/routes
from . import routes
