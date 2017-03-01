# encoding=utf8
import codecs
import json
import os
import ast
import re

from semanticpy.vector_space import VectorSpace









repo = "/Users/mehranhassani/repos/nova/"
if not os.path.exists("files_str.json"):
    py_files_str = dict()
    for root, dirs, files in os.walk(repo):
                for file in files:
                    if file.endswith(".py"):
                        # print os.path.join(root, file)
                        with codecs.open(os.path.join(root, file), "r") as pyFile:
                            sourcestr = pyFile.read()
                            source = sourcestr.split("\n")
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
                            text = names+comments.split(" ")
                            py_files_str[os.path.join(root, file)]= [item for item in text if item !='']
                            # for function in [node for node in file_ast.body if isinstance(node, ast.FunctionDef)]:
                            #     if ast.get_docstring(function):
                            #         comments += "\n"+ast.get_docstring(function)
    save_files_str = open("files_str.json","w")
    json.dump(py_files_str, save_files_str)
else:
    py_files_str = json.loads(open("files_str.json","r").read())


if not os.path.exists("file_vs.json"):
    py_file_VS = dict()
    for key,text in py_files_str.iteritems():
        break_dash_text=[]
        for word in text:
            if "_" in word:
                break_dash_text.extend(word.split("_"))
            else:
                break_dash_text.append(word)
        file_vector_space = VectorSpace(break_dash_text, transforms=[])
        py_file_VS[key]=file_vector_space
    save_files_vs = open("files_vs.json", "w")
    json.dump(py_file_VS, save_files_vs)


