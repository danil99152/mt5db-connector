import asyncio
import json

import requests
from sqlalchemy import update, insert, select

from service.configs import Options, Account
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

    @staticmethod
    def get_accounts(investor_pk):
        account_pk = select(investor.c.account_pk).where(investor.c.investor_pk == investor_pk)
        statement = select(account).where(account.c.account_pk == account_pk)
        try:
            with engine.connect() as conn:
                result = conn.execute(statement).fetchall()
                conn.commit()
                return result
        except Exception as e:
            print(f"Wasn't get options from db because {e}")
            return []

    @staticmethod
    def get_investors(investor_pk):
        statement = select(investor).where(atimex_options.c.investor_pk == investor_pk)
        try:
            with engine.connect() as conn:
                result = conn.execute(statement).fetchall()
                conn.commit()
                return result
        except Exception as e:
            print(f"Wasn't get options from db because {e}")
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

    async def update_options(self):
        while True:
            try:
                options = json.loads(requests.get(settings.host).text)
                investors = json.loads(requests.get(settings.host_investor).text)
                history = json.loads(requests.get(settings.host_history).text)

                options = self.remake_options(options)

                for invest in investors:
                    id = invest.get('investor_id')
                    result = self.get_options(id)
                    investor_result = self.get_investors(id)
                    account_result = self.get_accounts(id)
                    investment_size = 0
                    for hist in history:
                        if hist['user_id'] == id:
                            investment_size += hist['investment']
                    if investors:
                        investor_values = Account(**invest).dict()
                        investor_data = {
                            "account_pk": invest.get('id'),
                            "login": invest.get('investor_name'),
                            "password": invest.get('?'),
                            "server": invest.get('?'),
                            "balance": invest.get('investment'),
                            "equity": invest.get('equity'),
                            "investment_size": investment_size,
                        }
                        if not investor_result:
                            insert_investor_account = insert(account).values(investor_data)
                            insert_investor = insert(investor).values({
                                'investor_pk': invest.get('investor_account'),
                                'leader_pk': invest.get('leader_account'),
                                'account_pk': invest.get('id'),
                            })
                            with engine.connect() as conn:
                                conn.execute(insert_investor_account)
                                conn.commit()
                            with engine.connect() as conn:
                                conn.execute(insert_investor)
                                conn.commit()

                        elif account_result and list(account_result) != list(investor_values.values()):
                            update_investor = update(account).where(account.c.account_pk == investor_data['account_pk']
                                                                    ).values(investor_data)
                            with engine.connect() as conn:
                                conn.execute(update_investor)
                                conn.commit()

                    for option in options:
                        option['investment'] = option['investment_one_size']
                        values = Options(**options).dict()
                        leader_data = {
                            "account_pk": 1,
                            "login": options['leader_login'],
                            "password": options['leader_password'],
                            "server": options['leader_server'],
                            "balance": 10000,
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
                                    with engine.connect() as conn:
                                        conn.execute(insert_leader_account)
                                        conn.commit()
                                    with engine.connect() as conn:
                                        conn.execute(insert_leader)
                                        conn.commit()
                                    with engine.connect() as conn:
                                        conn.execute(insert_options)
                                        conn.commit()
                                    result = self.get_options(id)
                                except Exception as e:
                                    print(f"Wasn't inserted because {e}")
                            elif result and list(result[0]) != list(values.values()):
                                try:
                                    update_options = update(atimex_options).where(atimex_options.c.investor_pk == id
                                                                                  ).values(values)
                                    update_leader = update(account).where(account.c.account_pk == leader_data['account_pk']
                                                                          ).values(leader_data)
                                    with engine.connect() as conn:
                                        conn.execute(update_leader)
                                        conn.commit()
                                    with engine.connect() as conn:
                                        conn.execute(update_options)
                                        conn.commit()
                                    result = self.get_options(id)
                                except Exception as e:
                                    print(f"Wasn't patched because {e}")
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
