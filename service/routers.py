from datetime import datetime

from fastapi import APIRouter, Request
from pydantic import BaseModel
from sqlalchemy import select, delete, insert, update
from starlette.responses import JSONResponse

from service.models import atimex_options, position, engine

router = APIRouter(prefix='/investor')


class Position(BaseModel):
    leader_pk: int
    ticket: int
    time: datetime
    type: str
    volume: float
    sell_price: float
    buy_price: float
    profit: float


# for investors
@router.get('/get-positions/', response_class=JSONResponse)
async def get_positions():
    try:
        statement = select(position)
        result = engine.connect().execute(statement).fetchall()
        response = []
        for i in result:
            response.append([*i])
        return response
    except Exception as e:
        return f"Cannot get it because {e}"


# for investors
@router.get('/get-position/', response_class=JSONResponse)
async def get_position(ticket: int):
    try:
        statement = select(position).where(position.c.ticket == ticket)
        result = engine.connect().execute(statement).fetchall()
        return [*result[0]]
    except Exception as e:
        return f"Cannot get it because {e}"


# for leader
@router.post('/post-position/', response_class=JSONResponse)
async def post_position(request: Position):
    # for example, request can be like that:
    # {
    #   "leader_pk": 0,
    #   "ticket": 0,
    #   "time": "2023-04-01T00:47:06.104Z",
    #   "type": "string",
    #   "volume": 0,
    #   "sell_price": 0,
    #   "buy_price": 0,
    #   "profit": 0
    # }

    try:
        statement = insert(position).values(request.dict())
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Posted"
    except Exception as e:
        return f"Wasn't posted because {e}"


# for leader
@router.patch('/patch-position/', response_class=JSONResponse)
async def patch_position(ticket: int, request: dict):
    # for example, request can be like that:
    # {
    #     "profit": 600
    # }

    try:
        statement = update(position).where(position.c.ticket == ticket).values(request)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Patched"
    except Exception as e:
        return f"Wasn't patched because {e}"


# for leader
@router.delete('/delete-position/', response_class=JSONResponse)
async def delete_position(ticket: int):
    try:
        statement = delete(position).where(position.c.ticket == ticket)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Position deleted"
    except Exception as e:
        return f"Position was not deleted because {e}"


# for investors
@router.get('/get-option/', response_class=JSONResponse)
async def get_option(option_id: int):
    try:
        statement = select(atimex_options).where(atimex_options.c.atimex_options_pk == option_id)
        result = engine.connect().execute(statement).fetchall()
        return [*result[0]]
    except Exception as e:
        return f"Cannot get it because {e}"


# for investors
@router.get('/get-options/', response_class=JSONResponse)
async def get_options():
    try:
        statement = select(atimex_options)
        result = engine.connect().execute(statement).fetchall()
        response = []
        for i in result:
            response.append([*i])
        return response
    except Exception as e:
        return f"Cannot get it because {e}"
