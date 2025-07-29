import os
import re

import psycopg as dbapi2
from pydal._globals import THREAD_LOCAL
from pydal.adapters import Postgre, adapters
from pydal.utils import split_uri_args


@adapters.register_for("postgres", "postgres:psycopg3")
class Postgre3(Postgre):
    drivers = ("psycopg3", "psycopg")

    def find_driver(self):
        self.driver_name = self.drivers[0]
        self.driver = dbapi2

    def _config_json(self):
        self.dialect = self._get_json_dialect()(self)
        self.parser = self._get_json_parser()(self)

    def _initialize_(self):
        # copied and modified `database` driver arg to `dbname`
        super(Postgre, self)._initialize_()
        ruri = self.uri.split("://", 1)[1]
        m = re.match(self.REGEX_URI, ruri)
        if not m:
            raise SyntaxError("Invalid URI string in DAL")
        user = self.credential_decoder(m.group("user"))
        password = self.credential_decoder(m.group("password"))
        host = m.group("host")
        uriargs = m.group("uriargs")
        if uriargs:
            uri_args = split_uri_args(uriargs, need_equal=False)
        else:
            uri_args = dict()
        socket = uri_args.get("unix_socket")
        if not host and not socket:
            raise SyntaxError("Host or UNIX socket name required")
        db = m.group("db")
        self.driver_args.update(user=user, dbname=db)  # !!! changed
        if password is not None:
            self.driver_args["password"] = password
        if socket:
            if not os.path.exists(socket):
                raise ValueError("UNIX socket %r not found" % socket)
            if self.driver_name == "psycopg2":
                # the psycopg2 driver let you configure the socket directory
                # only (not the socket file name) by passing it as the host
                # (must be an absolute path otherwise the driver tries a TCP/IP
                # connection to host); this behaviour is due to the underlying
                # libpq used by the driver
                socket_dir = os.path.abspath(os.path.dirname(socket))
                self.driver_args["host"] = socket_dir
        else:
            port = int(m.group("port") or 5432)
            self.driver_args.update(host=host, port=port)
            sslmode = uri_args.get("sslmode")
            if sslmode and self.driver_name == "psycopg2":
                self.driver_args["sslmode"] = sslmode
        if self.driver:
            self.__version__ = "%s %s" % (self.driver.__name__, self.driver.__version__)
        else:
            self.__version__ = None
        THREAD_LOCAL._pydal_last_insert_ = None
        self.get_connection()
