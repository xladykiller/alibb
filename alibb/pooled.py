from __future__ import absolute_import, division, with_statement

import copy
import itertools
import logging
import os
import time
try:
    import MySQLdb.constants
    import MySQLdb.converters
    import MySQLdb.cursors
except ImportError:
    # If MySQLdb isn't available this module won't actually be useable,
    # but we want it to at least be importable on readthedocs.org,
    # which has limitations on third-party modules.
    if 'READTHEDOCS' in os.environ:
        MySQLdb = None
    else:
        raise
from DBUtils import PooledDB
class Conn(object):

    def __init__(self, host, database, user=None, password=None,
                 max_idle_time=7 * 3600, connect_timeout=0,
                 time_zone="+0:00", charset = "utf8", sql_mode="TRADITIONAL"):
        self.host = host
        self.database = database
        self.max_idle_time = float(max_idle_time)

        args = dict(conv=CONVERSIONS, use_unicode=True, charset=charset,
                    db=database, init_command=('SET time_zone = "%s"' % time_zone),
                    connect_timeout=connect_timeout, sql_mode=sql_mode)
        if user is not None:
            args["user"] = user
        if password is not None:
            args["passwd"] = password

        # We accept a path to a MySQL socket file or a host(:port) string
        if "/" in host:
            args["unix_socket"] = host
        else:
            self.socket = None
            pair = host.split(":")
            if len(pair) == 2:
                args["host"] = pair[0]
                args["port"] = int(pair[1])
            else:
                args["host"] = host
                args["port"] = 3306

        self._db = None
        self._pool = None
        self._db_args = args
        self._last_use_time = time.time()
        try:
            self._init_pool()
        except Exception:
            logging.error("Cannot connect to MySQL on %s", self.host,
                          exc_info=True)

    def _init_pool(self):
        try:
            self._pool = PooledDB.PooledDB(creator=MySQLdb, **self._db_args)
        except:
            logging.error("init db pool failed")

    def get_connection(self):
        if self._pool is None:
            self._init_pool()
        return self._pool.connection()

    def execute_lastrowid(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.lastrowid
        finally:
            if conn is not None:
                if cursor is not None:
                    cursor.close()
                conn.close()

    def execute_rowcount(self, query, *parameters, **kwparameters):
        """Executes the given query, returning the lastrowid from the query."""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            self._execute(cursor, query, parameters, kwparameters)
            return cursor.rowcount
        finally:
            if conn is not None:
                if cursor is not None:
                    cursor.close()
                conn.close()

    update = execute_rowcount
    insert = execute_lastrowid
    def query(self, query, *parameters, **kwparameters):
        """Returns a row list for the given query and parameters."""
        conn = None
        cursor = None
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            self._execute(cursor, query, parameters, kwparameters)
            column_names = [d[0] for d in cursor.description]
            return [Row(itertools.izip(column_names, row)) for row in cursor]
        finally:
            if conn is not None:
                if cursor is not None:
                    cursor.close()
                conn.close()

    def get(self, query, *parameters, **kwparameters):
        """Returns the (singular) row returned by the given query.

        If the query has no results, returns None.  If it has
        more than one result, raises an exception.
        """
        rows = self.query(query, *parameters, **kwparameters)
        if not rows:
            return None
        elif len(rows) > 1:
            raise Exception("Multiple rows returned for Database.get() query")
        else:
            return rows[0]


    def _execute(self, cursor, query, parameters, kwparameters):
        try:
            return cursor.execute(query, kwparameters or parameters)
        except OperationalError:
            logging.error("Error connecting to MySQL on %s", self.host)
            raise


class Row(dict):
    """A dict that allows for object-like property access syntax."""
    def __getattr__(self, name):
        try:
            return self[name]
        except KeyError:
            raise AttributeError(name)


if MySQLdb is not None:
    # Fix the access conversions to properly recognize unicode/binary
    FIELD_TYPE = MySQLdb.constants.FIELD_TYPE
    FLAG = MySQLdb.constants.FLAG
    CONVERSIONS = copy.copy(MySQLdb.converters.conversions)

    field_types = [FIELD_TYPE.BLOB, FIELD_TYPE.STRING, FIELD_TYPE.VAR_STRING]
    if 'VARCHAR' in vars(FIELD_TYPE):
        field_types.append(FIELD_TYPE.VARCHAR)

    for field_type in field_types:
        CONVERSIONS[field_type] = [(FLAG.BINARY, str)] + CONVERSIONS[field_type]

    # Alias some common MySQL exceptions
    IntegrityError = MySQLdb.IntegrityError
    OperationalError = MySQLdb.OperationalError

conn = Conn('127.0.0.1','spider','root','11111')
