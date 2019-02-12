# conding=utf-8
"""
导入数据到数据库中
"""
import pandas
import datetime

from sqlalchemy import create_engine

DB_CONF = {
	'url': 'rm-uf696xou9v8xe0sx0o.mysql.rds.aliyuncs.com/orders',
	'user': 'axu',
	'password': 'sv2_axu_qW12er34'
}

EXCEL_FILE = 'test-order-data.xlsx'


def get_pymysql_engine():
	"""
	获取数据库链接
	"""
	return create_engine(
		"mysql+pymysql://%s:%s@%s" % 
		(DB_CONF['user'], DB_CONF['password'], DB_CONF['url']), 
		max_overflow=5)


def main():

	excel = pandas.read_excel(EXCEL_FILE)
	excel['batch_code'] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	con = get_pymysql_engine().connect()#创建连接
	excel.to_sql(name='order_detail_temp', con=con, if_exists='replace', index=False)


if __name__ == '__main__':
	main()
