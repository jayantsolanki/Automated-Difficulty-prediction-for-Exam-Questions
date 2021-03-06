#k-means clustering

from config.config import * #configuration
from copy import deepcopy
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from sklearn import preprocessing
from scipy import stats
from database.MysqlDriver import MysqlDriver
import random
import string
MAX_ITERATION = 50
K = 3 #clusters
class KMeans(object):

	def __init__(self, features, max_iteration, k, year, taskId):
		self.dataset = features
		self.MAX_ITERATION = max_iteration
		self.K = k
		self.year = year
		self.taskId = taskId
		self.db = MysqlDriver(DATABASE.host,DATABASE.username, DATABASE.password, DATABASE.dbname) # connect to MySql database server
		self.path = DATABASE.imgpath+str(self.year)+'/'


	# Euclidean Distance Calculator
	def dist(self, a, b, ax=1):
	    return np.linalg.norm(a - b, axis=ax)

	def main(self):
		self.plt = plt
		self.plt.rcParams['figure.figsize'] = (16, 9)
		self.plt.style.use('ggplot')
		#delete older images in the stat for particular taskid
		self.db.deleteStats(self.taskId)

		# Importing the dataset
		# data = pd.read_csv('weightedfeatures.csv')
		# data = pd.read_csv('WeightedFeatures2015.csv')
		# data = pd.read_csv('WeightedFeatures2016.csv')
		f1 = []
		f2 = []
		manual_tags = []
		question_id = []
		for row in self.dataset:#getting data from the search query
			f1.append(row.feature1)
			f2.append(row.feature2)
			manual_tags.append(row.difficulty_level)
			question_id.append(row.question_id)

		X = np.array(list(zip(f1, f2)))
		Y = np.array(list(zip(manual_tags)))
		# Perform mean normalization
		print("\n\nPerforming Mean Normalization...\n");
		# meanX = mean(X);	#Mean of all the features
		# stdX = std(X);	#Standard deviation of all the features
		# X = preprocessing.scale(X)
		min_max_scaler = preprocessing.MinMaxScaler()
		max_abs_scaler = preprocessing.MaxAbsScaler()
		X = max_abs_scaler.fit_transform(X)
		self.plt.scatter(X[:,0], X[:,1], c='black', s=7)
		# plt.show()
		# plt.savefig('%s/%s/%s/%s-%d/channels_round-%d.png'%(LOG_DIR,STR_GRAPHS,STR_CSETUP,TARGET_SETUP,this_setup+1,this_day*NUMBER_OF_ROUNDS+this_round+1))
		# rrandom = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(12)])
		title="Initial distribution of features in "+str(len(X))+' questions'
		self.plt.title('%s'%(title))
		self.plt.xlabel('feature1')
		self.plt.ylabel('feature2')
		imgpath = self.year+self.taskId+str(1)+'.png'
		self.plt.savefig('%s'%(self.path+imgpath))
		self.db.insertStats(self.taskId, imgpath, title)



		# Plotting along with the Centroids
		# plt.scatter(X[:,0], X[:,1], c='#050505', s=7)
		# plt.show()
		# plt.scatter(C[:,0], C[:,1], marker='*', s=200, c='g')
		# plt.show()



		# Loop will run till the error becomes zero
		Cluster_error = float("inf")
		saved_clusters = []
		saved_centroids = []

		for j in range(MAX_ITERATION):
			print(Cluster_error)
			C = np.zeros((K, 2), dtype=np.float32);
			rand = np.random.permutation(X)
			# randomly generated initial clusters
			C = rand[0:K]
			# To store the value of centroids when it updates
			C_old = np.zeros(C.shape)
			# Cluster Lables(0, 1, 2)
			clusters = np.zeros(len(X))
			# Error func. - Distance between new centroids and old centroids
			error = self.dist(C, C_old, None)
			while error != 0:
			    # Assigning each value to its closest cluster
			    Total_error = 0
			    for i in range(len(X)):
			        distances = self.dist(X[i], C)
			        Total_error = Total_error + np.min(distances)
			        cluster = np.argmin(distances)#storing the index of the mimimum error found for a particular centroid
			        clusters[i] = cluster
			    # Storing the old centroid values
			    C_old = deepcopy(C)
			    # Finding the new centroids by taking the average value
			    for i in range(K):
			        points = [X[j] for j in range(len(X)) if clusters[j] == i]
			        C[i] = np.mean(points, axis=0)
			    error = self.dist(C, C_old, None)
			    if(Cluster_error > Total_error):
			    	Cluster_error = Total_error
			    	saved_clusters = clusters
			    	saved_centroids = C
			progress = int(j*100/MAX_ITERATION)
			print(progress)
			self.db.updateStat(self.taskId, progress, 1)
		    
		self.plt.rcParams['figure.figsize'] = (16, 9)
		self.plt.style.use('ggplot')
		colors = ['r', 'g', 'b', 'y', 'c', 'm']
		fig, ax = self.plt.subplots()
		for i in range(K):
		        points = np.array([X[j] for j in range(len(X)) if saved_clusters[j] == i])
		        ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
		ax.scatter(saved_centroids[:, 0], saved_centroids[:, 1], marker='*', s=200, c='#050505')
		# plt.show()
		title="Distribution of features in 3 clusters along with final centroids for "+str(len(X))+' questions'
		self.plt.title('%s'%(title))
		self.plt.xlabel('feature1')
		self.plt.ylabel('feature2')
		imgpath = self.year+self.taskId+str(2)+'.png'
		self.plt.savefig('%s'%(self.path+imgpath))
		self.db.insertStats(self.taskId, imgpath, title)
		print(saved_centroids)

		# Label Nomenclature
		hard_label = 2;
		medium_label = 1;
		easy_label = 0;

		polls = np.zeros((K, 2),dtype=np.uint8);
		# For feature 1 - Fraction of people who solved the given question
		# correctly adjusted by weights.
		# Expectation: Negative value for hard questions
		#			   Positive value for easy questions
		#			   Values close to zero for medium level questions
		# Hence order expected: Hard < Medium < Easy
		indices = np.argsort(saved_centroids[:,0])#sorting in descending order
		polls[indices[0],0] = hard_label
		polls[indices[1],0] = medium_label
		polls[indices[2],0] = easy_label

		# For feature 2 - Average marks of people who solved given question
		# incorrectly or did not solve it at all adjusted by weights
		# Expectation: Positive value for hard questions
		#			   Negative value for easy questions
		#			   Values close to zero for medium level questions
		# Hence order expected: Easy < Medium < Hard

		indices = np.argsort(saved_centroids[:,1])#sorting in descending order
		polls[indices[0],1] = easy_label
		polls[indices[1],1] = medium_label
		polls[indices[2],1] = hard_label

		print(polls)

		# Map the labels
		map = np.zeros((K, 1), dtype=np.uint8);
		mode = polls[0, :]
		# print(mode[0])
		map[0,0] = mode[0];	# Winning Label of Cluster 1
		mode = polls[1, :]
		map[1,0] = mode[0];	# Winning Label of Cluster 2
		mode = polls[2, :]
		map[2,0] = mode[0];	# Winning Label of Cluster 3
		print(map)


			# m = size(current_labels, 1);
			# for i = [1:m],
			# 	labels(i, 1) = map(current_labels(i, 1));
			# end;

		# Now assign semantically correct difficulty tags
		# print(clusters)
		predicted_tags = np.zeros((len(X),1), dtype=np.uint8)

		for i in range(len(X)):
			predicted_tags[i,0] = map[int(saved_clusters[i]),0]
			# print(int(clusters[i]))

		# calculating accuracy
		count = 0
		for i in range(len(X)):
			if(predicted_tags[i] == Y[i]):
				count = count + 1

		# updating the post-tags and difficulty_level
		print('updating tags in the question master database\n')
		for i in range(len(X)):
			self.db.updateTags(self.year, int(question_id[i]), int(predicted_tags[i]))

		print (count)

		print("\n Accuracy is %f \n" %(count/len(X)*100))
		self.db.updateStat(self.taskId, 100, 2, count/len(X)*100)
		print("Analysis Completed")
		exit()

