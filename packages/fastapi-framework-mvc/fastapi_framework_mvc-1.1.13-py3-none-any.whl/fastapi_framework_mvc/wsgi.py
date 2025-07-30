#!/usr/bin/python3
# coding: utf-8


__author__ = 'Frederick NEY'

try:
    import gevent.monkey

    gevent.monkey.patch_all()
except ImportError as e:
    pass
try:
    import eventlet

    eventlet.monkey_patch(all=True)
except ImportError as e:
    pass

import multiprocessing

import gunicorn.app.base
from six import iteritems

from fastapi_framework_mvc.Database import Database


class Server(gunicorn.app.base.Application):

    def init(self, parser, opts, args):
        print(parser)
        print(opts)
        print(args)

    @staticmethod
    def number_of_workers():
        return multiprocessing.cpu_count() * 2

    @staticmethod
    def application():
        import logging
        from fastapi_framework_mvc.Server import Process
        logging.info("Initializing the server...")
        Process.init(tracking_mode=False)
        logging.info("Server initialized...")
        Process.load_plugins()
        logging.debug("Loading server routes...")
        Process.load_routes()
        Process.load_middleware()
        logging.debug("Server routes loaded...")
        logging.debug("Loading websocket events")
        Process.load_socket_events()
        logging.debug("Websocket events loaded...")
        # app.teardown_appcontext(Database.save)
        logging.info("Server started...")
        return Process.wsgi_setup()

    def __init__(self, options=None):
        Server.options = (options or {}) if not hasattr(Server, 'options') else Server.options
        self.application = Server.application()
        super(Server, self).__init__()

    def reload(self):
        """
        reload app function
        :return:
        """
        logging.info('reloading')
        try:
            import gevent.monkey
            gevent.monkey.patch_all()
        except ImportError as e:
            pass
        Environment.reload(os.environ['CONFIG_FILE'])
        self.application = Server.application()
        Server.load_options()
        super(Server, self).reload()

    def load_config(self):
        logging.info(Server.options)
        config = dict([(key, value) for key, value in iteritems(Server.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        try:
            import eventlet
            eventlet.monkey_patch(all=True)
        except ImportError as e:
            pass
        try:
            import eventlet
            eventlet.monkey_patch(all=True)
        except ImportError as e:
            pass
        return self.application

    @classmethod
    def load_options(cls):
        cls.options = {
            'bind': '%s:%i' % (Environment.SERVER['BIND']['ADDRESS'], int(Environment.SERVER['BIND']['PORT'])),
            'workers': Server.number_of_workers(),
            'threads': Environment.SERVER['THREADS_PER_CORE'],
            'capture_output': Environment.SERVER['CAPTURE'],
            "loglevel": loglevel,
            "worker_class": Environment.SERVER['WORKERS'],
            "reload_engine": 'poll'
        }
        if logging_dir_exist:
            cls.options["errorlog"] = os.path.join(os.environ.get("log_dir"), 'fastapi-error.log')
            cls.options["accesslog"] = os.path.join(os.environ.get("log_dir"), 'fastapi-access.log')
        if 'SSL' in Environment.SERVER:
            cls.options["certfile"] = Environment.SERVER['SSL']['Certificate']
            cls.options["keyfile"] = Environment.SERVER['SSL']['PrivateKey']


if __name__ == '__main__':
    import os
    import fastapi_framework_mvc.Server as Process
    import logging
    from logging.handlers import TimedRotatingFileHandler
    from fastapi_framework_mvc.Config import Environment

    loglevel = 'warning'
    logging_dir_exist = False
    if os.environ.get("LOG_DIR", None):
        os.environ.setdefault("log_dir", os.environ.get("LOG_DIR", "/var/log/server/"))
        os.environ.setdefault("log_file", os.path.join(os.environ.get("log_dir"), 'process.log'))
        if not os.path.exists(os.path.dirname(os.environ.get('log_file'))):
            os.mkdir(os.path.dirname(os.environ.get('log_file')), 0o755)
    if os.environ.get("log_file", None):
        logging.basicConfig(
            level=loglevel.upper(),
            format='%(asctime)s %(levelname)s %(message)s',
            handlers=[
                TimedRotatingFileHandler(
                    filename=os.environ.get('log_file'),
                    when='midnight',
                    backupCount=30
                )
            ]
        )
        logging_dir_exist = True
    else:
        logging.basicConfig(
            level=loglevel.upper(),
            format='%(asctime)s %(levelname)s %(message)s',
        )
    logging.info("Loading configuration file...")
    if 'CONFIG_FILE' in os.environ:
        Environment.load(os.environ['CONFIG_FILE'])
    else:
        Environment.load("/etc/server/config.json")
        os.environ.setdefault('CONFIG_FILE', "/etc/server/config.json")
    logging.info("Configuration file loaded...")
    try:
        loglevel = Environment.SERVER['LOG']['LEVEL']
        logging.getLogger().setLevel(loglevel.upper())
    except KeyError as e:
        pass
    logging_dir_exist = False
    try:
        if not os.path.exists(Environment.SERVER["LOG"]["DIR"]):
            os.mkdir(Environment.SERVER["LOG"]["DIR"], 0o755)
        RotatingLogs = TimedRotatingFileHandler(
            filename=os.path.join(Environment.SERVER["LOG"]["DIR"], 'process.log'),
            when='midnight',
            backupCount=30
        )
        RotatingLogs.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
        logging.getLogger().handlers = [
            RotatingLogs
        ]
        logging.info('Logging handler initialized')
        os.environ.setdefault("log_dir", Environment.SERVER["LOG"]["DIR"])
        logging_dir_exist = True
    except KeyError as e:
        pass
    except FileNotFoundError as e:
        pass
    except PermissionError as e:
        pass
    if len(Environment.Databases) > 0:
        logging.debug("Connecting to database(s)...")
        Database.register_engines(echo=Environment.SERVER['CAPTURE'])
        Database.init()
        logging.debug("Database(s) connected...")
    logging.info("Loading options...")
    Server.load_options()
    logging.info("Options loaded...")
    logging.info("Starting the server...")
    try:
        Server().run()
    except RuntimeError as e:
        exit(255)
