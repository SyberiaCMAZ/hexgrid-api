import unittest

from abstract.events import HealthEvent, InventoryEvent
from abstract.player import Player


class EventTestCase(unittest.TestCase):

    def setUp(self):
        self.player = Player("Szefito")

    def test_trap_event(self):
        # Arrange
        bandit = Player("Bandit")
        trap_event = HealthEvent(amount=10, creator=bandit)
        expected_result = {
            "type": "HealthEvent",
            "amount": 10,
            "player": "Szefito",
            "set_by": "Bandit",
        }

        # Act
        result = trap_event.apply_event(self.player)

        # Assert
        self.assertEqual(self.player.health, 20)
        self.assertEqual(result, expected_result)

    def test_inventory_event(self):
        # Arrange
        # For prototype purposes, we will use HealthEvent as a granted item
        item = HealthEvent(amount=10)
        inventory_event = InventoryEvent(item)
        expected_result = {
            "type": "InventoryEvent",
            "item": "HealthEvent",
            "player": "Szefito",
            "set_by": "System",
        }

        # Act
        result = inventory_event.apply_event(self.player)

        # Assert
        self.assertEqual(result, expected_result)
