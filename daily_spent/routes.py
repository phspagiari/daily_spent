#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

from flask import jsonify, request, make_response
from ds import daily, get_info
from . import app


@app.route('/', methods=['GET'])
def index():
    return "Daily Spent"


@app.route('/v1/daily', methods=['POST'])
def daily_route():
    data = json.loads(request.data)
    result = daily(data['spent'], data['reason'])

    if result:
        return make_response(
            jsonify(result),
            200
        )
    return make_response(
        jsonify(result),
        406
    )

@app.route('/v1/logs', methods=['GET'])
def logs():
    result = get_info()
    if result:
        return make_response(
            jsonify(result),
            200
        )
    return make_response(
        jsonify(result),
        406
    )       
