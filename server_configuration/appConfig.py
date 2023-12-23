#!/usr/bin/python
# -*- coding: utf-8 -*-
import urllib


class CommonConfig(object):
    # User Type
    API_HEADERS = {'Content-type': 'application/json'}

class DevelopmentConfig(CommonConfig):
    DATABASE = "edusample2db"
    BIND_PORT = 8081
    SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:p#ssw0rd@127.0.0.1/edusample2db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DAEMON_HEADERS = {'Content-type': 'application/json'}
    UPLOAD_FOLDER = "./"


class ProductionConfig(CommonConfig):
    DATABASE = "edusample2db"
    BIND_PORT = 8081
    SQLALCHEMY_DATABASE_URI = 'mysql://dbadmin:p#ssw0rd@127.0.0.1/edusample2db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DAEMON_HEADERS = {'Content-type': 'application/json'}
    UPLOAD_FOLDER = "./"


