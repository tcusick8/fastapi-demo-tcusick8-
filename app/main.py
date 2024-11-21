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


if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)


@app.get("/")  # zone apex
def zone_apex():
    return {"Hello": "my best friend!"}

@app.get("/add/{a}/{b}")
def add(a: int, b: int):
    return {"sum": a + b}

@app.get("/multiply/{c}/{d}")
def multiply (c: int, d: int):
    return {"product": c * d}

@app.get("/square/{e}")
def square(e: int):
    return {"product": e * e}

@app.get("/divide/{f}/{g}")
def divide(f: int, g: int):
    return {"quotient": f / g}

@app.get("/sqrt/{h}")
def sqrt(h: int):
    if h < 0:
        return {"error": "Cannot take the square root of a negative number"}
    return {"square_root": math.sqrt(h)}

@app.get("/power/{base}/{exponent}")
def power(base: int, exponent: int):
    return {"result": math.pow(base, exponent)}

@app.get("/customer/{idx}")
def customer(idx: int):
    #read the data into a df
    df = pd.read_csv("../customers.csv")
    #filter the data based on index
    customer = df.iloc[idx]
    return customer.to_dict()

@app.post("/get_body")
async def get_body(request: Request):
        return await request.json()




DBHOST = "ds2022.cqee4iwdcaph.us-east-1.rds.amazonaws.com"
DBUSER = "admin"
DBPASS = os.getenv('DBPASS')
DB = "tpg6hu"

db = mysql.connector.connect(user=DBUSER, host=DBHOST, password=DBPASS, database=DB)
cur=db.cursor()

@app.get('/genres')
def get_genres():
    query = "SELECT * FROM genres ORDER BY genreid;"
    try:    
        cur.execute(query)
        headers=[x[0] for x in cur.description]
        results = cur.fetchall()
        json_data=[]
        for result in results:
            json_data.append(dict(zip(headers,result)))
        return(json_data)
    except Error as e:
        return {"Error": "MySQL Error: " + str(e)}


@app.get('/songs')
def get_songs():
    query = """
    SELECT 
        songs.title AS title,
        songs.album AS album,
        songs.artist AS artist,
        songs.year AS year,
        CONCAT('http://tpg6hu-dp1-spotify.s3-website-us-east-1.amazonaws.com/, songs.file) AS file,
        CONCAT('http://tpg6hu-dp1-spotify.s3-website-us-east-1.amazonaws.com/', songs.image) AS image,
        genres.genre AS genre
    FROM 
        songs
    JOIN 
        genres ON songs.genre = genres.genreid
    ORDER BY 
        songs.title;
    """
    try:
        cur.execute(query)
        headers = [x[0] for x in cur.description]
        results = cur.fetchall()
        json_data = []
        for result in results:
            json_data.append(dict(zip(headers, result)))
        return json_data
    except mysql.connector.Error as e:
        return {"Error": "MySQL Error: " + str(e)}















