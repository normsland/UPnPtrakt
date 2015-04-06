#!/usr/bin/env python
import argparse
import os
import json
import urllib2
from urllib2 import Request, urlopen
import sqlite3 as sql
import datetime
import djmountHandler
import episodeMatcher
import trakt
from trakt.tv import TVShow, TVEpisode

CLIENT_ID = '579e14acbabe1637df5f9537de20a582cff25ca885964083b0d1fd54a49defc1'

def postNewEpisodesToTrakt(newEpisodes):
	HEADERS = {'Content-Type': 'application/json','trakt-api-version': '2','trakt-api-key': CLIENT_ID}
	HEADERS['Authorization'] = 'Bearer {}'.format(trakt.api_key)
	for episode in newEpisodes:
		title = episode[0]
		season = episode[2]
		episode_num = episode[3]
		to_post = TVEpisode(title,season,episode_num)
		trakt_id = to_post.to_json()
		trakt_id.update(progress=100, app_version="1.0",date="2015-03-07")
		encodedData = json.dumps(trakt_id)
		request = Request('https://api-v2launch.trakt.tv/scrobble/stop', data=encodedData, headers=HEADERS)
		resp = urlopen(request).getcode()
		if (resp == 201):
			print str(title)+ " " + str(season) +" "+ str(episode_num) + " Successfully scrobbled"
		else:
			print 'Error: '+ str(resp)

def updateDatabase(episodes, args):
	dbConnection = sql.connect(args.database_file)
	newEpisodes = []
	with dbConnection:
		dbCursor = dbConnection.cursor()
		dbCursor.execute("SELECT (episodetvdbid) from episodes order by id DESC limit 200")
		ids = dbCursor.fetchall()
		ids = [id[0] for id in ids]
		# print ids, episodes[-1]
		for episode in episodes:
			if not (episode[-1] in ids):
				newEpisodes.append(episode)
				if not (args.dont_store):
					dbCursor.execute("INSERT INTO episodes (date, seriesname, seriestvdbid, season, episode, episodetitle, episodetvdbid) VALUES (?,?,?,?,?,?,?)", (int(datetime.datetime.now().strftime("%s")),) + episode)
					print "Inserted", episode
		dbConnection.commit()
	return newEpisodes

<<<<<<< HEAD
def updateCache(data,showName,showTitle,showTVDBId):
	data.update({showName.lower(): {'title' : showTitle, 'tvdb':showTVDBId}})
	return data

def getTraktEpisodeInfo(showName, seasonNumber, episodeNumber, cache, seriesWhitelist, seriesMismatched):
    print showName, seasonNumber, episodeNumber
    if (showName.lower() in cache):
        showTvDbId = cache[showName.lower()]['tvdb']
        showName = cache[showName.lower()]['title']
    elif (showName in seriesMismatched):
        showRes = showName
        showName = seriesMismatched[showName]
        showTvDbId = TVShow('"'+ showName +'"').tvdb
        cache = updateCache(cache,showRes,showName,showTvDbId) 
=======
def getTraktEpisodeInfo(showName, seasonNumber, episodeNumber, seriesWhitelist, seriesMismatched):
    print showName, seasonNumber, episodeNumber
    if (showName in seriesMismatched):
        showName = seriesMismatched[showName]
        showTvDbId = TVShow('"'+ showName +'"').tvdb
>>>>>>> a27d471015deb86c5c7f7b8495c6103f4bdf9e85
    elif (showName in seriesWhitelist):
        showTvDbId = seriesWhitelist[showName]
    else:
        showName = showName.replace("(", "").replace(")", "").replace(":", "")
        showRes = TVShow.search('"'+ showName +'"')
        for showFound in showRes:
            if showName.lower() == showFound.title.lower():
<<<<<<< HEAD
                cache = updateCache(cache,showName,showFound.title,showFound.tvdb)
=======
>>>>>>> a27d471015deb86c5c7f7b8495c6103f4bdf9e85
                showName = showFound.title
                showTvDbId = showFound.tvdb
                break
        else:
            # Cannot find exact show name in trakt.tv search results so use 1st entry
<<<<<<< HEAD
            cache = updateCache(cache,showName,showRes[0].title,showRes[0].tvdb)
            showName = showRes[0].title
            showTvDbId = showRes[0].tvdb
			
    print showName, showTvDbId, seasonNumber, episodeNumber
    episode = TVEpisode(showName, seasonNumber, episodeNumber)
    #print episode.show, showTvDbId, seasonNumber, episodeNumber, episode.title, episode.tvdb
=======
            showName = showRes[0].title
            showTvDbId = showRes[0].tvdb
    print showName, showTvDbId, seasonNumber, episodeNumber
    episode = TVEpisode(showName, seasonNumber, episodeNumber)
    # print episode.show, showTvDbId, seasonNumber, episodeNumber, episode.title, episode.tvdb
>>>>>>> a27d471015deb86c5c7f7b8495c6103f4bdf9e85
    return (showName, showTvDbId, seasonNumber, episodeNumber, episode.title, episode.tvdb)

def jsonParser(file):
	data_file = open(file)
	data = json.load(data_file)
	data_file.close()
	return data

def getLastViewedContent(path):
	content = os.listdir(path)
	if '.metadata' in content: content.remove('.metadata')
	return content

def getEpisodesFromFiles(files):
	episodeList = []
	for entry in files:
		episodeInfo = episodeMatcher.getEpisodeInfo(entry)
		if (episodeInfo != (None, None, None)):
			episodeList.append(episodeInfo)
	return episodeList

def main(args):
	cache={}
	if (args.restart_djmount):
		djmountHandler.cleanUp(args.mount_path)
	path = djmountHandler.mountFolder(args.mount_path)
	path = os.path.join(path, r''+args.path_to_last_viewed+'')

	files = getLastViewedContent(path)
	rawEpisodes = getEpisodesFromFiles(files)
	traktCredentials = jsonParser(args.trakt_config_json)
	trakt.api_key = traktCredentials['api_key']
	seriesWhitelist = jsonParser(args.series_whitelist_json)
	seriesMismatched = jsonParser(args.series_mismatched_json)
	episodes = [getTraktEpisodeInfo(episode[0], episode[1], episode[2], cache,seriesWhitelist=seriesWhitelist, seriesMismatched=seriesMismatched) for episode in rawEpisodes]
	newEpisodes = updateDatabase(episodes, args)
	if (args.dont_post):
		if (newEpisodes == []):
			print "No new shows since last check."
		else:
			print "New shows since last check"
			for episode in newEpisodes:
				print episode
	else: # not (args.dont_post)
		postNewEpisodesToTrakt(newEpisodes)
<<<<<<< HEAD
	print (cache)
=======
>>>>>>> a27d471015deb86c5c7f7b8495c6103f4bdf9e85

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Monitors a UPnP Last Viewed folder for changes, writes into a database and posts to trakt.tv.', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
	parser.add_argument('--dont-store', action='store_true', help="Don't store to database but print out potential database changes instead.")
	parser.add_argument('--dont-post', action='store_true', help="Don't post to trakt.tv but print out possible database changes instead.")
	parser.add_argument('--restart-djmount', action='store_true', help="Unmount and delete the UPnP FUSE folder and kill all djmount processes before reinitialize them again.")
	parser.add_argument('--mount-path', type=str, default=".upnpDevices", help="Folder where the UPnP FUSE content will be mounted in via djmount.")
	parser.add_argument('--path-to-last-viewed', type=str, default=r"Serviio (SERVERNAME)/Video/Last Viewed", help="Path to monitored Last Viewed folder, beginning from djmount's mount point.")
	parser.add_argument('--database-file', type=str, default="episodes.db", help="Database file name.")
	parser.add_argument('--trakt-config-json', type=str, default="trakt-config.json", help="Trakt.tv login and API credentials JSON file.")
	parser.add_argument('--series-whitelist-json', type=str, default="seriesWhitelist.json", help="File with list of TVDB IDs of shows which just won't parse properly through trakt.tv's search.")
	parser.add_argument('--series-mismatched-json', type=str, default="seriesMismatched.json", help="Sometimes, your UPnP server displays the wrong show name. This file provides the proper names for mismatched ones.")
	# add parser argument to pass custom regex string for episode matching
	# add ability to parse all parameters from json file
	args = parser.parse_args()
	# print args
	main(args)
