from abstract.player import Player
from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel

router = APIRouter(
    prefix="/player",
    tags=["player"],
)


class CreatePlayerRequest(BaseModel):
    name: str


@router.post("/create")
async def create_player(request: Request, body: CreatePlayerRequest):
    player = Player(body.name)
    hex_grid = request.state.hex_grid
    hex_grid.add_player(player, 0, 0, 0)
    return {"player_id": player.player_id}


class MovePlayerRequest(BaseModel):
    player_id: str
    q: int
    r: int
    s: int


@router.post("/move")
async def move_player(request: Request, body: MovePlayerRequest):
    hex_grid = request.state.hex_grid
    player = hex_grid.players[body.player_id]

    try:
        cell = hex_grid.get_cell(body.q, body.r, body.s)
        results = player.move_one(cell)
    except (AssertionError, KeyError) as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"results": results}


class UseItemRequest(BaseModel):
    player_id: str
    inventory_slot: int


@router.post("/use_item")
async def use_item(request: Request, body: UseItemRequest):
    hex_grid = request.state.hex_grid
    player = hex_grid.players[body.player_id]
    player.use_item(body.inventory_slot)
    return {"message": "Item used"}


@router.get("/get/{player_id}")
async def get_player(request: Request, player_id):
    hex_grid = request.state.hex_grid
    player = hex_grid.players[player_id]
    return {
        "player": player.name,
        "health": player.health,
        "energy": player.energy,
        "inventory": player.inventory,
        "position": [player.cell.q, player.cell.r, player.cell.s],
    }
