#!/usr/bin/env python
from config.config import *
import logging
import tornado.escape
import tornado.ioloop
import tornado.web
import os.path
from KMeans import *
from database.MysqlDriver import MysqlDriver
from tornado.concurrent import Future
from tornado import web, websocket
from tornado.options import define, options, parse_command_line
from threading import Thread
import json

define("port", default=8888, help="run on the given port", type=int)

class HomePage(tornado.web.RequestHandler):
    @web.asynchronous
    def get(self):
        # self.render("index.html")
        self.write("Hello World")
        print("This will be the main page")
        self.finish()

class DoAnalysis(tornado.web.RequestHandler):
    @web.asynchronous
    def set_default_headers(self): # this as safety issues, cors
        origin = self.request.headers.get('Origin')
        if origin:
            self.set_header('Access-Control-Allow-Origin', origin)
        self.set_header('Access-Control-Allow-Credentials', 'true')
    def post(self):
        year = self.get_argument("year")
        taskId = self.get_argument("taskId")
        # print(taskId)
        self.db = MysqlDriver(DATABASE.host,DATABASE.username, DATABASE.password, DATABASE.dbname) # connect to MySql database server
        self.dataset = self.db.getFeatures()
        # km=KMeans( self.dataset, 50, 3, year, taskId)#initiatating ML algo
        self.db.updateStat(8, 100, 0)
        # MLthread = Thread(target = km.main, args=())
        # MLthread.daemon = True  
        # MLthread.start()
        self.write("Request created")#send the response of requested created
        self.finish()


def main():
    # try:
    parse_command_line()
    app = tornado.web.Application(
        [
            (r"/", HomePage),
            (r"/doAnalysis", DoAnalysis),
        ]
    )
    app.listen(options.port)
    print("MLServer core is hot now "+str(options.port))
    tornado.ioloop.IOLoop.current().start()
    # except:
    #     print("Server cannot be initialised")

if __name__ == "__main__":
    thread = Thread(target = main)
    thread.start()
    # thread.join()
    # main()