import pandas as pd
import pymysql
import config


class DatabaseDeal:
    def __init__(self):
        self.host = config.host
        self.user = config.user
        self.database = config.database
        self.password = config.password

        self.result = None

    def select(self, sql):
        con = pymysql.connect(self.host, self.user, self.password, self.database)
        try:
            self.result = pd.read_sql(sql=sql, con=con)
        except Exception as e:
            print(e)
            status = 500
        else:
            status = 200
        finally:
            con.close()
        return self.result, status

    def insert_like(self, sql):
        con = pymysql.connect(self.host, self.user, self.password, self.database)
        cursor = con.cursor()
        try:
            cursor.execute(sql)
            con.commit()
        except pymysql.err.IntegrityError as e:
            print(e)
            print('sql: ', sql)
            status = 400
            con.rollback()
        except pymysql.err.DataError as e:
            print(e)
            print('sql: ', sql)
            status = 402
        except Exception as e:
            print('undeal error: ', e, type(e))
            print('sql: ', sql)
            status = 201
        else:
            status = 200
        finally:
            con.close()
        return None, status
