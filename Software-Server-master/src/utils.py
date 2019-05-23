import pandas as pd
import pymysql
import config
import smtplib
from email.mime.text import MIMEText


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


class SendEmail:
    def __int__(self):
        pass

    def send_email(self, receivers, subject, data):
        message = MIMEText(data, 'plain', 'utf-8')
        message['Subject'] = subject
        message['From'] = config.mail_user
        message['To'] = receivers[0]

        try:
            smtpObj = smtplib.SMTP()
            smtpObj.connect(config.mail_host, 25)
            smtpObj.login(user=config.mail_user, password=config.mail_password)
            smtpObj.sendmail(from_addr=config.mail_user, to_addrs=receivers[0], msg=message.as_string())
            smtpObj.quit()
            status = 200
        except Exception as e:
            print('send email fail', e)
            status = 500
        return status
