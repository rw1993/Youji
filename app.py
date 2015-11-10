# -*- coding:utf-8 -*-

import web

from urls import urls

from controllers import index

app = web.application(urls, globals())

if __name__ == "__main__":
    app.run()
