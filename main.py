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
	return result


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
	print "user: "+str(userid)
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
	# rankings.reverse()
	#return recommended movies
	# print rankings[:n]
	ranks = rankings.reverse()[:n]
	#return recommended movies with title & info
	rec_result = dict()
	for i in range(10):
		m_id = ranks[i][1]
		rec_result[i] = movie_info[m_id]
	print rec_result
	
	

def main():
	user_id = range(2783, 6041) # [2783...6040]
	movie_id = range(1, 3953) # [1...3952]
	f = open('training_ratings_for_kaggle_comp.csv','rU')
	SourceLines = csv.reader(f, delimiter=',')
	SourceLines = list(SourceLines)
	user_movie = preprocess(SourceLines[1:])
	#with open('user_movie.json','w') as f:
	#	json.dump(user_movie,f)
	#print 'file saved'
	#print len(user_movie)


	# get 10 recommended movies with highest scores
	i=0
	for user in user_movie:
		i+=1
		if i>5: # for testing, print recommendations for 5 users
			break
		predictRatings(user, user_movie, 10)
		
	#print pearsonSim(user_movie[2783],user_movie[2785])
	print ''

if __name__ == '__main__':
    main()
