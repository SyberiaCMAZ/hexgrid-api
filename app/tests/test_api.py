import unittest

from main import create_app
from starlette.testclient import TestClient


class ApiEventTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app()
        self.client = TestClient(app)

    def test_event_create(self):
        # Arrange
        with self.client as client:
            # Act
            response = client.post(
                "/events/create",
                json={
                    "name": "HealthEvent",
                    "amount": 10,
                    "q": 0,
                    "r": 0,
                    "s": 0,
                },
            )

            # Assert
            self.assertEqual(response.status_code, 200)


class ApiHexGridTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app()
        self.client = TestClient(app)

    def test_hexgrid_map(self):
        # Arrange
        with self.client as client:
            # Act
            response = client.get("hexgrid/map")

            # Assert
            self.assertEqual(response.status_code, 200)


class ApiPlayerTestCase(unittest.TestCase):

    def setUp(self):
        app = create_app()
        self.client = TestClient(app)

    def test_player_create(self):
        # Arrange
        with self.client as client:
            # Act
            response = client.post(
                "/player/create",
                json={
                    "name": "Szefito",
                },
            )

            # Assert
            self.assertEqual(response.status_code, 200)

    def test_player_get(self):
        # Arrange
        with self.client as client:
            response = client.post(
                "/player/create",
                json={
                    "name": "Szefito",
                },
            )
            player_id = response.json()["player_id"]

            # Act
            response = client.get(f"/player/get/{player_id}")

            # Assert
            self.assertEqual(response.status_code, 200)

    def test_player_move(self):
        # Arrange
        with self.client as client:
            response = client.post(
                "/player/create",
                json={
                    "name": "Szefito",
                },
            )
            player_id = response.json()["player_id"]

            # Act
            response = client.post(
                "/player/move",
                json={
                    "player_id": player_id,
                    "q": -1,
                    "r": 0,
                    "s": 1,
                },
            )

            # Assert
            self.assertEqual(response.status_code, 200)

    def test_player_illegal_move(self):
        # Arrange
        with self.client as client:
            response = client.post(
                "/player/create",
                json={
                    "name": "Szefito",
                },
            )
            player_id = response.json()["player_id"]

            # Act
            response = client.post(
                "/player/move",
                json={
                    "player_id": player_id,
                    "q": -2,
                    "r": 0,
                    "s": 2,
                },
            )

            # Assert
            self.assertEqual(response.status_code, 400)
