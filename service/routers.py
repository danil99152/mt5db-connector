import json
import os

import requests
from fastapi import APIRouter
from sqlalchemy import select, delete, insert, update, and_
from starlette.responses import JSONResponse

from exceptions import Exceptions
from service.configs import Position, Options, Exchange, PositionHistory, ConnectData
from service.models import atimex_options, position, engine, exchange, position_history, investor_leader, container
from settings import settings

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

@router.post('/data/post', response_class=JSONResponse)
async def post_data(request: ConnectData) -> JSONResponse:
    try:
        data = request.dict()
        investor_id = data.get('investor_id')
        leader_ids = data.get('leaders_ids')
        history = json.loads(requests.get(settings.host_history).text)
        for exch in data.get('exchanges'):
            id = exch.get('id')
            investment_size = sum([d.get('investment') for d in history if d['user_id'] == id])
            type = 'investor' if id == investor_id else 'leader' if id in leader_ids else 'None'
            option = next((item for item in data.get('options') if item["user_id"] == id), None)
            exchanges_data = {
                "exchange_pk": id,
                "login": exch.get('api_key'),
                "password": exch.get('api_secret'),
                "server": exch.get('server'),
                "balance": option.get('investment'),
                "equity": option.get('equity'),
                "investment_size": investment_size,
                "currency": option.get('currency'),
                "access_dcs": True,
                "type": type
            }
            exchange_result = await get_exchange(id)
            option_result = await get_option(id)
            exchange_values = Exchange(**exchanges_data).dict()
            if not exchange_result:
                insert_account = insert(exchange).values(exchange_values)
                with engine.connect() as conn:
                    conn.execute(insert_account)
                    conn.commit()

                if type == "leader":
                    os.system(f"docker run -e ACCOUNT_ID={id} "
                              f"--name mt_leader{id} "
                              f"205b28d28c91f81522f6f4335ae77aaac20c58645ad8be3d1a4e4f63380ed3b1")
                    os.system(f"docker exec -it mt_leader{id} start_leader.sh")
                    os.system(f"docker exec -it mt_leader{id} chmod +x /start_leader.sh")

                    container_data = {
                        "exchange_pk": id,
                        "name": f"mt_leader{id}",
                    }
                    insert_relate = insert(container).values(container_data)
                    with engine.connect() as conn:
                        conn.execute(insert_relate)
                        conn.commit()
                elif type == "investor":
                    os.system(f"docker run -e ACCOUNT_ID={id} "
                              f"--name mt_investor{id} "
                              f"205b28d28c91f81522f6f4335ae77aaac20c58645ad8be3d1a4e4f63380ed3b1")
                    os.system(f"docker exec -it mt_investor{id} start_investor.sh")
                    os.system(f"docker exec -it mt_investor{id} chmod +x /start_investor.sh")

                    container_data = {
                        "exchange_pk": id,
                        "name": f"mt_investor{id}",
                    }
                    insert_relate = insert(container).values(container_data)
                    with engine.connect() as conn:
                        conn.execute(insert_relate)
                        conn.commit()

            elif list(exchange_result) != list(exchange_values.values()):
                update_exchange = update(exchange).where(exchange.c.exchange_pk == id).values(exchange_values)
                with engine.connect() as conn:
                    conn.execute(update_exchange)
                    conn.commit()

            option_values = Options(**option).dict()
            if not option_result:
                insert_options = insert(atimex_options).values(option_values)
                with engine.connect() as conn:
                    conn.execute(insert_options)
                    conn.commit()
            elif list(option_result) != list(option_values.values()):
                update_option = update(atimex_options).where(atimex_options.c.investor_pk == id).values(option_values)
                with engine.connect() as conn:
                    conn.execute(update_option)
                    conn.commit()

        for lead in leader_ids:
            relate_result = await get_relate(investor_id, lead)
            if not relate_result:
                data = {
                    "investor_id": investor_id,
                    "leader_id": lead,
                }
                insert_relate = insert(investor_leader).values(data)
                with engine.connect() as conn:
                    conn.execute(insert_relate)
                    conn.commit()

        return JSONResponse(content={'result': 'ok'})
    except Exception as e:
        return JSONResponse(content={'result': e})
