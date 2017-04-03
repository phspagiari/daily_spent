#!/usr/bin/env python
# -*- coding: utf-8 -*-
from flask import jsonify, request, make_response
from ds import daily, get_info
from . import app


@app.route('/', methods=['GET'])
def index():
    return "Daily Spent"


@app.route('/v1/daily', methods=['POST'])
def daily_route():
    daily_spent = float(request.data)
    result = daily(daily_spent)
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
