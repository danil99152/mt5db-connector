import asyncio
import json

import requests
from pydantic import BaseModel
from sqlalchemy import update, insert, select

from service.models import atimex_options, engine
from settings import settings


class Options(BaseModel):
    id: int
    investor_pk: int
    leader_login: str
    leader_password: str
    leader_server: str
    investor_one_login: str
    investor_one_password: str
    investor_one_server: str
    investment_one_size: str
    investor_two_login: str
    investor_two_password: str
    investor_two_server: str
    investment_two_size: str
    deal_in_plus: float
    deal_in_minus: float
    waiting_time: float
    ask_an_investor: str
    price_refund: bool
    multiplier: str
    multiplier_value: float
    changing_multiplier: bool
    stop_loss: str
    stop_value: float
    open_trades: str
    shutdown_initiator: str
    disconnect: bool
    open_trades_disconnect: str
    notification: bool
    blacklist: bool
    accompany_transactions: bool
    no_exchange_connection: bool
    api_key_expired: bool
    closed_deals_myself: bool
    reconnected: bool
    recovery_model: bool
    buy_hold_model: bool
    not_enough_margin: str
    accounts_in_diff_curr: str
    synchronize_deals: bool
    deals_not_opened: bool
    closed_deal_investor: bool


class OptionsUpdater:
    __slots__ = []

    @staticmethod
    async def update_options():
        investor_pk = 1
        statement = select(atimex_options).where(atimex_options.c.investor_pk == investor_pk)
        try:
            with engine.connect() as conn:
                result = conn.execute(statement).fetchall()
                conn.commit()
        except Exception as e:
            print(f"Wasn't get options from db because {e}")

        while True:
            options = {}
            try:
                options = json.loads(requests.get(settings.host).text)[0]
                to_delete = ['opening_deal', 'closing_deal', 'target_and_stop',
                             'signal_relevance', 'profitability', 'risk',
                             'profit', 'comment', 'relevance', 'access',
                             'access_1', 'access_2', 'update_at', 'created_at']
                for key in to_delete:
                    options.pop(key, None)

                for key in options:
                    if options[key] in {"Да", "Переоткрывать", "Корректировать объем"}:
                        options[key] = True
                    elif options[key] in {"Нет", "Не переоткрывать", "Не корректировать"}:
                        options[key] = False

                options['investor_pk'] = investor_pk
            except Exception as e:
                print(e)

            values = Options(**options).dict()
            values['investor_pk'] = investor_pk
            if options:
                if not result:
                    try:
                        statement = insert(atimex_options).values(values)
                        with engine.connect() as conn:
                            conn.execute(statement)
                            conn.commit()
                    except Exception as e:
                        print(f"Wasn't inserted because {e}")
                elif result and list(result[0]) != list(values.values()):
                    try:
                        statement = update(atimex_options).where(atimex_options.c.investor_pk == investor_pk).values(
                            values)
                        with engine.connect() as conn:
                            conn.execute(statement)
                            conn.commit()
                    except Exception as e:
                        print(f"Wasn't patched because {e}")

            await asyncio.sleep(5)


async def callback():
    await OptionsUpdater.update_options()


def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(callback())
    loop.close()
