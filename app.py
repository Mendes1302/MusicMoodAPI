from fastapi.middleware.cors import CORSMiddleware
from os.path import dirname, join, abspath
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List
from sys import path

current_script_path = abspath(__file__)
project_root = dirname(dirname(current_script_path))
affective_computing_path = join(project_root, 'AffectiveComputing')
path.insert(0, affective_computing_path)
from libs.pre_processing import PreProcessing
from libs.sqlite_manager import Sqlite

PATH_DATABASE = affective_computing_path+"/songs_database.db"

# Configuração do FastAPI
app = FastAPI(
    title="Music MoodAI",
    version="1.0.0"
)

# Configuração do CORS
origins = [
    "http://localhost",
    "http://localhost:8080",  
]

# Configuração do CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],  
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Rotas da API
@app.get("/")
async def root():
    return {"root": "Hello, Welcome!"}

@app.get("/name_emotion")
async def get_name_emotion():
    sql3 = Sqlite(database=PATH_DATABASE)
    inputs = sql3.get_by_select(query='SELECT name_emotion, description, synonym_emotion FROM emotion;')
    inputs = inputs.to_dict(orient='records')    
    return inputs

@app.get("/lyrics")
async def get_lyrics():
    sql3 = Sqlite(database=PATH_DATABASE)
    inputs = sql3.get_by_select(query='SELECT song_name, lyrics, vagalume_song_url FROM song')
    inputs = inputs.to_dict(orient='records')    
    return inputs

@app.get("/songs_name")
async def get_song_name():
    sql3 = Sqlite(database=PATH_DATABASE)
    query = """SELECT s.song_id, s.song_name || ' - ' || a.artist_full_name AS song_name, er.value, er.emotion
                FROM song s
                INNER JOIN artist a ON s.song_id = a.song_id
                INNER JOIN emotional_result er ON s.song_id = a.song_id;"""
    inputs = sql3.get_by_select(query)
    inputs = inputs.to_dict(orient='records')    
    return inputs


@app.get("/emotional_result")
async def get_emotional_result(q: str = Query(None, min_length=2)):
    sql3 = Sqlite(database=PATH_DATABASE)
    query = """SELECT s.song_id, s.song_name || ' - ' || a.artist_full_name AS song_name, er.value, er.emotion, er.model_name
                FROM song s
                INNER JOIN artist a ON s.song_id = a.song_id
                INNER JOIN emotional_result er ON s.song_id = er.song_id;"""
    inputs = sql3.get_by_select(query)

    if q:
        inputs = inputs[inputs['song_name'].str.contains(q, case=False, na=False)]

    inputs = inputs.to_dict(orient='records')
    return inputs

@app.get("/get_sources")
async def get_sources():
    sql3 = Sqlite(database=PATH_DATABASE)
    query = f"""SELECT e.name_emotion, i.source FROM inputs i 
                INNER JOIN emotion e ON i.emotion_id = e.emotion_id"""
    inputs = sql3.get_by_select(query=query)
    inputs = inputs.to_dict(orient='records')    
    return inputs

@app.get("/get_sources_emotions")
async def get_sources():
    sql3 = Sqlite(database=PATH_DATABASE)
    query = f"""SELECT e.name_emotion, COUNT(*) AS count
                FROM inputs i
                INNER JOIN emotion e ON i.emotion_id = e.emotion_id
                GROUP BY e.name_emotion;"""
    inputs = sql3.get_by_select(query=query)
    inputs = inputs.to_dict(orient='records')    
    return inputs


# Execução da aplicação
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
