'''
Collaborative filtering

steps:
1. Pearson correlaton score (similarity score)
2. Predict used weighted score
''' 
import csv
from math import sqrt
import progressbar
import json
from random import choice
# load "movies.dat" to a dictionary
# output: dictionary of movie information
def loadsMovieData():
	movies = dict()
	fhand= open('movies.dat','rU')
	lines = fhand.readlines()

	for line in lines:
		line = line.rstrip()
		line = line.split('::')
		movies[line[0]]= dict()
		movies[line[0]]['name'] = line[1]
		movies[line[0]]['genre'] = line[2].split('|')
	return movies


# input:  a list l
# output: a dictionary with this format:
#		{user1: {movie1: rating,
#				  movie2: rating,
#				  ...,
#				  movien: rating},
#		 User2: {}}
def preprocess(l):
	result = dict()
	print "preprocessing..."
	bar = progressbar.ProgressBar(maxval = len(l) , \
        widgets=[progressbar.Bar('=','[',']'), ' ', progressbar.Percentage()])
	i = 0
	bar.start()
	for line in l:
		bar.update(i + 1)
		i+=1
		if int(line[0]) not in result.keys():
			result[int(line[0])] = dict()
			result[int(line[0])][int(line[1])]=int(line[2])
		else:
			result[int(line[0])][int(line[1])]=int(line[2])
	bar.finish()

	# set filtering  (filter out users with rating # less than 100)
	for k,v in result.items():
		if len(v)< 100:
			del result[k] 
	print "length users" + str(len(result))

	#length users 1560(>100)   1069(>150)   806(>200)
	#print result.keys()
	return result


# 
def seperateTestData(user_movie):
	# 3883 movies in total
	# 2000 as predict set, 1883 as testing set
	print 'seperating...'
	bar = progressbar.ProgressBar(maxval = len(user_movie) , \
        widgets=[progressbar.Bar('=','[',']'), ' ', progressbar.Percentage()])
	i = 0
	bar.start()
	predict_user_movie = dict()
	test_user_movie = dict()
	
	for u in user_movie:
		bar.update(i+1)
		i +=1
		test_user_movie[u] =dict()
		rated_len = len(user_movie[u])
		for i in range(1,rated_len/10): # random 10% data as testing data
			m = choice(user_movie[u].keys())
			test_user_movie[u][m] = user_movie[u][m]
			del user_movie[u][m]
	predict_user_movie = user_movie
	bar.finish()
	#print "pred:"+str(len(predict_user_movie))
	#print "test:"+str(len(test_user_movie))
	return (predict_user_movie, test_user_movie)

	#for m in movies.keys():


# input: movie-rating data two users
# pearson similarity
def pearsonSim(user1, user2):
	# get both rated movies
	both_rated = []
	for m in user1.keys():
		if m in user2.keys():
			both_rated.append(m)
	num_of_both_rated = len(both_rated)
	
	if num_of_both_rated == 0:
		return 0

	# sum(u1m)
	user1_pref_sum = sum([user1[m] for m in both_rated])
	user2_pref_sum = sum([user2[m] for m in both_rated])
	
	# sum(u1m ^2)
	user1_sqr_pref_sum = sum([pow(user1[m], 2) for m in both_rated])
	user2_sqr_pref_sum = sum([pow(user2[m], 2) for m in both_rated])
	
	# sum(u1m * u2m)
	product_sum_of_both_users = sum(user1[m] * user2[m] for m in both_rated)
	
	# calculate pearson similarity
	numerator_value = product_sum_of_both_users - (float(user1_pref_sum * user2_pref_sum) / num_of_both_rated)
	demonimator_value = sqrt((user1_sqr_pref_sum - float(pow(user1_pref_sum, 2)) / num_of_both_rated) * \
		(user2_sqr_pref_sum - float(pow(user2_pref_sum, 2)) / num_of_both_rated))

	if demonimator_value == 0:
		return 0
	else:
		return (numerator_value / demonimator_value)

# input: userid
#		 user_movie -- movie-rating data for all users
#		 n -- recommend top n movies
# output: a list of highest movie-rating (using weighted average)
def predictRatings(userid, user_movie, n):
	movie_info = dict()
	for line in open('movies.dat', 'r'):
	    temp = line.split('::')
	    movie_info[temp[0]] = temp[1:]
	
	totals = dict()
	simSums = dict()
	rankings_list = []
	user = user_movie[userid]
	#print "user: "+str(userid)
	# user: 2785
	for other in user_movie:
		if other == userid:
			continue
		other = user_movie[other]
		sim = pearsonSim(user, other)
		
		# ignore similarity less or equal than 0
		if sim <= 0:
			continue
		for m in other:
			if m not in user or user[m] == 0:
				# similarity * rating
				totals.setdefault(m, 0)
				totals[m] += other[m] * sim
				#sum of similarities
				simSums.setdefault(m, 0)
				simSums[m] += sim

	# create normalized list
	rankings = [(total / simSums[m], m) for m, total in totals.items()]
	
	rankings.sort()
	rankings.reverse()
	
	#return recommended movies
	# print rankings[:n]
	#ranks = rankings[:n]
	
	#print rankings[:15]
	return rankings

	

def main():
	user_id = range(2783, 6041) # [2783...6040]
	movie_id = range(1, 3953) # [1...3952]
	f = open('training_ratings_for_kaggle_comp.csv','rU')
	SourceLines = csv.reader(f, delimiter=',')
	SourceLines = list(SourceLines)

	# preprocess
	user_movie = preprocess(SourceLines[1:])

	# save to file
	#with open('user_movie.json','w') as f:
	#	json.dump(user_movie,f)
	#print 'file saved'

	# load file
	#user_movie = dict()
	#with open('user_movie.json','rU') as f:
	#	lines = f.readlines()
	#	user_movie = json.loads(lines[0])

	# separate test data
	(predict_user_movie, test_user_movie) = seperateTestData(user_movie)
	#with open('predict_user_movie.json','w') as f:
	#	json.dump(predict_user_movie,f)
	#print 'file saved'
	#with open('test_user_movie.json','w') as f:
	#	json.dump(test_user_movie,f)
	#print 'file saved'

	#load file
	#predict_user_movie = dict()
	#test_user_movie = dict()
	#with open('predict_user_movie.json','rU') as f:
	#	lines = f.readlines()
	#	predict_user_movie = json.loads(lines[0])
	#with open('test_user_movie.json','rU') as f:
	#	lines = f.readlines()
	#	test_user_movie = json.loads(lines[0])

	test_predict_user = []
	i=0
	for u in predict_user_movie.keys():
		i+=1
		if i>100:
			break
		test_predict_user.append(u)


	# get 15 recommended movies with highest scores
	print 'predicting...'
	bar = progressbar.ProgressBar(maxval = len(predict_user_movie) , \
        widgets=[progressbar.Bar('=','[',']'), ' ', progressbar.Percentage()])
	ii = 0
	bar.start()
	user_movie_predicted = dict()
	for user in test_predict_user:
		bar.update(ii + 1)
		ii += 1
		#if ii>10: # for testing, print recommendations for 5 users
		#	break
		user_movie_predicted[user] = predictRatings(user, predict_user_movie, 15)
	bar.finish()

	# accuracy
	#i = 0
	accuracy = 0
	accuracy_real = 0
	total = 0
	for user in test_predict_user:
		#i+=1
		#if i>200:
		#	break
		for m in test_user_movie[user].keys():
			
			predicted_list = user_movie_predicted[user]

			total +=1
			rating = 0
			
			for (r,movie) in predicted_list:
				if str(m) == str(movie):
					rating = r
			
			#print str(test_user_movie[user][m])+', '+str(int(round(rating)))
			if int(test_user_movie[user][m]) in [int(round(rating)), int(round(rating))+1, int(round(rating))-1]:
			#if int(test_user_movie[user][m])>(rating-1) and int(test_user_movie[user][m])<(rating+1):
			
				accuracy +=1
			if int(test_user_movie[user][m]) == int(round(rating)):
				accuracy_real+=1

	print total
	print accuracy
	print accuracy_real
	print 'releived accuracy:'+str(float(accuracy)/total)
	print 'accuracy:'+str(float(accuracy_real)/total)
	

		
	
	

if __name__ == '__main__':
    main()
