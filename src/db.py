from functools import wraps
import logging
import time

import psycopg2
import psycopg2.extras
import os


def retry_connection(fn):
    @wraps(fn)
    def wrapper(*args, **kw):
        cls = args[0]
        for x in range(cls._reconnectTries):
            try:
                return fn(*args, **kw)
            except (psycopg2.InterfaceError, psycopg2.OperationalError) as e:
                print("Idle for %s seconds" % (cls._reconnectIdle), e)
                time.sleep(cls._reconnectIdle)
                cls.connect()
    return wrapper


class DB:
    database = None
    user = None
    password = None
    host = None
    port = None
    _reconnectIdle = 4
    _reconnectTries = 3

    def __init__(self):
        self.conn = None
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(
            database=self.database,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port,
        )
        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    @retry_connection
    def _execute(self, sql):
        self.cursor.execute(sql)

    def get_list(self, query):
        self._execute(query)
        rows = self.cursor.fetchall()
        return rows

    @retry_connection
    def _add_or_update(self, query):
        try:
            self._execute(query)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            logging.exception(e)

    def update(self, query):
        self._add_or_update(query)

    def insert(self, query):
        self._add_or_update(query)

    def update_multiple_values(self, sql, values):
        self._execute_values(sql, values)

    def insert_many(self, sql, values):
        self._execute_values(sql, values)

    @retry_connection
    def _execute_values(self, sql, values):
        try:
            psycopg2.extras.execute_values(
                self.cursor, sql, values, template=None, page_size=len(values))
            self.conn.commit()
        except Exception as e:
            logging.exception(e)

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()


class FinniuDB(DB):
    database = os.environ['FINNIU_DB']
    user = os.environ['FINNIU_USERNAME']
    password = os.environ['FINNIU_PASSWORD']
    host = os.environ['FINNIU_HOST']
    port = os.environ['FINNIU_PORT']