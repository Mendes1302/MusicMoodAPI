from os.path import dirname, join, abspath
from json import loads
from os import environ
from sys import path
import pandas as pd

current_script_path = abspath(__file__)
project_root = dirname(dirname(current_script_path))
affective_computing_path = join(project_root, 'AffectiveComputing')
path.insert(0, affective_computing_path)
from libs.sqlite_manager import Sqlite
from libs.pre_processing import PreProcessing

path = affective_computing_path+"/songs_database.db"
print(path)

#print(environ['PATH_DATABASE'])
sql3 = Sqlite(database=path)
inputs = sql3.get_by_select(query='SELECT * FROM song;')
inputs.to_csv("data_songs.csv")
inputs = inputs.to_json(orient='records', force_ascii=False)
print()

