import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
import argparse
import sys
import json

from redis import Redis, RedisError

from remotecv.utils import config
from remotecv.utils import logger
from remotecv.unique_queue import UniqueQueue


class MainHandler(tornado.web.RequestHandler):
    queue = None

    def get(self):
        self.clear()
        response = [{'name': 'REMOTECV', 'quantity': 0}]
        try:
            if not MainHandler.queue:
                redis = Redis(host=config.redis_host,
                              port=config.redis_port,
                              db=config.redis_database,
                              password=config.redis_password)
                MainHandler.queue = UniqueQueue(server=redis)
            jobs = MainHandler.queue.info().get('pending')
            response[0]['quantity'] = jobs
            self.write(json.dumps(response))
        except RedisError:
            MainHandler.queue = None
            logger.exception('Could not connect to Redis')
            self.write(json.dumps(response))
        finally:
            self.set_header('Content-Type', 'application/json')


def main(params=None):
    if params is None:
        params = sys.argv[1:]
    parser = argparse.ArgumentParser(description='Runs RemoteCV status endpoint')
    token_group = parser.add_argument_group('HireFire Token for info endpoint')
    token_group.add_argument('-t', '--token', default='123', help='HireFire token')

    conn_group = parser.add_argument_group('Pyres Connection Arguments')
    conn_group.add_argument('--host', default='localhost', help='Redis host')
    conn_group.add_argument('--port', default=6379, type=int, help='Redis port')
    conn_group.add_argument('--database', default=0, type=int, help='Redis database')
    conn_group.add_argument('--password', default=None, help='Redis password')

    arguments = parser.parse_args(params)
    config.hirefire_token = arguments.token
    config.redis_host = arguments.host
    config.redis_port = arguments.port
    config.redis_database = arguments.database
    config.redis_password = arguments.password

    application = tornado.web.Application([
        (r"/hirefire/{hft}/info".format(hft=config.hirefire_token), MainHandler),
    ])
    http_server = tornado.httpserver.HTTPServer(application)
    port = int(os.environ.get("PORT", 5000))
    http_server.listen(port)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()
