import pymongo
import os
import pyexcel as pe

mongo_uri = 'localhost'
mongo_db = 'financial_db'
root_dir_name = '上海指数FromDB'

cur_dir = os.getcwd()
dir_full_name = os.path.join(cur_dir, root_dir_name)
if not os.path.exists(dir_full_name):
	os.makedirs(dir_full_name)

client = pymongo.MongoClient(mongo_uri)
db = client[mongo_db]
collection_list = db.list_collection_names()
for collection in collection_list:
	file_name = collection 
	sheet_name = collection

	results = db[collection].find()
	print (sheet_name)

	file_name = file_name.replace(' ', '') + '.xlsx'
	file_full_name = os.path.join(cur_dir, root_dir_name, file_name)	

	if not os.path.exists(file_full_name):
		data = [['更新时间', '指数代码', '样本数量', '收盘', '样本均价', '成交额(亿元)', '平均股本(亿股)', '总市值(万亿)', '占比(%)', '静态市盈率']]
		pe.save_as(array=data, dest_file_name=file_full_name, sheet_name=sheet_name)

	sheet = pe.get_sheet(file_name=file_full_name)
	for result in results:
		print(result)
		ssei_data = result['ssei_data']
		update_time = result['update_time']
		ssei_data.insert(0, update_time)
		update_time_list = sheet.column[0]
		if update_time not in update_time_list:
			sheet.row += ssei_data

	sheet.save_as(file_full_name)
client.close()