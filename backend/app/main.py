from fastapi import FastAPI
import os

app = FastAPI()


@app.get('/')
def index():
    return {'Hello': 'World'}
