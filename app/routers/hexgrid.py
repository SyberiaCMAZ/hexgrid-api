from fastapi import APIRouter, Request

router = APIRouter(
    prefix="/hexgrid",
    tags=["hexgrid"],
)


@router.get("/map")
async def get_map(request: Request):
    hex_grid = request.state.hex_grid
    hello = str(hex_grid)
    return {"message": hello}
