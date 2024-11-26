#!/usr/bin/env python3

from fastapi import Request, FastAPI
from typing import Optional
from pydantic import BaseModel
import pandas as pd
import json
import os
import math
import mysql.connector
import uvicorn
from mysql.connector import Error
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")  # zone apex
def zone_apex():   
    return {"Hello": "my best friend!"}

DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "tpg6hu"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()
    
@app.get('/genres')
async def get_genres():
    try:
        db = mysql.connector.connect(
            user=DBUSER,
            host=DBHOST,
            password=DBPASS,
            database=DB, 
            ssl_disabled=True
        )
        cur = db.cursor()
        
        query = "SELECT * FROM genres ORDER BY genreid;"
    
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()

        json_data = [dict(zip(headers, result)) for result in results]
        return json_data
    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))
        return {"Error": "MySQL Error: " + str(e)}
    finally:
            cur.close()
            db.close() 
    

@app.get('/songs')
async def get_songs():
    try:
        db = mysql.connector.connect(
            user=DBUSER,
            host=DBHOST,
            password=DBPASS,
            database=DB,
            ssl_disabled=True
        )
        cur = db.cursor()

        query = """
        SELECT
            songs.title,
            songs.album,
            songs.artist,
            songs.year,
            songs.file,
            songs.image,
            genres.genre
        FROM
            songs
        JOIN
            genres ON songs.genre = genres.genreid
        ORDER BY
            songs.title;
        """

        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()

        json_data = [dict(zip(headers, result)) for result in results]
        return json_data
    except mysql.connector.Error as e:
        print("MySQL Error:", str(e))
        return {"Error": "MySQL Error: " + str(e)}
    finally:
            cur.close()
            db.close()

