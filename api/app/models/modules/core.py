from flask import Flask, request, jsonify, make_response, url_for, Response, send_from_directory, redirect
from itsdangerous import URLSafeTimedSerializer, SignatureExpired
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import requests as req
import logging as logger
from functools import lru_cache

logger.basicConfig(level="DEBUG")

app = Flask(__name__)
app.config.from_pyfile('../configs/config.cfg')
CORS(app)

class InvalidUsage(Exception):
    status_code = 500

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['error'] = self.message
        return rv