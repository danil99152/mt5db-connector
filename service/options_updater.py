import asyncio
import json

import requests
from sqlalchemy import update, insert, select

from service.configs import Options
from service.models import atimex_options, engine, account, investor, leader
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

    async def update_options(self):
        investor_pk = 1
        result = self.get_options(investor_pk)

        while True:
            options = {}
            try:
                options = json.loads(requests.get(settings.host).text)[0]

                for key in options:
                    if options[key] in {"Да", "Переоткрывать", "Корректировать объем"}:
                        options[key] = True
                    elif options[key] in {"Нет", "Не переоткрывать", "Не корректировать"}:
                        options[key] = False

                options['investor_pk'] = investor_pk
            except Exception as e:
                print(e)

            options['investment'] = options['investment_one_size']

            values = Options(**options).dict()

            leader_data = {
                "account_pk": 1,
                "login": options['leader_login'],
                "password": options['leader_password'],
                "server": options['leader_server'],
                "balance": 10000,
                "equity": 10000,
            }
            investor1_data = {
                "account_pk": 2,
                "login": options['investor_one_login'],
                "password": options['investor_one_password'],
                "server": options['investor_one_server'],
                "balance": options['investment_one_size'],
                "equity": 10000,
            }
            investor2_data = {
                "account_pk": 3,
                "login": options['investor_two_login'],
                "password": options['investor_two_password'],
                "server": options['investor_two_server'],
                "balance": options['investment_two_size'],
                "equity": 10000,
            }
            if options:
                if not result:
                    try:
                        insert_options = insert(atimex_options).values(values)
                        insert_leader_account = insert(account).values(leader_data)
                        insert_leader = insert(leader).values({
                            'leader_pk': 1,
                            'account_pk': 1,
                        })
                        insert_investor1_account = insert(account).values(investor1_data)
                        insert_investor1 = insert(investor).values({
                            'investor_pk': 1,
                            'leader_pk': 1,
                            'account_pk': 2,
                        })
                        insert_investor2_account = insert(account).values(investor2_data)
                        insert_investor2 = insert(investor).values({
                            'investor_pk': 2,
                            'leader_pk': 1,
                            'account_pk': 3,
                        })
                        with engine.connect() as conn:
                            conn.execute(insert_leader_account)
                            conn.commit()
                        with engine.connect() as conn:
                            conn.execute(insert_leader)
                            conn.commit()
                        with engine.connect() as conn:
                            conn.execute(insert_investor1_account)
                            conn.commit()
                        with engine.connect() as conn:
                            conn.execute(insert_investor1)
                            conn.commit()
                        with engine.connect() as conn:
                            conn.execute(insert_investor2_account)
                            conn.commit()
                        with engine.connect() as conn:
                            conn.execute(insert_investor2)
                            conn.commit()
                        with engine.connect() as conn:
                            conn.execute(insert_options)
                            conn.commit()
                        result = self.get_options(investor_pk)
                    except Exception as e:
                        print(f"Wasn't inserted because {e}")
                elif result and list(result[0]) != list(values.values()):
                    try:
                        update_options = update(atimex_options).where(atimex_options.c.investor_pk == investor_pk
                                                                      ).values(values)
                        update_leader = update(account).where(account.c.account_pk == leader_data['account_pk']
                                                              ).values(leader_data)
                        update_investor1 = update(account).where(account.c.account_pk == investor1_data['account_pk']
                                                                 ).values(investor1_data)
                        update_investor2 = update(account).where(account.c.account_pk == investor2_data['account_pk']
                                                                 ).values(investor2_data)
                        with engine.connect() as conn:
                            conn.execute(update_leader)
                            conn.commit()
                        with engine.connect() as conn:
                            conn.execute(update_investor1)
                            conn.commit()
                        with engine.connect() as conn:
                            conn.execute(update_investor2)
                            conn.commit()
                        with engine.connect() as conn:
                            conn.execute(update_options)
                            conn.commit()
                        result = self.get_options(investor_pk)
                    except Exception as e:
                        print(f"Wasn't patched because {e}")

            await asyncio.sleep(1)


async def callback():
    await OptionsUpdater().update_options()


def between_callback():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(callback())
    loop.close()
