"""
该模块进行数据库ORM定义
"""

from enum import unique
from peewee import *

Db_sqlite = SqliteDatabase("database.db")
# db = SqliteDatabase(":memory:")

class App(Model):
    id = AutoField(unique=True)
    name = TextField(unique=True)
    path = TextField()
    tag = TextField()

    class Meta():
        database = Db_sqlite


class InFo(Model):
    id = AutoField()
    name = TextField(unique=True)
    content = TextField()

    class Meta():
        database = Db_sqlite

