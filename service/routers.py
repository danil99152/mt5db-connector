from fastapi import APIRouter
from sqlalchemy import select, delete, insert, update, and_
from starlette.responses import JSONResponse

from exceptions import Exceptions
from service.configs import Position, Options, Exchange, PositionHistory
from service.models import atimex_options, position, engine, exchange, position_history, investor_leader

router = APIRouter()


# for investors
@router.get('/position/list/{exchange_id}/', response_class=JSONResponse)
async def get_positions(exchange_id: int) -> list[dict] | str:
    try:
        statement = select(position).where(position.c.exchange_pk == exchange_id)
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


@router.get('/position/list/all/', response_class=JSONResponse)
async def get_all_positions() -> list[dict] | str:
    try:
        statement = select(position)
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

@router.get('/relate/list/', response_class=JSONResponse)
async def get_relates() -> list | str:
    try:
        statement = select(investor_leader)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for value in result:
            response.append(int(value[0]))
        return response
    except Exception as e:
        return Exceptions().get_exception(e)

@router.get('/relate/get/{investor_id}/{leader_id}/', response_class=JSONResponse)
async def get_relate(investor_id: int, leader_id: int) -> list | str:
    try:
        statement = select(investor_leader).where(and_(investor_leader.c.investor_id == investor_id,
                                                       investor_leader.c.leader_id == leader_id))
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for value in result:
            response.append(int(value[0]))
        return response
    except Exception as e:
        return Exceptions().get_exception(e)


# for investors
@router.get('/position/list/active/{exchange_id}/', response_class=JSONResponse)
async def get_active_positions(exchange_id: int) -> list[dict] | str:
    try:
        statement = select(position).where(and_(position.c.active == True), (position.c.exchange_pk == exchange_id))
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
@router.get('/position/get/{exchange_id}/{ticket}/', response_class=JSONResponse)
async def get_position(exchange_id: int, ticket: int) -> list[dict] | str:
    try:
        statement = select(position).where(position.c.ticket == ticket and position.c.exchange_pk == exchange_id)
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


# for leader
@router.post('/position/post', response_class=JSONResponse)
async def post_position(request: Position) -> str:
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
@router.patch('/position/patch/{exchange_id}/{ticket}/', response_class=JSONResponse)
async def patch_position(exchange_id: int, ticket: int, request: dict) -> str:
    # for example, request can be like that:
    # {
    #     "profit": 600
    # }

    try:
        statement = update(position).where(position.c.ticket == ticket
                                           and position.c.exchange_pk == exchange_id).values(request)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Patched"
    except Exception as e:
        return Exceptions().patch_exception(e)


@router.patch('/exchange/patch/{exchange_id}/', response_class=JSONResponse)
async def patch_exchange(exchange_id: int, request: dict) -> str:
    try:
        statement = update(exchange).where(exchange.c.exchange_pk == exchange_id).values(request)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Patched"
    except Exception as e:
        return Exceptions().patch_exception(e)


@router.get('/exchange/get/{exchange_id}/', response_class=JSONResponse)
async def get_exchange(exchange_id: int) -> list[dict] | str:
    try:
        statement = select(exchange).where(exchange.c.exchange_pk == exchange_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(Exchange.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        return Exceptions().get_exception(e)


@router.get('/exchange/list/', response_class=JSONResponse)
async def get_exchanges() -> list[dict] | str:
    try:
        statement = select(exchange)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(Exchange.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        return Exceptions().get_exception(e)

@router.delete('/exchange/delete/{exchange_id}/', response_class=JSONResponse)
async def delete_position(exchange_id: int) -> str:
    try:
        statement = delete(exchange).where(exchange.c.exchange_pk == exchange_id)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Exchange deleted"
    except Exception as e:
        return Exceptions().delete_exception(e)

@router.post('/exchange/post', response_class=JSONResponse)
async def post_exchange(request: Exchange) -> str:
    try:
        statement = insert(exchange).values(request.dict())
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Posted"
    except Exception as e:
        engine.connect().close()
        return Exceptions().post_exception(e)


# for leader
@router.delete('/position/delete/{exchange_id}/{ticket}/', response_class=JSONResponse)
async def delete_exchange(exchange_id: int, ticket: int) -> str:
    try:
        statement = delete(position).where(position.c.ticket == ticket and position.c.exchange_pk == exchange_id)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Position deleted"
    except Exception as e:
        return Exceptions().delete_exception(e)


# for investors
@router.get('/option/get/{option_id}/', response_class=JSONResponse)
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


@router.delete('/position-history/delete/{ticket}', response_class=JSONResponse)
async def delete_position_history(ticket: int) -> str:
    try:
        statement = delete(position_history).where(position_history.c.ticket == ticket)
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Position deleted"
    except Exception as e:
        return Exceptions().delete_exception(e)


@router.get('/position-history/get/{ticket}/', response_class=JSONResponse)
async def get_position_history(ticket: int) -> list[dict] | str:
    try:
        statement = select(position_history).where(position_history.c.ticket == ticket)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(PositionHistory.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        return Exceptions().get_exception(e)


@router.get('/position-history/list/', response_class=JSONResponse)
async def get_position_history_list() -> list[dict] | str:
    try:
        statement = select(position_history)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            res = list(res)
            del res[0]
            d = {}
            for key, value in zip(PositionHistory.__annotations__, res):
                d[key] = value
            response.append(d)
        return response
    except Exception as e:
        return Exceptions().get_exception(e)


@router.post('/position-history/post', response_class=JSONResponse)
async def post_position_history(request: PositionHistory) -> str:
    try:
        statement = insert(position_history).values(request.dict())
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Posted"
    except Exception as e:
        engine.connect().close()
        return Exceptions().post_exception(e)


@router.get('/leader_id_by_investor/get/{investor_id}/', response_class=JSONResponse)
async def get_leader_id_by_investor_id(investor_id: int) -> list | str:
    try:
        statement = select(investor_leader.c.leader_id).where(investor_leader.c.investor_id == investor_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for value in result:
            response.append(int(value[0]))
        return response
    except Exception as e:
        return Exceptions().get_exception(e)

@router.get('/investor_id_by_leader/get/{leader_id}/', response_class=JSONResponse)
async def get_investor_id_by_leader_id(leader_id: int) -> list | str:
    try:
        statement = select(investor_leader.c.investor_id).where(investor_leader.c.leader_id == leader_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for value in result:
            response.append(int(value[0]))
        return response
    except Exception as e:
        return Exceptions().get_exception(e)
