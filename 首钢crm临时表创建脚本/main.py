# coding=utf-8
"""
读取excel表格数据，创建表
依赖
python3.X
pymysql
sqlalchemy
pandas
"""

import xlrd
import re
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

EXCEL_FILE = 'tables.xlsx'

Base = declarative_base()


def get_pymysql_engine():
	"""
	获取数据库链接
	"""
	return create_engine(
		"mysql+pymysql://%s:%s@%s" % 
		(DB_CONF['user'], DB_CONF['password'], DB_CONF['url']), 
		max_overflow=5)


def uncamelize(camelCaps, separator="_"):
	"""
	驼峰命名转下划线命名
	"""
	pattern = re.compile(r'([A-Z]{1})')
	sub = re.sub(pattern, separator+r'\1', camelCaps).lower()
	return sub


def get_default(v):
	if v:
		if isinstance(v, str) and v.strip():
			return v.strip()
		else:
			return v 
	return None


def get_table_by_sheet(sheet):
	"""
	根据sheet动态产生类
	"""
	print('sheet', sheet.name)
	print('table remak', sheet.cell_value(0, 0))
	print('table name', sheet.cell_value(1, 0))
	print('table rows', sheet.nrows)

	class Table(Base):

		__tablename__ = sheet.cell_value(1, 0)
		__doc__ = sheet.cell_value(0, 0)

		id = Column(Integer, primary_key=True, autoincrement=True)
		batch_code = Column(String(64), comment=u'批次号')

	for row_index in range(3, sheet.nrows):
		row = sheet.row_values(row_index)
		if not row[0].strip():
			continue

		filed = row[0].strip()
		if '_' in filed:
			filed = filed.lower()
		else:
			filed = uncamelize(filed)

		if row[2] in 'Cc':
			setattr(Table, filed, Column(
				String(row[3]), 
				comment=u'%s:%s'%(row[1], row[6]), 
				default=get_default(row[5])))

		if row[2] in 'Nn':
			n = str(row[3]).split(',')
			if len(n) == 1:
				setattr(Table, filed, Column(
					Integer, 
					comment=u'%s:%s'%(row[1], row[6]), 
					default=get_default(row[5])))
			else:
				setattr(Table, filed, Column(
					Numeric(int(n[0]), int(n[1])), 
					comment=u'%s:%s'%(row[1], row[6]), 
					default=get_default(row[5])))

	setattr(Table, 'create_time', Column(DateTime, default=datetime.datetime.now))
	setattr(Table, 'create_by', Column(String(32), default='sys'))
	setattr(Table, 'update_time', Column(DateTime, default=datetime.datetime.now))
	setattr(Table, 'update_by', Column(String(32), default='sys'))

	return Table

def main():

	excel = xlrd.open_workbook(EXCEL_FILE)
	print(excel.sheet_names())

	for sheet in excel.sheets():
		print(get_table_by_sheet(sheet))

	engine = get_pymysql_engine()
	Base.metadata.drop_all(engine)
	Base.metadata.create_all(engine)
	print('this is main')


if __name__ == '__main__':
	main()