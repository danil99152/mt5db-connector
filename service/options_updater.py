import asyncio
import json
import os

import requests
from sqlalchemy import update, insert, select, and_

from service.configs import Exchange
from service.models import atimex_options, engine, exchange, container, investor_leader
from settings import settings


class OptionsUpdater:
    __slots__ = []

    @staticmethod
    def get_exchange(exchange_pk):
        statement = select(exchange).where(exchange.c.exchange_pk == exchange_pk)
        try:
            with engine.connect() as conn:
                result = conn.execute(statement).fetchall()[0]
                conn.commit()
                response = []
                for value in result:
                    response.append(value)
                return response
        except Exception as e:
            print(f"Wasn't get accounts from db because {e}")
            return []

    @staticmethod
    def get_relates(invest_id, leader_id):
        statement = select(investor_leader).where(and_(investor_leader.c.investor_id == invest_id,
                                                       investor_leader.c.leader_id == leader_id))
        try:
            with engine.connect() as conn:
                result = conn.execute(statement).fetchall()[0]
                conn.commit()
                response = []
                for value in result:
                    response.append(value)
                return response
        except Exception as e:
            print(f"Wasn't get accounts from db because {e}")
            return []

    @staticmethod
    def get_investor_from_api(id):
        return json.loads(requests.get(f'http://127.0.0.1:8000/api/investor/get/{id}').text)

    @staticmethod
    def get_strategy_from_api(id):
        return json.loads(requests.get(f'http://127.0.0.1:8000/api/strategy-detail/{id}').text)

    async def update_options(self):
        while True:
            try:
                history = json.loads(requests.get(settings.host_history).text)
                exchanges = json.loads(requests.get(settings.host_exchanges).text)

                if exchanges:
                    for exch in exchanges:
                        id = exch.get("id")
                        account_id = exch.get('users_connect').get('id')
                        type = exch.get('type_account')
                        exchange_result = self.get_exchange(id)
                        investment_size = sum([d.get('investment') for d in history if d['user_id'] == account_id])
                        exch = {k: v or 0 for (k, v) in exch.items()}
                        exchanges_data = {
                            "exchange_pk": id,
                            "login": exch.get('api_key'),
                            "password": exch.get('api_secret'),
                            "server": exch.get('server'),
                            "balance": exch.get('balance'),
                            "equity": exch.get('equity'),
                            "investment_size": investment_size,
                            "currency": str(exch['account_exch'].get('currency')),
                            "access_dcs": True,
                            "type": type
                        }
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

                    investor_exchanges = list(filter(lambda d: d['exchange'] == 'mt5'
                                                               and d['type_account'] == 'investor',
                                                     exchanges))
                    for invest in investor_exchanges:
                        invest_id = invest.get('id')
                        account_id = invest.get('users_connect').get('id')
                        investor_strategies = self.get_investor_from_api(account_id).get('strategies_investor')
                        leader_ids = [self.get_strategy_from_api(i).get('user_leader').get('id')
                                      for i in investor_strategies]
                        for lead_id in leader_ids:
                            leader_exchange = list(filter(lambda d: d['exchange'] == 'mt5'
                                                                     and d['type_account'] == 'leader'
                                                                     and d['users_connect']['id'] == lead_id,
                                                           exchanges))
                            for leader in leader_exchange:
                                leader_id = leader.get('id')
                                relate_result = self.get_relates(invest_id, leader_id)
                                if not relate_result:
                                    data = {
                                        "investor_id": invest_id,
                                        "leader_id": leader_id,
                                    }
                                    insert_relate = insert(investor_leader).values(data)
                                    with engine.connect() as conn:
                                        conn.execute(insert_relate)
                                        conn.commit()

            except Exception as e:
                print(e)

            await asyncio.sleep(1)


async def callback():
    await OptionsUpdater().update_options()


def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(callback())
    loop.close()
