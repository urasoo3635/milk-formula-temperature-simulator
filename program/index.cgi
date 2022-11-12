#! /usr/local/bin/python

import cgitb
from app import app
from wsgiref.handlers import CGIHandler

CGIHandler().run(app)

