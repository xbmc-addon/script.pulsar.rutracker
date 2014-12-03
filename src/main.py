# -*- coding: utf-8 -*-

import os, sys, time

from pulsar import provider

try:
    sys.path.insert(0, os.path.dirname(__file__) + '/../plugin.rutracker/')
    from default import CONTENT
    from drivers.rutracker import RuTracker
    sys.path.pop(0)
    ENABLED = True
except ImportError, e:
    ENABLED = False



def rutracker_search(query, content=None):
    if not ENABLED:
        return []
    rutracker = RuTracker()
    if content:
        index = CONTENT[content]['index']
        ignore = CONTENT[content]['ignore']
    else:
        index, ignore = [], []
        for ind, ign in [(x['index'], x['ignore']) for x in CONTENT.values() if x['media'] == 'video']:
            index.extend(ind)
            ignore.extend(ign)

    data = rutracker.search(search=query, index=index, ignore=ignore)
    if data and not data['data']:
        return []
    result = []
    start_time = time.time()
    for item in [x for x in data['data'] if x['type'] == 'torrent']:
        magnet = rutracker.magnet(item['id'])
        if magnet:
            result.append({
                'uri': magnet,
                #'trackers': [], TODO: надо разобраться что сюда пихать - толи просто домен серверов, то ли полный URL для анонса
                'name': item['name'],
                'size': item['size'],
                'seeds': item['seeder'],
                'peers': item['seeder'] + item['leecher'],
                'language': 'ru'
                # 'resolution': 'int', TODO: все что ниже оставленно до лучших времен
                # 'video_codec': 'int',
                # 'audio_codec': 'int',
                # 'rip_type': 'int',
                # 'scene_rating': 'int'
            })
            if time.time() - start_time > 1.5:
                break
    return result




# for Pulsar

def search(query):
    return rutracker_search(query)


def search_episode(episode):
    return search("%(title)s S%(season)02dE%(episode)02d" % episode)


def search_movie(movie):
    return rutracker_search(movie['title'], 'movie')


# This registers your module for use
provider.register(search, search_movie, search_episode)
