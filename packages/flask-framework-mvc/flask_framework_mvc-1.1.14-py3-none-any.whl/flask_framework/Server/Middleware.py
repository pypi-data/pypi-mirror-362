# coding: utf-8


__author__ = 'Frederick NEY'


class Load(object):

    def __init__(self, srv):
        """

        :param srv:
        :type srv: flask.Flask
        :return: Load object
        """
        import logging
        try:
            import server
            server.middleware.Load(srv)
        except Exception as e:
            import os
            logging.debug("{}: {} in {}".format(__name__, e, os.getcwd()))
        try:
            import Server
            Server.Middleware.Load(srv)
        except Exception as e:
            import os
            logging.debug("{}: {} in {}".format(__name__, e, os.getcwd()))
        return
