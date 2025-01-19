import unittest

from abstract.events import HealthEvent
from abstract.hexgrid import HexGrid
from abstract.player import Player

from .map_json import json_data


class PlayerTestCase(unittest.TestCase):

    def setUp(self):
        self.hexgrid = HexGrid.from_json(json_data)
        self.player = Player("Szefito")
        self.hexgrid.add_player(self.player, 0, 0, 0)

    def test_player_teleport(self):
        # Arrange
        start_cell = self.hexgrid.get_cell(0, 0, 0)
        cell = self.hexgrid.get_cell(-1, 0, 1)

        # Act
        self.player._teleport(cell)

        # Assert
        self.assertTrue(self.player in cell.get_players())
        self.assertTrue(self.player not in start_cell.get_players())

    def test_player_move_one(self):
        # Arrange
        start_cell = self.hexgrid.get_cell(0, 0, 0)
        cell = self.hexgrid.get_cell(-1, 0, 1)

        # Act
        self.player.move_one(cell)

        # Assert
        self.assertTrue(self.player in cell.get_players())
        self.assertTrue(self.player not in start_cell.get_players())
        self.assertEqual(self.player.energy, 38)

    def test_player_move_event(self):
        # Arrange
        start_cell = self.hexgrid.get_cell(0, 0, 0)
        cell = self.hexgrid.get_cell(-1, 0, 1)
        event = HealthEvent(amount=10)
        cell.add_event(event)

        # Act
        self.player.move_one(cell)

        # Assert
        self.assertTrue(self.player in cell.get_players())
        self.assertTrue(self.player not in start_cell.get_players())

        self.assertEqual(self.player.health, 20)
        self.assertTrue(event not in cell.get_events())

    def test_player_move_no_energy(self):
        # Arrange
        cell = self.hexgrid.get_cell(-1, 0, 1)
        self.player.energy = 0

        # Act & Assert
        with self.assertRaises(AssertionError):
            self.player.move_one(cell)

    def test_player_illegal_move(self):
        # Arrange
        illegal_cell = self.hexgrid.get_cell(0, 2, -2)

        # Act & Assert
        with self.assertRaises(AssertionError):
            self.player.move_one(illegal_cell)

    def test_player_use_item(self):
        # Arrange
        # For prototype purposes, we will use HealthEvent as a granted item
        # proper implementation should use some kind of Item class
        item = HealthEvent(amount=10)
        self.player.inventory.append(item)

        # Act
        self.player.use_item(0)

        # Assert
        self.assertTrue(item not in self.player.inventory)
        self.assertTrue(item in self.player.cell.get_events())
