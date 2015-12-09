import csv
import json

f = open('training_ratings_for_kaggle_comp.csv','rU')
SourceLines = csv.reader(f, delimiter=',')
SourceLines = list(SourceLines)


user_movie = dict()
for line in SourceLines[1:]:
	if int(line[0]) not in user_movie.keys():
		user_movie[int(line[0])] = dict()
		user_movie[int(line[0])][int(line[1])]=int(line[2])
	else:
		user_movie[int(line[0])][int(line[1])]=int(line[2])	

print json.dumps(user_movie)
