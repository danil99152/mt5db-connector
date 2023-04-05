from datetime import datetime

from fastapi import APIRouter, Request
from pydantic import BaseModel
from sqlalchemy import select, delete, insert, update
from starlette.responses import JSONResponse

from exceptions import Exceptions
from service.models import atimex_options, position, engine

router = APIRouter(prefix='/investor')


class Position(BaseModel):
    leader_pk: int
    ticket: int
    time: int
    time_update: int
    type: int
    magic: int
    volume: float
    price_open: float
    tp: float
    sl: float
    price_current: float
    symbol: str
    comment: str
    price_close: float
    time_close: int
    active: bool


# for investors
@router.get('/get-positions/', response_class=JSONResponse)
async def get_positions(leader_id: int) -> list | str:
    try:
        statement = select(position).where(position.c.leader_pk == leader_id)
        result = engine.connect().execute(statement).fetchall()
        response = []
        for i in result:
            response.append([*i])
        return response
    except Exception as e:
        Exceptions().get_exception(e)


# for investors
@router.get('/get-position/', response_class=JSONResponse)
async def get_position(leader_id: int, ticket: int) -> list | str:
    try:
        statement = select(position).where(position.c.ticket == ticket and position.c.leader_pk == leader_id)
        result = engine.connect().execute(statement).fetchall()
        return [*result[0]]
    except Exception as e:
        Exceptions().get_exception(e)


# for leader
@router.post('/post-position/', response_class=JSONResponse)
async def post_position(request: Position) -> str:
    # for example, request can be like that:
    # {
    #     "leader_pk": 0,
    #     "ticket": 0,
    #     "time": 0,
    #     "time_update": 0,
    #     "type": 0,
    #     "magic": 0,
    #     "volume": 0,
    #     "price_open": 0,
    #     "tp": 0,
    #     "sl": 0,
    #     "price_current": 0,
    #     "symbol": "string",
    #     "comment": "string",
    #     "price_close": 0,
    #     "time_close": 0,
    #     "active": true
    # }

    try:
        statement = insert(position).values(request.dict())
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Posted"
    except Exception as e:
        engine.connect().close()
        return Exceptions().post_exception(e)


# for leader
@router.patch('/patch-position/', response_class=JSONResponse)
async def patch_position(leader_id: int, ticket: int, request: dict) -> str:
    # for example, request can be like that:
    # {
    #     "profit": 600
    # }

    try:
        statement = update(position).where(position.c.ticket == ticket
                                           and position.c.leader_pk == leader_id).values(request)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Patched"
    except Exception as e:
        return Exceptions().patch_exception(e)


# for leader
@router.delete('/delete-position/', response_class=JSONResponse)
async def delete_position(leader_id: int, ticket: int) -> str:
    try:
        statement = delete(position).where(position.c.ticket == ticket and position.c.leader_pk == leader_id)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Position deleted"
    except Exception as e:
        return Exceptions().delete_exception(e)


# for investors
@router.get('/get-option/', response_class=JSONResponse)
async def get_option(option_id: int) -> list | str:
    try:
        statement = select(atimex_options).where(atimex_options.c.atimex_options_pk == option_id)
        result = engine.connect().execute(statement).fetchall()
        return [*result[0]]
    except Exception as e:
        return Exceptions().get_exception(e)


# for investors
@router.get('/get-options/', response_class=JSONResponse)
async def get_options() -> list | str:
    try:
        statement = select(atimex_options)
        result = engine.connect().execute(statement).fetchall()
        response = []
        for i in result:
            response.append([*i])
        return response
    except Exception as e:
        return Exceptions().get_exception(e)


# for investors
@router.get('/get-positions/active/', response_class=JSONResponse)
async def get_active_positions(leader_id: int) -> list | str:
    try:
        statement = select(position).where(position.c.active is True and position.c.leader_pk == leader_id)
        result = engine.connect().execute(statement).fetchall()
        response = []
        for i in result:
            response.append([*i])
        return response
    except Exception as e:
        return Exceptions().get_exception(e)
