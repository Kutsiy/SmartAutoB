from fastapi import APIRouter

notify_router = APIRouter(prefix="/notify")

@notify_router.get('/massege')
def notify():
    pass