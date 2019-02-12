# coding=utf-8
"""
读取excel表格数据，导入数据
依赖
python3.X
pymysql
sqlalchemy
pandas
"""

import pandas
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import create_engine

DB_CONF = {
	'url': '120.55.40.54/interface',
	'user': 'root',
	'password': 'opmysql'
}

EXCEL_FILE = 'enums.xlsx'

Base = declarative_base()


def get_pymysql_engine():
	"""
	获取数据库链接
	"""
	return create_engine(
		"mysql+pymysql://%s:%s@%s" % 
		(DB_CONF['user'], DB_CONF['password'], DB_CONF['url']), 
		max_overflow=5)

def enum():

	excel = pandas.read_excel(EXCEL_FILE)
	excel['create_time'] = datetime.datetime.now()
	excel['update_time'] = datetime.datetime.now()
	excel['create_by'] = 'sys'
	excel['update_by'] = 'sys'
	excel['batch_code'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	con = get_pymysql_engine().connect()#创建连接
	excel.to_sql(name='crm_enums', con=con, if_exists='append', index=False)


if __name__ == '__main__':
	enum()
