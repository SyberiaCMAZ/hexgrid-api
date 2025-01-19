import typing
import uuid

if typing.TYPE_CHECKING:
    from .events import Event
    from .hexgrid import Cell


class Player:

    def __init__(self, name: str):
        self.name = name
        self.player_id = str(uuid.uuid4())

        self.energy = 40
        self.health = 10

        # For now, we will not implement inventory
        self.inventory: list["Event"] = []

        self.cell: Cell = Cell(0, 0, 0, "plains")

    def __repr__(self):
        return f"<Player(name={self.name}, health={self.health}, energy={self.energy})>"

    def move_one(self, cell) -> list[dict] | None:
        assert self.energy >= cell.energy_cost, "Player energy too low"
        assert self.cell != cell, "Player already in this cell"
        assert self.cell.is_in_range(cell, 1), "Range greater than one"

        self.energy -= cell.energy_cost
        self._teleport(cell)
        results = [
            {
                "type": "PlayerMove",
                "player": self.name,
                "position": [cell.q, cell.r, cell.s],
            }
        ]
        events = self.cell.get_events()
        for event in events:
            results.append(event.apply_event(self))
        return results

    def use_item(self, inventory_slot: int) -> None:
        try:
            event = self.inventory.pop(inventory_slot)
        except IndexError:
            return
        self.cell.add_event(event)

    def _teleport(self, cell: "Cell") -> None:
        self.cell.remove_player(self)
        cell.add_player(self)
        self.cell = cell
