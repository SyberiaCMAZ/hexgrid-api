import unittest

from abstract.hexgrid import HexGrid
from abstract.player import Player

from .map_json import json_data


class HexGridTestCase(unittest.TestCase):

    def test_hexgrid_from_json(self):
        # Arrange

        # Act
        hex_grid = HexGrid.from_json(json_data)

        # Assert
        self.assertEqual(len(hex_grid._cells), 8)
        self.assertEqual(hex_grid._cells[(0, 0, 0)].cell_type, "forest")
        self.assertEqual(hex_grid._cells[(0, 1, -1)].cell_type, "plains")
        self.assertEqual(hex_grid._cells[(1, 0, -1)].cell_type, "mountains")

    def test_hex_grid_add_player(self):
        # Arrange
        hex_grid = HexGrid.from_json(json_data)
        player = Player("Szefito")

        # Act
        hex_grid.add_player(player, 0, 0, 0)
        cell = hex_grid.get_cell(0, 0, 0)

        # Assert
        self.assertTrue(player.player_id in hex_grid.players)
        self.assertTrue(player in cell._players.values())
