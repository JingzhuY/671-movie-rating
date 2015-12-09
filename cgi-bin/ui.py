#!/usr/bin/env python
import cgi
import json
from math import sqrt

print "Content-Type: text/html" # HTML is following
print # blank line, end of headers



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
	totals = dict()
	simSums = dict()
	rankings_list = []
	user = user_movie[userid]
	for other in user_movie:
		# skip the user himself
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
	return rankings[:n]

#---------------UI-------------------
print "<TITLE>CGI output</TITLE>"
print "<H1>This is my first CGI script</H1>"
form = cgi.FieldStorage()

# get posted value from form

userid = form['who'].value

formhtml = '''
<p>User: %s</p> 
'''  
print formhtml % (userid)

print "Recommended movie for you:"
print '\r\n'
fhand = open('user_movie.json','rU')
lines = fhand.readlines()
user_movie = json.loads(lines[0])
recommended_movies = predictRatings(userid, user_movie, 10)
for (r, m) in recommended_movies:
	print m
	print '\r\n'
