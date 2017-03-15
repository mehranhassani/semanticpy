# encoding=utf8
import codecs
import json,pickle
import os
import ast
import re
from bs4 import BeautifulSoup

import requests

from semanticpy.vector_space import VectorSpace

import logging
logging.basicConfig(format='%(asctime)s %(message)s')


def get_related_docs(rating_list,id,cut,threshold):
    related = []
    if id>cut:
        for score in range(0,cut):
            if rating_list[score]>threshold:
                related.append(score)
    else:
        for score in range(cut,len(rating_list)):
            if rating_list[score]>threshold:
                related.append(score)
    return related
def getWords(text):
    return re.compile('\w+').findall(text)







file_counter=1541
repo = "/Users/mehranhassani/repos/nova/"
words_list = []
word_file_bp_map = dict()
if not os.path.exists("text.json") or True:
    logging.warning('start extracting words from files')
    file_counter=0
    for root, dirs, files in os.walk(repo):
                for file in files:
                    if file.endswith(".py"):
                        # print os.path.join(root, file)
                        with codecs.open(os.path.join(root, file), "r") as pyFile:
                            sourcestr = pyFile.read()
                            source = sourcestr.split("\n")

                            #remove licence
                            for line_index in range(0,len(source)):
                                if source[0].startswith("#"):
                                    del source[0]
                                else:
                                    break
                            source = "\n".join(source)
                            file_ast = ast.parse(source)
                            names = sorted({node.id for node in ast.walk(file_ast) if isinstance(node, ast.Name)})
                            comments = '\n'.join(re.findall(r'\"\"\"(.*)\"\"\"',source))
                            comments += '\n'.join(re.findall(r'\#(.*)',source))
                            text = names+getWords(comments)
                            words = ' '.join(text).replace("_","")
                            if words !='':
                                words_list.append(words)
                                word_file_bp_map[words] = os.path.join(root, file)
                                file_counter+=1

    logging.warning('start extracting words from blueprints')
    blueprints_json = open("json_metadata.json","r").read().split("\n")
    for blueprint in blueprints_json:
        data = json.loads(blueprint)
        if '/nova/' in data['self_link']:
            words = ' '.join(getWords(data['summary'] + data['title']))
            #add linked spec to the words
            if data['specification_url']:
                try:
                    spec_link = requests.get(data['specification_url'])
                except Exception as e:
                    print e
                if spec_link.status_code<400:
                    soup = BeautifulSoup(spec_link.text)
                    words+=' '.join([i.text for i in soup.find_all('p')])
            words_list.append(words)
            word_file_bp_map[words]=data['bugs_collection_link']
    text_file = open("text.json","wb")
    map_file =  open("map.json","wb")
    pickle.dump(words_list,text_file)
    pickle.dump(word_file_bp_map,map_file)
    text_file.close()
    map_file.close()
text_file = open("text.json","rb")
map_file =  open("map.json","rb")
words_list = pickle.load(text_file)
word_file_bp_map = pickle.load(map_file)
if not os.path.exists("VSM.pickle"):
    VS  = VectorSpace(words_list)
    save_vs = open("VSM.pickle", "wb")
    logging.warning('start writing file for vector_space ')
    pickle.dump(VS, save_vs)
    logging.warning('end writing file for vector_space ')
    save_vs.close()
VS_file = open("VSM.pickle", "rb")
logging.warning('start reading file for files_vector_space ')
VS = pickle.load(VS_file)
logging.warning('end reading file for files_vector_space ')

for i in range(file_counter,len(words_list)):
    related = get_related_docs(VS.related(i),i,file_counter,0.5)
    if related:
        print "######"
        print word_file_bp_map[words_list[i]]
        print "related:"
        for r in related:
            print word_file_bp_map[words_list[r]]
