import asyncio
import json
import os

import requests
from sqlalchemy import update, insert, select

from service.configs import Account
from service.models import atimex_options, engine, account, investor, leader, container
from settings import settings


class OptionsUpdater:
    __slots__ = []

    @staticmethod
    def get_options(investor_pk):
        statement = select(atimex_options).where(atimex_options.c.investor_pk == investor_pk)
        try:
            with engine.connect() as conn:
                result = conn.execute(statement).fetchall()
                conn.commit()
                return result
        except Exception as e:
            print(f"Wasn't get options from db because {e}")
            return []

    @staticmethod
    def get_account_by_investor_pk(investor_pk):
        account_pk = select(investor.c.account_pk).where(investor.c.investor_pk == investor_pk)
        statement = select(account).where(account.c.account_pk == account_pk)
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
    def get_account_by_leader_pk(leader_pk):
        account_pk = select(leader.c.account_pk).where(leader.c.leader_pk == leader_pk)
        statement = select(account).where(account.c.account_pk == account_pk)
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
    def get_investor(investor_pk):
        statement = select(investor).where(investor.c.investor_pk == investor_pk)
        try:
            with engine.connect() as conn:
                result = conn.execute(statement).fetchall()
                conn.commit()
                return result
        except Exception as e:
            print(f"Wasn't get investor from db because {e}")
            return []


    @staticmethod
    def get_leader(leader_pk):
        statement = select(leader).where(leader.c.leader_pk == leader_pk)
        try:
            with engine.connect() as conn:
                result = conn.execute(statement).fetchall()
                conn.commit()
                return result
        except Exception as e:
            print(f"Wasn't get leader from db because {e}")
            return []

    @staticmethod
    def remake_options(options):
        for i, option in enumerate(options):
            for key in option:
                if options[i][key] in {"Да", "Переоткрывать", "Корректировать объем"}:
                    options[i][key] = True
                elif options[i][key] in {"Нет", "Не переоткрывать", "Не корректировать"}:
                    options[i][key] = False
        return options

    @staticmethod
    def get_investor_from_api(id):
        return json.loads(requests.get(f'http://127.0.0.1:8000/api/investor/get/{id}').text)

    async def update_options(self):
        while True:
            try:
                options = json.loads(requests.get(settings.host).text)
                investors = json.loads(requests.get(settings.host_investor).text)
                leaders = json.loads(requests.get(settings.host_leader).text)
                history = json.loads(requests.get(settings.host_history).text)

                investor_exchanges = json.loads(requests.get(settings.host_exchanges).text)
                investor_exchanges = list(filter(lambda d: d['exchange'] == 'mt5'
                                                           and d['type_account'] == 'investor', investor_exchanges))
                leader_exchanges = json.loads(requests.get(settings.host_exchanges).text)
                leader_exchanges = list(filter(lambda d: d['exchange'] == 'mt5'
                                                           and d['type_account'] == 'leader', leader_exchanges))

                if leader_exchanges:
                    for lead in leader_exchanges:
                        id = lead.get("leader_id")
                        account_id = lead.get('account_exch').get('id')
                        leader_result = self.get_leader(id)
                        account_result = self.get_account_by_leader_pk(id)
                        investment_size = sum([d.get('investment') for d in history if d['user_id'] > id])
                        lead = {k: v or 0 for (k, v) in lead.items()}
                        leader_data = {
                            "account_pk": account_id,
                            "login": lead.get('api_key'),
                            "password": lead.get('api_secret'),
                            "server": lead.get('server'),
                            "balance": lead.get('balance'),
                            "equity": lead.get('equity'),
                            "investment_size": investment_size,
                            "currency": str(lead['account_exch'].get('currency')),
                            "access_dcs": True,
                        }
                        leader_values = Account(**leader_data).dict()
                        if not leader_result:
                            insert_leader_account = insert(account).values(leader_values)
                            insert_leader = insert(leader).values({
                                'leader_pk': id,
                                'account_pk': account_id,
                            })
                            with engine.connect() as conn:
                                conn.execute(insert_leader_account)
                                conn.commit()
                            with engine.connect() as conn:
                                conn.execute(insert_leader)
                                conn.commit()

                            os.system(f"docker run -e ACCOUNT_ID={account_id} "
                                      f"--name mt_leader{account_id} "
                                      f"205b28d28c91f81522f6f4335ae77aaac20c58645ad8be3d1a4e4f63380ed3b1")
                            os.system(f"docker exec -it mt_leader{account_id} start_leader.sh")
                            os.system(f"docker exec -it mt_leader{account_id} chmod +x /start_leader.sh")

                            container_data = {
                                "account_pk": account_id,
                                "name": f"mt_leader{account_id}",
                            }
                            insert_investor_container = insert(container).values(container_data)
                            with engine.connect() as conn:
                                conn.execute(insert_investor_container)
                                conn.commit()

                        elif list(account_result) != list(leader_values.values()):
                            update_leader = update(account).where(account.c.account_pk == id).values(leader_values)
                            with engine.connect() as conn:
                                conn.execute(update_leader)
                                conn.commit()

                    if investors:
                        for invest in investor_exchanges:
                            id = invest.get('id')
                            account_id = invest.get('account_exch').get('id')
                            investor_result = self.get_investor(id)
                            account_result = self.get_account_by_investor_pk(id)
                            investment_size = sum([d.get('investment') for d in history if d['user_id'] > id])
                            invest = {k: v or 0 for (k, v) in invest.items()}
                            investor_data = {
                                "account_pk": account_id,
                                "login": invest.get('api_key'),
                                "password": invest.get('api_secret'),
                                "server": invest.get('server'),
                                "balance": invest.get('balance'),
                                "equity": invest.get('equity'),
                                "investment_size": investment_size,
                                "currency": str(invest['account_exch'].get('currency')),
                                "access_dcs": True,
                            }
                            investor_values = Account(**investor_data).dict()
                            investor_strategies = self.get_investor_from_api(account_id).get('strategies_investor')
                            if not investor_result:
                                insert_investor_account = insert(account).values(investor_values)
                                insert_investor = insert(investor).values({
                                    'investor_pk': id,
                                    # 'leader_pk': invest.get('leader_account'),
                                    'account_pk': account_id,
                                })
                                with engine.connect() as conn:
                                    conn.execute(insert_investor_account)
                                    conn.commit()
                                with engine.connect() as conn:
                                    conn.execute(insert_investor)
                                    conn.commit()

                                os.system(f"docker run -e ACCOUNT_ID={account_id} "
                                          f"--name mt_investor{account_id} "
                                          f"205b28d28c91f81522f6f4335ae77aaac20c58645ad8be3d1a4e4f63380ed3b1")
                                os.system(f"docker exec -it mt_investor{account_id} start_investor.sh")
                                os.system(f"docker exec -it mt_investor{account_id} chmod +x /start_investor.sh")

                                container_data = {
                                    "account_pk": account_id,
                                    "name": f"mt_investor{account_id}",
                                }
                                insert_investor_container = insert(container).values(container_data)
                                with engine.connect() as conn:
                                    conn.execute(insert_investor_container)
                                    conn.commit()

                            elif list(account_result) != list(investor_values.values()):
                                update_investor = update(account).where(account.c.account_pk == id).values(investor_values)
                                with engine.connect() as conn:
                                    conn.execute(update_investor)
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
