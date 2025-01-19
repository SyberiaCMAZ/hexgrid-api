import abc
import random
import typing
from typing import Optional

if typing.TYPE_CHECKING:
    from .player import Player


class Event(abc.ABC):
    name: str

    def __init__(self, creator: Optional["Player"] = None):
        self.creator = creator

    @abc.abstractmethod
    def apply_event(self, player: "Player") -> dict:
        # This method should return a message
        pass


class HealthEvent(Event):
    name = "HealthEvent"

    def __init__(self, amount: int, creator: Optional["Player"] = None):
        super().__init__(creator)
        self.amount = amount

    def apply_event(self, player) -> dict:
        player.health += self.amount
        message = {
            "type": "HealthEvent",
            "amount": self.amount,
            "player": player.name,
            "set_by": self.creator.name if self.creator else "System",
        }
        return message


class InventoryEvent(Event):
    name = "InventoryEvent"

    def __init__(self, granted_event: Event, creator: Optional["Player"] = None):
        super().__init__(creator)
        self.granted_event = granted_event

    def apply_event(self, player: "Player") -> dict:
        player.inventory.append(self.granted_event)
        return {
            "type": self.name,
            "item": self.granted_event.name,
            "player": player.name,
            "set_by": self.creator.name if self.creator else "System",
        }


def event_factory(name: str, amount: int | None = None) -> Event:
    amount = amount if amount else random.randint(-8, 8)
    if name == "HealthEvent":
        return HealthEvent(amount=amount)
    elif name == "ItemEvent":
        item = HealthEvent(amount=amount)
        return InventoryEvent(granted_event=item)
    else:
        raise ValueError("Unknown event")
