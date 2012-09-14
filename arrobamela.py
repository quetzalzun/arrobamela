#!/usr/bin/python
# -*- coding: utf-8 -*-
import tweepy, sys, getopt, csv
import time, calendar
from datetime import datetime

def mysql_time_to_epoch(mysql_time):
	mysql_time_struct = time.strptime(mysql_time, '%Y-%m-%d %H:%M:%S')
	return calendar.timegm(mysql_time_struct)

def string_to_datetime(string):
	struct = time.strptime(string, '%Y-%m-%d %H:%M:%S')
	return datetime.fromtimestamp(time.mktime(struct))

def connect_twitter():
	consumer_key="aRY4OZ39lakuwpBR8mXAIQ"
	consumer_secret="TsbCj8RrwOsI9A49Nk0lBIE4rLWOiM9IND9u5xSU"
	
	access_token="22443184-JqQh6QXJX2mMuKgQGO16VaPYgvlYL6AWZeeIbZCk"
	access_token_secret="Q6IMfzFIXngPEEJcsTIXmW3qAG8c0Z8qE86Mh8EGI"
	
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_token, access_token_secret)
	
	return tweepy.API(auth)

def write_csv(twitter_users, csvfile):
        csvWriter = csv.writer(open(csvfile, 'wb'), delimiter = ',', quotechar="|", quoting=csv.QUOTE_MINIMAL)
        csvWriter.writerow(["nombre de usuario", "tweets", "seguidores", "siguiendo", "último tweet"])

        for item in twitter_users:
		created = 0
		if hasattr(item, 'status'):
			created = item.status.created_at
                csvWriter.writerow(["@" + str(item.screen_name), item.statuses_count, item.followers_count, item.friends_count, created])

def discard_older(twitter_users, newer):
	return_this = []
	for item in twitter_users:
		if item.status.created_at >= newer:
			return_this.append(item)
	return return_this

def get_twitter_users(search_term):
	twitter = connect_twitter()
	twitter_users = []
	page = 1
	while True:
		tmp = twitter.search_users(search_term, 20, page)
		page += 1
		if not tmp:
			break
		twitter_users = twitter_users + tmp
	return twitter_users		

def main():
	try:
		opts, args = getopt.getopt(sys.argv[1:], "o:n:", ["output=","newer="])
	except getopt.GetoptError, err:
		print str(err)
		sys.exit(2)

	if len(args) == 0:
		print "Escribe el término de búsqueda"
		exit(2)
	search_term = args[0]

	csvfile = "out.csv"
	newer = 0
	for o, a in opts:
		if o in ("-o", "--output"):
			csvfile = a
		if o in ("-n", "--newer"):
			newer = string_to_datetime(a)

	twitter_users = get_twitter_users(search_term)

	if newer != 0:
		twitter_users = discard_older(twitter_users, newer)

	write_csv(twitter_users, csvfile)

if __name__ == "__main__":
    main()

