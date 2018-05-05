from config.config import *
from sqlalchemy import *
import pymysql
import json
import numpy as np
import datetime
# pip install mysqlclient
pymysql.install_as_MySQLdb()

# I could have used ORM, but due to lack of time I settled on classical approach
# insertion is not able to handle bulk inserts in thousands
class MysqlDriver(object):
	def __init__(self, host, username, password, database):
		self.db = create_engine('mysql://'+username+':'+password+'@'+host,pool_recycle=3600) # connect to server
		self.database = database
		self.useDatabase()
		

	def useDatabase(self):
		self.db.execute("USE "+self.database+";") # select Trading for use
		self.metadata = MetaData(self.db)
		# self.weight=Table(self.tablename, self.metadata, autoload=True)
		# return self.db

	def getFeatures(self):
		self.WeightedFeatures=Table('WeightedFeatures', self.metadata, autoload=True)
		query = self.WeightedFeatures.select()
		result = self.db.execute(query)
		return result

	def updateTags(self, year, question_id, tag):
		self.useDatabase()
		self.Question_Master=Table('question_master', self.metadata, autoload=True)
		query = self.Question_Master.update().where(self.Question_Master.c.year==year).where(self.Question_Master.c.quid==question_id).values(difficulty_level=tag, post_tag = tag, is_analysed = 1, updated_at=datetime.datetime.now())
		result = self.db.execute(query)

	def updateStat(self, taskId, progress, status, accuracy=0):
		self.useDatabase()
		self.analysis=Table('analysis', self.metadata, autoload=false)
		query = self.analysis.update().where(self.analysis.c.id==taskId).values(progress=progress, status = status, accuracy = accuracy,  updated_at=datetime.datetime.now())
		result = self.db.execute(query)
	# def updateStat(self, taskId):
	# 	self.analysis=Table('analysis', self.metadata, autoload=True)
	# 	query = self.analysis.select()
	# 	# query = query.where(self.analysis.c.id == taskId)#check for current task
	# 	result = self.db.execute(query)
	# 	count = 0
	# 	for row in result: # for getting the count
	# 		count = count +1
	# 		print(row.id)
	# 		print(row.accuracy)
	# 		print(row.status)
	# 		print(row.algoUsed)
	# 	return count

	def insertStats(self, taskId, imgpath, imgcap):
		self.useDatabase()
		self.stats=Table('stats', self.metadata, autoload=false)
		query = self.stats.insert().values(task_id=taskId, img_path = imgpath, caption = imgcap, created_at=datetime.datetime.now(), updated_at=datetime.datetime.now())
		result = self.db.execute(query)

	def deleteStats(self, taskId):
		self.useDatabase()
		self.stats=Table('stats', self.metadata, autoload=false)
		query = self.stats.delete().where(self.stats.c.task_id == taskId)
		result = self.db.execute(query)

	def insertData(self, data):
		if len(data) > 0:
			try:
				query = self.orderBook.insert()
				query.execute(data)
				# print("Row insertion success")
			except:
				print("OMG!!! I failed at inserting data into the table")
		else:
			pass

# method for allowing user get features from WeightedFeatures table
	def selectData(self, params, arguments):
		# chanId = arguments("exchange")
		request = json.dumps({ k: arguments(k) for k in params })
		request = json.loads(request)
		query = self.orderBook.select()
		numRows = 50 #default number of rows to be fetched unless specified
		if 'price_greater_than' in request:
			query = query.where(self.orderBook.c.price > float(request['price_greater_than']))
			# print(query)

		elif 'pair' in request:
			query = query.where(self.orderBook.c.pairname == request['pair'])
			# print(query)
		elif 'exchange' in request:
			query = query.where(self.orderBook.c.exchange == request['exchange'])
		# else: #default snapshot, when user lands on the website
			
			
		if 'numRows' in request:
			numRows = int(request['numRows'])
		query = query.order_by(desc(self.orderBook.c.id)) # for snapshot, recent rows
		query = query.limit(numRows)
		result = self.db.execute(query)
		packet = []
		for row in result:
			payload = {
				'transactionType': row.transactionType,
				'price' : float(row.price),
				'count' : float(row.count),
				'exchange' : row.exchange,
				'pairname' : row.pairname
			}
			packet.append(payload)
		return (json.dumps(packet))
