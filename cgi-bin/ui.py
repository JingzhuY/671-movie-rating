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
	similarity = dict()
	user = user_movie[userid]
	for otherid in user_movie:
		# skip the user himself
		if otherid == userid:
			continue
		other = user_movie[otherid]
		sim = pearsonSim(user, other)
		similarity[otherid] = sim

	#sort user-similarity
	similarity = sorted(similarity.items(), key = lambda d:d[1], reverse = True)

	for (otherid, sim) in similarity[:30]:
		other = user_movie[otherid]
		# ignore similarity less or equal than 0
		if sim <= 0:
			continue
		for m in other:
			if m not in user:
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
	#-----testing----
	#movies=loadsMovieData()
	
	#i=0
	#for (u, s) in similarity:
	#	print str(u) + '  '+str(s)
	#	print '<br>'
	#	i+=1
	#	if i>40:
	#		break
	#	for m in user_movie[u].keys():
	#		if user_movie[u][m] in [4,5]:
	#			print movies[m]['name']+'|| '+', '.join(movies[m]['genre'])+str(user_movie[u][m])
	#			print '<br>'
	#	print '<br><br>'
	
	#return recommended movies
	return rankings[:n]

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

#---------------UI-------------------
print "<TITLE>Movie_recommender</TITLE>"
print "<H1>Movie recommeder</H1>"
# read file to dictionaries
fhand = open('user_movie.json','rU')
lines = fhand.readlines()
user_movie = json.loads(lines[0])
movies = loadsMovieData()

# get posted value from form
form = cgi.FieldStorage()
userid = form['who'].value

# print user id
formhtml = '''
<p>User: %s</p> 
'''  
print formhtml % (userid)

# print movies recommended
print "<p><b>Recommended movie for you:</b><br>"
print '\r\n'

recommended_movies = predictRatings(userid, user_movie, 15)
print '<table>'
print '<tr><td><b>Title</b></td><td><b>Genre</b></td>'
for (r, m) in recommended_movies:
	print '<tr>'
	print '<td>'+movies[m]['name'] + '</td><td>' + '/ '.join(movies[m]['genre']) + '</td>'
	print '</tr>'
print '</table></p>'

# print movies rated 
print "<p><b>Your 5-star rating history:</b><br>"
rated = user_movie[userid]
#rated = sorted(rated.items(), key = lambda d: d[1], reverse = True)
#for (m, r) in rated[:10]:
print '<table>'
print '<tr><td><b>Title</b></td><td><b>Genre</b></td></tr>'
for m, r in rated.items():
	if r == 5:
		print '<tr>'
		print '<td>' + movies[m]['name']+ '</td><td>' + '/ '.join(movies[m]['genre']) + '</td>'
		print '</tr>'
print '</table></p>'