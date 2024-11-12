from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def start(name: str):
    return name



