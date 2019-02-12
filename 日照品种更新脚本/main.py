# coding=utf-8
"""
脚本依赖环境
python3.x
pandas
requests
"""

import pandas as pd 
import requests
import json


def get_json(filename):
	excel = pd.read_excel(filename)
	
	return [dict(categoryFirstCode=v.categoryFirstCode,
				categoryFirstName=v.categoryFirstName,
				categorySecondCode=v.categorySecondCode,
				categorySecondName=v.categorySecondName,
				categoryThirdCode=v.categoryThirdCode,
				categoryThirdName=v.categoryThirdName) for v in excel.itertuples()]

def main(filename):
	print('filename', filename)
	data = {'fromId': 'test', 'test':'Y','data': get_json(filename)}
	url = 'http://dev.imprz.com/api/rizhao/jk19/'
	reqs = requests.post(url, {'JSON': json.dumps(data)} )
	print(reqs)
	if reqs.status_code == 200:
		print(reqs.json())


if __name__ == '__main__':
	main('sijxac07.xlsx')