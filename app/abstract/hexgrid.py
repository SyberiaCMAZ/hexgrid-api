import random
import typing

if typing.TYPE_CHECKING:
    from .events import Event
    from .player import Player


class Cell:
    cost_table = {"mountains": 4, "desert": 3, "forest": 2, "plains": 1}

    def __init__(self, q: int, r: int, s: int, cell_type: str):
        self.q = q
        self.r = r
        self.s = s
        assert q + r + s == 0, "Invalid coordinates"

        self.cell_type = cell_type
        self.energy_cost = self.cost_table[cell_type]
        self._players: dict[str, "Player"] = {}
        self.events: list["Event"] = []

    def __repr__(self):
        players_names = [player.name for player in self.get_players()]
        return f"<Cell (type={self.cell_type}, pos=({self.q}, {self.r}, {self.s}), players={players_names})>"

    def is_in_range(self, other_cell, n) -> bool:
        # https://www.redblobgames.com/grids/hexagons/#distances
        return (
            max(
                abs(self.q - other_cell.q),
                abs(self.r - other_cell.r),
                abs(self.s - other_cell.s),
            )
            == n
        )

    def get_players(self) -> list["Player"]:
        return list(self._players.values())

    def add_player(self, player: "Player") -> None:
        self._players[player.player_id] = player

    def remove_player(self, player: "Player") -> None:
        del self._players[player.player_id]

    def add_event(self, event: "Event") -> None:
        self.events.append(event)

    def get_events(self) -> list["Event"]:
        # Get all events and clear the list
        if not self.events:
            return self.events
        events = self.events.copy()
        self.events.clear()
        return events


class HexGrid:
    _cells: dict[tuple[int, int, int], Cell] = {}
    players: dict[str, "Player"] = {}

    def __repr__(self) -> str:
        return f"<HexGrid: {self._cells}>"

    @classmethod
    def from_json(cls, data: dict):
        obj = cls()
        for cell in data["cells"]:
            q = cell["q"]
            r = cell["r"]
            s = cell["s"]
            cell_type = cell["type"]
            cell = Cell(q, r, s, cell_type)
            obj._cells[(q, r, s)] = cell

        return obj

    def get_cell(self, q: int, r: int, s: int) -> Cell:
        return self._cells[(q, r, s)]

    def add_player(self, player: "Player", q: int, r: int, s: int) -> None:
        self.players[player.player_id] = player
        cell = self._cells[(q, r, s)]
        player.cell = cell
        cell.add_player(player)


# Helper
def generate_map(range_value=10):
    cells = []
    types = ["forest", "plains", "desert", "mountains"]
    for q in range(-range_value, range_value + 1):
        for r in range(-range_value, range_value + 1):
            s = -(q + r)
            if abs(s) <= range_value:
                cell_data = {
                    "type": random.choice(types),
                    "q": q,
                    "r": r,
                    "s": s,
                }
                cells.append(cell_data)
    map_data = {"cells": cells}
    return map_data
