from config.config import *
from sqlalchemy import *
import pymysql
import json
import numpy as np
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

	def updateTags(self):
		self.Question_Master=Table('Question_Master', self.metadata, autoload=True)
		query = self.Question_Master.update().where(self.Question_Master.c.quid==5).values(name='user #5')
		# query = self.Question_Master.select()
		result = self.db.execute(query)
		return result
	# def checkExistingTask(self):
	# 	self.analysis=Table('analysis', self.metadata, autoload=True)
	# 	query = self.analysis.select()
	# 	query.where(self.analysis.c.status == 10)#check if any task is still running
	# 	result = self.db.execute(query)
	# 	print(query)
	# 	count = 0
	# 	for row in result: # for getting the count
	# 		count = count +1
	# 		print(row)

	# 	return count

	def updateStat(self, taskId, progress, status):
		self.analysis=Table('analysis', self.metadata, autoload=True)
		query = self.analysis.update().where(self.Question_Master.c.id==taskId).values(progress=progress, status = taskId)
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
