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

