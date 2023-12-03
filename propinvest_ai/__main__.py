import json

import requests
from fastapi import BackgroundTasks, FastAPI, Request
from pydantic import Json

from propinvest_ai.chat import get_answer
from propinvest_ai.settings import settings

app = FastAPI()


def send_answer(req_id: str, payload: dict):
    data = get_answer(json.dumps(payload))
    try:
        requests.post(settings.web_hook, json={"req_id": req_id, "giga": data})
    except Exception as ex:
        print(ex)


@app.post("/webhook/{req_id}")
async def webhook(
    req_id: str, req: Request, background_tasks: BackgroundTasks
):
    data = json.loads(json.dumps(await req.json(), ensure_ascii=False))
    background_tasks.add_task(send_answer, req_id, data)
    return dict(message="pong")
