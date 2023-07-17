# TODO add fields to container model like error (text), status (bool), updated_at (datetime) and crud method patch
import json
import subprocess

import requests
from fastapi import APIRouter
from sqlalchemy import select, delete, insert, update, and_
from starlette.responses import JSONResponse

from exceptions import Exceptions
from service.configs import Position, Options, Exchange, PositionHistory, Container
from service.models import option, position, engine, exchange, position_history, container
from settings import settings

router = APIRouter()


def dict_clean(items: dict):
    result = {}
    for key, value in items.items():
        if value is None:
            value = 0
        result[key] = value
    return result


def run_cms_container(id, type):
    subprocess.Popen(f"docker run "
                     f"-e EXCHANGE_ID={id} "
                     f"--name mt_{type}{id} "
                     f"{settings.investor_cms_image if type == 'investor' else settings.leader_cms_image}",
                     shell=True,
                     stdout=subprocess.PIPE)

    container_data = {
        "exchange_pk": id,
        "name": f"mt_{type}{id}",
        "is_leader": True if type == 'leader' else False,
        "is_cms": True
    }
    insert_relate = insert(container).values(container_data)
    with engine.connect() as conn:
        conn.execute(insert_relate)
        conn.commit()


def run_signal_container(id, type):
    subprocess.Popen(f"docker run "
                     f"-e EXCHANGE_ID={id} "
                     f"--name mt_{type}{id} "
                     f"{settings.investor_signal_image if type == 'investor' else settings.leader_signal_image}",
                     shell=True,
                     stdout=subprocess.PIPE)

    container_data = {
        "exchange_pk": id,
        "name": f"mt_{type}{id}",
        "is_leader": True if type == 'leader' else False,
        "is_cms": False
    }
    insert_relate = insert(container).values(container_data)
    with engine.connect() as conn:
        conn.execute(insert_relate)
        conn.commit()


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


# for investors
@router.get('/position/list/active/{exchange_id}/', response_class=JSONResponse)
async def get_active_positions(exchange_id: int) -> list[dict] | str:
    try:
        statement = select(position).where(and_(position.c.active), (position.c.exchange_pk == exchange_id))
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


@router.get('/position/list/not-active/{exchange_id}/', response_class=JSONResponse)
async def get_not_active_positions(exchange_id: int) -> list[dict] | str:
    try:
        statement = select(position).where(and_(position.c.active == False), (position.c.exchange_pk == exchange_id))
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
        statement = select(position).where(and_(position.c.ticket == ticket, position.c.exchange_pk == exchange_id))
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


@router.post('/position/post', response_class=JSONResponse)
async def post_position(request: Position) -> str:
    try:
        statement = insert(position).values(request.model_dump())
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Posted"
    except Exception as e:
        engine.connect().close()
        return Exceptions().post_exception(e)


@router.patch('/position/patch/{exchange_id}/{ticket}/', response_class=JSONResponse)
async def patch_position(exchange_id: int, ticket: int, request: dict) -> str:
    # for example, request can be like that:
    # {
    #     "profit": 600
    # }

    try:
        statement = update(position).where(and_(position.c.ticket == ticket,
                                                position.c.exchange_pk == exchange_id)).values(request)
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
async def post_exchange(request: dict) -> JSONResponse:
    try:
        history = json.loads(requests.get(settings.host_history).text)
        id = request.get('account_pk')
        try:
            investment_size = sum([d.get('investment') for d in history if d['user_id'] == id])
        except:
            investment_size = 0
        request['investment_size'] = investment_size
        request['access_dcs'] = True
        statement = insert(exchange).values(dict_clean(dict(request)))
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return JSONResponse(content={'exchange': 'posted'})
    except Exception as e:
        engine.connect().close()
        return Exceptions().post_exception(e)


@router.delete('/position/delete/{exchange_id}/{ticket}/', response_class=JSONResponse)
async def delete_exchange(exchange_id: int, ticket: int) -> str:
    try:
        statement = delete(position).where(and_(position.c.ticket == ticket, position.c.exchange_pk == exchange_id))
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Position deleted"
    except Exception as e:
        return Exceptions().delete_exception(e)


@router.get('/container/get/{exchange_id}/{type}', response_class=JSONResponse)
async def get_container(exchange_id: int, is_cms: bool) -> list[dict] | str:
    try:
        statement = select(container).where(and_(container.c.exchange_pk == exchange_id,
                                                 container.c.is_cms == is_cms))
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for res in result:
            d = {}
            for key, value in zip(Container.__annotations__, res):
                d[key] = value
            response.append(d)
        return response

    except Exception as e:
        return Exceptions().get_exception(e)


@router.post('/option/post', response_class=JSONResponse)
async def post_option(request: Options) -> JSONResponse:
    try:
        statement = insert(option).values(request.model_dump())
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        if request.is_investor:
            # run leader container
            if not await get_container(request.leader_pk, request.is_investor):
                run_cms_container(request.leader_pk, 'leader')
            # run investor container
            run_cms_container(request.investor_pk, 'investor')
        else:
            # run leader container
            if not await get_container(request.leader_pk, request.is_investor):
                run_signal_container(request.leader_pk, 'leader')
            # run investor container
            run_signal_container(request.investor_pk, 'investor')
        return JSONResponse(content={'option': 'posted'})
    except Exception as e:
        engine.connect().close()
        return Exceptions().post_exception(e)


@router.get('/option/get/{leader_id}/', response_class=JSONResponse)
async def get_option(leader_id: int) -> list[dict] | str:
    try:
        statement = select(option).where(option.c.leader_pk == leader_id)
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
        statement = select(option)
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
        statement = insert(position_history).values(request.model_dump())
        with engine.connect() as conn:
            conn.execute(statement)
            conn.commit()
        return "Posted"
    except Exception as e:
        engine.connect().close()
        return Exceptions().post_exception(e)


@router.get('/leader-id-by-investor/get/{investor_id}/', response_class=JSONResponse)
async def get_leader_id_by_investor_id(investor_id: int) -> list | str:
    try:
        statement = select(option.c.leader_pk).where(option.c.investor_pk == investor_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for value in result:
            response.append(int(value[0]))
        return response
    except Exception as e:
        return Exceptions().get_exception(e)


@router.get('/leader-id-by-exchange/get/{exchange_id}/', response_class=JSONResponse)
async def get_leader_id_by_exchange_id(exchange_id: int) -> list | str:
    try:
        statement = select(option.c.leader_pk).where(option.c.exchange_pk == exchange_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for value in result:
            response.append(int(value[0]))
        return response
    except Exception as e:
        return Exceptions().get_exception(e)


@router.get('/investor-id-by-leader/get/{leader_id}/', response_class=JSONResponse)
async def get_investor_id_by_leader_id(leader_id: int) -> list | str:
    try:
        statement = select(option.c.investor_pk).where(option.c.leader_pk == leader_id)
        with engine.connect() as conn:
            result = conn.execute(statement).fetchall()
            conn.commit()
        response = []
        for value in result:
            response.append(int(value[0]))
        return response
    except Exception as e:
        return Exceptions().get_exception(e)
