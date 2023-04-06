import logging
import logging
import threading

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import services_router
from service.models import leader, investor, position, atimex_options, engine, account, container
from service.options_updater import between_callback
from settings import settings

logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s', encoding='utf-8', level=logging.DEBUG)

app = FastAPI(docs_url='/api/', redoc_url=None, title=settings.APP_TITLE, version=settings.APP_VERSION,
              swagger_ui_oauth2_redirect_url='/api/oauth2-redirect/')

origins = ['*']

app.add_middleware(middleware_class=CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'],
                   )

app.include_router(router=services_router)

if __name__ == '__main__':
    account.create(engine, checkfirst=True)
    leader.create(engine, checkfirst=True)
    investor.create(engine, checkfirst=True)
    container.create(engine, checkfirst=True)
    position.create(engine, checkfirst=True)
    atimex_options.create(engine, checkfirst=True)
    # TODO sqlalchemy.exc.TimeoutError: QueuePool limit of size 5 overflow 10 reached, connection timed out, timeout 30.00
    threading.Thread(target=between_callback).start()
    uvicorn.run(app=app, app_dir=settings.APP_PATH, host=settings.APP_HOST, port=settings.APP_PORT)