import json
import os
import logging


class MatchController:
    """Handles the creation and viewing of matches."""

    FILE_PATH = "data/matches.json"

    def __init__(self, player_controller):
        self.player_controller = player_controller
        logging.debug("Loading matches from JSON file")
        print("[DEBUG] Initializing MatchController")
        self.matches = self.load_matches()

    def load_matches(self):
        if not os.path.exists(self.FILE_PATH):
            logging.warning("matches.json file not found, creating a new list")
            print("[DEBUG] Match file not found, returning empty list")
            return []
        with open(self.FILE_PATH, "r", encoding="utf-8") as f:
            print("[DEBUG] Loading existing match file")
            return json.load(f)

    def save_matches(self):
        with open(self.FILE_PATH, "w", encoding="utf-8") as f:
            json.dump(self.matches, f, indent=2, ensure_ascii=False)
        logging.info("Matches saved")
        print("[DEBUG] Matches saved to file")

    def create_match(self, idx1, idx2, result):
        players = self.player_controller.list_players()
        try:
            p1 = players[idx1]
            p2 = players[idx2]
        except IndexError:
            logging.error("Invalid player index for match")
            print("[DEBUG] Invalid player index")
            return False

        if idx1 == idx2:
            logging.warning("A player cannot play against themselves")
            print("[DEBUG] Player against themselves")
            return False

        if result == "1":
            score = [1, 0]
        elif result == "2":
            score = [0, 1]
        elif result == "0":
            score = [0.5, 0.5]
        else:
            logging.error(f"Invalid result provided: {result}")
            print(f"[DEBUG] Invalid result: {result}")
            return False

        self.matches.append({"joueur1": p1, "joueur2": p2, "score": score})
        self.save_matches()
        logging.info(f"Match created between {p1} and {p2} with score {score}")
        print(f"[DEBUG] Match added: {p1} vs {p2}, score {score}")
        return True

    def list_matches(self):
        print("[DEBUG] Match list returned")
        return self.matches
