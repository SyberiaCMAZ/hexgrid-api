from abstract.events import event_factory
from fastapi import APIRouter, Request
from pydantic import BaseModel, Field

router = APIRouter(
    prefix="/events",
    tags=["events"],
)


class CreateEventRequest(BaseModel):
    name: str
    amount: int | None = Field(default=None)
    q: int
    r: int
    s: int


@router.post("/create")
async def create_event(request: Request, body: CreateEventRequest):
    hex_grid = request.state.hex_grid

    event = event_factory(body.name, body.amount)

    cell = hex_grid.get_cell(body.q, body.r, body.s)
    cell.add_event(event)

    return {"message": "Event created"}
