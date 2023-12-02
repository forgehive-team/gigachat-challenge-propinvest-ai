from fastapi import FastAPI

from propinvest_ai.settings import settings

app = FastAPI()


@app.get("/")
def ping():
    return dict(message="pong")
