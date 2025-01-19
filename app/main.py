from fastapi import FastAPI
from lifespan import lifespan
from routers import events, hexgrid, player


def create_app():
    app = FastAPI(lifespan=lifespan)
    app.include_router(hexgrid.router)
    app.include_router(player.router)
    app.include_router(events.router)
    return app


app = create_app()
