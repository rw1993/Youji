# -*- coding:utf-8 -*-

from utils import render

class index(object):

    def GET(self):
        return render.index()
