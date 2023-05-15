import asyncio
import json

import requests
from sqlalchemy import update, insert, select

from service.configs import Account
from service.models import atimex_options, engine, account, investor
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
                result = conn.execute(statement).fetchall()[0]
                conn.commit()
                response = []
                for value in result:
                    response.append(value)
                return response
        except Exception as e:
            print(f"Wasn't get options from db because {e}")
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

    @staticmethod
    def get_exchanges_user(id):
        return json.loads(requests.get(f'https://my.atimex.io:8000/api/exchanges/user?users_connect__id={id}&exchange').text)

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



                for invest in investors:
                    if investors:
                        investor_exchanges = self.get_exchanges_user(invest.get('investor_id'))
                        for exchange in investor_exchanges:
                            id = exchange.get('id')
                            investor_result = self.get_investor(id)
                            account_result = self.get_accounts(id)
                            investment_size = 0
                            for hist in history:
                                if hist['user_id'] == id:
                                    investment_size += hist['investment']
                            exchange = {k: v or 0 for (k, v) in exchange.items()}
                            investor_data = {
                                "account_pk": exchange.get('account_exch').get('account'),
                                "login": exchange.get('api_key'),
                                "password": exchange.get('api_secret'),
                                "server": exchange.get('server'),
                                "balance": exchange.get('balance'),
                                "equity": exchange.get('equity'),
                                "investment_size": investment_size,
                                "currency": str(exchange['account_exch'].get('currency')),
                                "access_dcs": True,
                            }
                            investor_values = Account(**investor_data).dict()
                            if not investor_result:
                                insert_investor_account = insert(account).values(investor_values)
                                insert_investor = insert(investor).values({
                                    'investor_pk': id,
                                    'leader_pk': invest.get('leader_account'),
                                    'account_pk': exchange.get('account_exch').get('account'),
                                })
                                with engine.connect() as conn:
                                    conn.execute(insert_investor_account)
                                    conn.commit()
                                with engine.connect() as conn:
                                    conn.execute(insert_investor)
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
