#!/usr/bin/env python
# encoding: utf-8
import os
import sys
import site

site.addsitedir('/home/spreadband/virtualenvs/spreadband.com/lib/python2.5/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'spreadband.settings'

sys.path.append('/home/spreadband/virtualenvs/spreadband.com/')

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

