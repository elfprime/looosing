import MySQLdb
import tushare as ts
import pandas as pd
from sqlalchemy import create_engine
import datetime

class MyDB(object):
    """Personal data base, python + MySQL + tushare"""
    def __init__(self, host='localhost', passwd='12345', user='root', port=3306, db='my'):
        super(MyDB, self).__init__()
        self.host = host
        self.passwd = passwd
        self.user = user
        self.port = port
        self.db = db
        id_str = 'mysql+mysqldb://{}:{}@{}/{}'.format(self.user, self.passwd, self.host, self.db)
        self.engine = create_engine(id_str)
        self.pool = ts.get_stock_basics().index
        


    def update_dailyprice(self, start=None):
        '''
        This function is used to update table - dailyprice

        '''
        with open('cfg.txt', 'r') as f:
            start = f.readlines()[0]
            print start
        for code in self.pool:
            p = ts.get_k_data(code, start=start)
            p.to_sql('dailyprice', self.engine, if_exists='append')

    def update_reports(self, start=None):
        '''
        This function is used to update table - reports
        如何处理复权数据？
        需要使用不复权数据？
        '''
        with open('cfg.txt', 'r') as f:
            year, quar = f.readlines()[1].split('-')
            year_start = int(year)
            quar_start = int(quar)
        today = datetime.date.today()
        year_end = today.year
        quar_end = today.month/4
        for y in xrange(year_start, year_end + 1):
            s = quar_start if y == year_start else 1
            e = quar_end if y == year_end else 4
            for q in xrange(s, e + 1):
                report = ts.get_report_data(y, q)
                report = pd.concat()
                # TODO

        report = ts.get_report_data(2017, 1)
        print report


    def read_k(self):
        a = pd.read_sql_table('test_data', self.engine, 
            parse_dates=['date']
            )
        print max(a.date)


if __name__ == '__main__':
    a = MyDB()
    a.update_reports()

  