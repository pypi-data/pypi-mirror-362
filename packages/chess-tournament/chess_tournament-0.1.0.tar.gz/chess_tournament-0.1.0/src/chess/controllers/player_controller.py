import json
import os
import logging


class PlayerController:
    """Handles player-related operations."""

    FILE_PATH = "data/players.json"

    def __init__(self):
        logging.debug("Loading players from JSON file")
        print("[DEBUG] Initializing PlayerController")
        self.players = self.load_players()

    def load_players(self):
        if not os.path.exists(self.FILE_PATH):
            logging.warning("players.json file not found, creating a new list")
            print("[DEBUG] Player file not found, returning empty list")
            return []
        with open(self.FILE_PATH, "r", encoding="utf-8") as f:
            print("[DEBUG] Loading existing player file")
            return json.load(f)

    def save_players(self):
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.players, f, indent=2, ensure_ascii=False)
        logging.info("Players saved")
        print("[DEBUG] Players saved to file")

    def add_player(self, name):
        if name and name not in self.players:
            self.players.append(name)
            self.save_players()
            logging.info(f"Player added: {name}")
            print(f"[DEBUG] Player added: {name}")
            return True
        logging.warning(f"Invalid or duplicate player addition attempt: {name}")
        print(f"[DEBUG] Failed to add player: {name}")
        return False

    def list_players(self):
        print("[DEBUG] Player list returned")
        return self.players
