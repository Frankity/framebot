import peewee

db = peewee.SqliteDatabase('data.base')


class BaseModel(peewee.Model):
    class Meta:
        database = db


class Alerts(BaseModel):
    id = peewee.CharField()
