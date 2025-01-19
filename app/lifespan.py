from contextlib import asynccontextmanager

from abstract.hexgrid import HexGrid, generate_map
from fastapi import FastAPI


@asynccontextmanager
async def lifespan(app: FastAPI):
    game_map = generate_map()
    hex_grid = HexGrid.from_json(game_map)
    yield {"hex_grid": hex_grid}

    # TODO: Quick fix
    hex_grid._cells.clear()
