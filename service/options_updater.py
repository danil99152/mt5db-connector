import asyncio
import json

import requests
from pydantic import BaseModel
from sqlalchemy import update, insert, select

from service.configs import Options
from service.models import atimex_options, engine
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
                        result = self.get_options(investor_pk)
                    except Exception as e:
                        print(f"Wasn't inserted because {e}")
                elif result and list(result[0]) != list(values.values()):
                    try:
                        statement = update(atimex_options).where(atimex_options.c.investor_pk == investor_pk).values(
                            values)
                        with engine.connect() as conn:
                            conn.execute(statement)
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
