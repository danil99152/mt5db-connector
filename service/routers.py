from fastapi import APIRouter
from starlette.responses import JSONResponse

router = APIRouter(prefix='/investor')


# for investors
@router.get('/get-positions/', response_class=JSONResponse)
async def get_positions():
    pass


# for investors
@router.get('/get-position/', response_class=JSONResponse)
async def get_position(ticket: int):
    pass


# for leader
@router.post('/post-position/', response_class=JSONResponse)
async def post_position(request: dict):
    pass


# for leader
@router.patch('/patch-position/', response_class=JSONResponse)
async def patch_position(ticket: int, request: dict):
    pass


# for investors
@router.get('/get-option/', response_class=JSONResponse)
async def get_option(option_id: int):
    pass


# for investors
@router.get('/get-options/', response_class=JSONResponse)
async def get_options():
    pass

