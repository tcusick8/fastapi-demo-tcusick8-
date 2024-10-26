#!/usr/bin/env python3

from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel
import json
import os
import math


app = FastAPI()

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
