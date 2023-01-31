from fastapi import FastAPI, Body

app = FastAPI()

@app.get("/")
def hello_world() :
    return {"hello" : "world"}

