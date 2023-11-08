from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
import redis
import os
import time
import logging

app = FastAPI()

redis_client = redis.StrictRedis(host=os.environ.get("REDIS_HOST"),
                                 port=6379,
                                 db=0)

hash_name = "test"
ttl = os.environ.get("TTL")
redis_client.expire(hash_name, ttl)


class Item(BaseModel):
    key: str
    value: str


def key_value_streamer():
    for key in range(10):
        yield key
        time.sleep(1)


@app.post('/create')
async def create_key_value(item: Item):
    redis_client.hset(hash_name, item.key, item.value)
    return item


@app.get('/list')
async def main():
    return StreamingResponse(key_value_streamer(), media_type='text/event-stream')
