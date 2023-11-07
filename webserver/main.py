from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.requests import Request
from pydantic import BaseModel
import redis
import os

app = FastAPI()

redisClient = redis.StrictRedis(host=os.environ.get("REDIS_HOST"),
                                port=6379,
                                db=0)
hash_name = "test"


class Item(BaseModel):
    key: str
    value: str


def key_value_streamer():
    for key in redisClient.scan_iter():
        yield key


@app.post('/create')
async def create_key_value(item: Item):
    redisClient.hset(hash_name, item.key, item.value)
    return item


@app.get('/list')
async def main():
    return StreamingResponse(key_value_streamer(), media_type='text/event-stream')
