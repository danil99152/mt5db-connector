from typing import List, Dict, Any

from fastapi import APIRouter
from sqlalchemy import select, delete, insert, update
from starlette.responses import JSONResponse

from exceptions import Exceptions
from service.configs import Position, Options
from service.models import atimex_options, position, engine, account

router = APIRouter()


# for investors
@router.get('/position/list/', response_class=JSONResponse)
async def get_positions(leader_id: int) -> list[dict] | str:
    try:
        statement = select(position).where(position.c.leader_pk == leader_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(Position.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        Exceptions().get_exception(e)


# for investors
@router.get('/position/list/active/', response_class=JSONResponse)
async def get_active_positions(leader_id: int) -> list[dict] | str:
    try:
        statement = select(position).where(position.c.active == True and position.c.leader_pk == leader_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(Position.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        return Exceptions().get_exception(e)


# for investors
@router.get('/position/get/', response_class=JSONResponse)
async def get_position(leader_id: int, ticket: int) -> list[dict] | str:
    try:
        statement = select(position).where(position.c.ticket == ticket and position.c.leader_pk == leader_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(Position.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        Exceptions().get_exception(e)


# for leader
@router.post('/position/post', response_class=JSONResponse)
async def post_position(request: dict) -> str:
    # for example, request can be like that:
    # {
    #     "leader_pk": 1,
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
        statement = insert(position).values(request)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Posted"
    except Exception as e:
        engine.connect().close()
        return Exceptions().post_exception(e)


# for leader
@router.patch('/position/patch/', response_class=JSONResponse)
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


@router.patch('/account/patch/', response_class=JSONResponse)
async def patch_account(account_id: int, request: dict) -> str:
    try:
        statement = update(account).where(account.c.account_pk == account_id).values(request)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Patched"
    except Exception as e:
        return Exceptions().patch_exception(e)


@router.patch('/account/get/', response_class=JSONResponse)
async def get_account(account_id: int) -> list[dict] | str:
    try:
        statement = select(account).where(account.c.account_pk == account_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(Position.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        Exceptions().get_exception(e)

# for leader
@router.delete('/position/delete/', response_class=JSONResponse)
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
@router.get('/option/get/', response_class=JSONResponse)
async def get_option(option_id: int) -> list[dict] | str:
    try:
        statement = select(atimex_options).where(atimex_options.c.id == option_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(Options.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        return Exceptions().get_exception(e)


# for investors
@router.get('/option/list/', response_class=JSONResponse)
async def get_options() -> list[dict] | str:
    try:
        statement = select(atimex_options)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(Options.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        return Exceptions().get_exception(e)
