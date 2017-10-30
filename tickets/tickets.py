# coding = "utf-8"

"""
通过命令查询火车票
Usage:
	tickets <from> <to> <date>
	
Examples:
	tickets beijing shanghai 2016-09-21

Options:
	-h	显示帮助菜单
	(-g	高铁
	-d	动车
	-t	特快
	-k	快速
	-z	直达)(未实现)
"""

import requests
from docopt import docopt
from stations import stations
from prettytable import PrettyTable


def addColor(color, text):
	return text
	# 用于 Unix 终端
	table = {'red': '\033[91m', 'green': '\033[92m', 'nc': '\033[0m'} # 最后一个指没有颜色
	cv = table.get(color)
	nc = table.get('nc')
	return ''.join([cv, text, nc]) # 设置颜色|文字|取消颜色


class TrColl(object):
	"""解析数据"""
	headers = '车次 车站 时间 时长 商务座 一等座 二等座 软卧 硬卧 硬座'.split(' ')

	def __init__(self, rows):
		self.rows = rows

	def _getDur(self, rows):
		"""获取车次运行时间 Duration"""
		dur = rows.get('lishi').replace(':', 'h') + 'm'
		if dur.startswith('00'):
				dur = dur[4:]
		elif dur.startswith('0'):
				dur = dur[1:]
		return dur

	@property
	def trains(self):
		for row in self.rows:
			train = [
				str(row['station_train_code']) + '\n\n', # 车次
				addColor('green', str(row['from_station_name'])) + '\n' + addColor('red', str(row['to_station_name'])), # 出发到达车站
				addColor('green', str(row['start_time'])) + '\n' + addColor('red', str(row['arrive_time'])), # 出发到达时间
				self._getDur(row), # 经历时长
				row['swz_num'], # 商务座
				row['zy_num'], # 一等座
				row['ze_num'], # 二等座
				row['rw_num'], # 软卧
				row['yw_num'], # 硬卧
				row['yz_num'] # 硬座
			]
			yield train
		
	def prettyPrint(self):
		"""使用 prettyprint 库美化显示，像 MySQL 数据库那样"""
		pt = PrettyTable()
		pt._set_field_names(self.headers) # 设置每一列的标题
		for train in self.trains:
			pt.add_row(train)
		print(pt)		


def cli():
	"""命令行接口"""
	args = docopt(__doc__)
	print(args)
	headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:47.0) Gecko/20100101 Firefox/47.0"}
	date = args['<date>']
	fromSt = stations.get(args['<from>'])
	toSt = stations.get(args['<to>'])
	url = 'https://kyfw.12306.cn/otn/lcxxcx/query?purpose_codes=ADULT&queryDate={0}&from_station={1}&to_station={2}'.format(date, fromSt, toSt)
	r = requests.get(url, headers=headers, verify=False)
	print('\n网址\t', r.url)
	print('响应状态码\t', r.status_code, '\n')
	rows = r.json()['data']['datas']
	trains = TrColl(rows)
	trains.prettyPrint()


if __name__ == "__main__":
	cli()

