# encoding=utf8
import codecs
import json,pickle
import os
import ast
import re
import logging
from bs4 import BeautifulSoup

import requests

logging.basicConfig(format='%(asctime)s %(message)s')




repo = "/Users/mehranhassani/repos/nova/"

counter=0
# logging.warning('start extracting words from files')
# file_counter=0
# for root, dirs, files in os.walk(repo):
#             for file in files:
#                 if file.endswith(".py"):
#                     # print os.path.join(root, file)
#                     with codecs.open(os.path.join(root, file), "r") as pyFile:
#                         sourcestr = pyFile.read()
#                         if "blue" in sourcestr:
#                             print file
#                             file_counter+=1
#                             print file_counter

blueprints_json = open("json_metadata.json","r").read().split("\n")
for blueprint in blueprints_json:
        data = json.loads(blueprint)
        if '/nova/' in data['self_link']:
            # bugs = json.loads(requests.get(data['bugs_collection_link']).text)
            # if bugs['total_size']>0:
            #     counter+=1
            #     print data['self_link'],bugs['total_size']
            if data['whiteboard'] and "Addressed by" in data['whiteboard'] and data['specification_url']:
                print data['self_link'],data['whiteboard']
                counter += 1
print counter