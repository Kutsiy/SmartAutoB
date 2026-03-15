from collections.abc import AsyncIterable, Iterable
from fastapi import APIRouter
from sse_starlette.sse import EventSourceResponse
from pydantic import BaseModel
import asyncio

notify_router = APIRouter(prefix="/notify")

class Item(BaseModel):
    name: str
    description: str | None


items = [
    Item(name="Plumbus", description="A multi-purpose household device."),
    Item(name="Portal Gun", description="A portal opening device."),
    Item(name="Meeseeks Box", description="A box that summons a Meeseeks."),
]

async def generator():
    index = 0
    while True:
        while index < len(items):
            yield items[index].json()
            index+=1
        await asyncio.sleep(1)

@notify_router.get('/add', response_class=EventSourceResponse)
def add():
    items.append(Item(name="Meeseeks Box", description="A box that summons a Meeseeks."))

@notify_router.get('/message', response_class=EventSourceResponse)
def notify():
    return EventSourceResponse(generator())