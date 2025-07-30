from sqlalchemy import insert


class RPALogRepository:
    def __init__(self, connection, rpa, table):
        self.connection = connection
        self.table = table
        self.rpa = rpa

    def insert(self, data: dict):
        try:
            data.update({'RPA': self.rpa})
            with self.connection as db:
                db.session.execute(insert(self.table).values(**data))
                db.session.commit()
        except Exception as e:
            pass
