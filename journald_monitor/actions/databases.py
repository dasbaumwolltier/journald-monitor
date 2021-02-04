#This file requires the pyodbc package

import pyodbc

import logging as log

from pyodbc import Connection
from typing import List


con: Connection = None

class DatabaseState:
    con: Connection = None

def database_insert(config_dict: dict, line: str, table: str, fields: str, values: str, config: str) -> str:
    db_config = config_dict['database'][config]

    if DatabaseState.con is None:
        init_db_con(db_config)

    statement = 'INSERT INTO %s %s VALUES %s'%(table, fields, values)

    log.debug('Insert Statement: %s'%statement)

    con = DatabaseState.con
    con.execute(statement)
    con.commit()


def init_db_con(db_config: dict):
    import atexit

    con_str = ''
    if 'dsn' in db_config:
        con_str = 'DSN=%s;'%(db_config['dsn'])
    else:
        driver = db_config['driver']
        database = db_config['database']
        server = db_config['server']

        con_str = 'DRIVER=%s;DATABASE=%s;SERVER=%s;'%(driver, database, server)


    if 'username' in db_config:
        con_str += 'UID=%s;'%(db_config['username'])

    if 'password' in db_config:
        con_str += 'PWD=%s;'%(db_config['password'])

    if 'port' in db_config:
        con_str += 'PORT=%s;'%(db_config['port'])

    DatabaseState.con = pyodbc.connect(con_str)
    atexit.register(close_db)

def close_db():
    if DatabaseState.con is not None:
        DatabaseState.con.close()
