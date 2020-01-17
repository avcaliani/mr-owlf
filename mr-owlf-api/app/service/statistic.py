from os import environ as env

from pymongo import MongoClient

from service import database

DB_NAME = env.get('APP_DB_NAME', 'mr-owlf-db')


def find_last() -> any:
    """
    Find last statistic data available.
    :return: Statistics
    """
    conn: MongoClient = database.connect()
    data: any = conn[DB_NAME]['statistics'] \
        .find_one({}, sort=[('calculated_at', -1)])
    del data['_id']

    database.disconnect(conn)
    return data
