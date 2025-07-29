import logging


class MenuView:
    """Handles the main menu display and user interactions."""

    def __init__(self, player_controller, match_controller):
        self.player_controller = player_controller
        self.match_controller = match_controller

    def run(self):
        while True:
            print("\n=== Main Menu ===")
            print("1. Add a player")
            print("2. Create a match")
            print("3. View players")
            print("4. View matches")
            print("5. Quit")
            choice = input("Choice: ").strip()
            logging.debug(f"User choice: {choice}")
            print(f"[DEBUG] User choice: {choice}")

            if choice == "1":
                name = input("Player name: ").strip()
                if self.player_controller.add_player(name):
                    print(f" Player '{name}' added.")
                else:
                    print("❌ Invalid or duplicate player.")

            elif choice == "2":
                players = self.player_controller.list_players()
                if len(players) < 2:
                    print(" Not enough players.")
                    continue
                print("List of players:")
                for i, p in enumerate(players):
                    print(f"{i+1}. {p}")
                try:
                    i1 = int(input("Player 1 (number): ")) - 1
                    i2 = int(input("Player 2 (number): ")) - 1
                    result = input("Result (1, 2 or 0 for draw): ")
                    if self.match_controller.create_match(i1, i2, result):
                        print(" Match recorded.")
                    else:
                        print(" Invalid match data.")
                except ValueError:
                    print(" Invalid input.")

            elif choice == "3":
                players = self.player_controller.list_players()
                if not players:
                    print("No players.")
                else:
                    print("Registered players:")
                    for p in players:
                        print(f"- {p}")

            elif choice == "4":
                matches = self.match_controller.list_matches()
                if not matches:
                    print("No matches recorded.")
                else:
                    print("List of matches:")
                    for m in matches:
                        j1, j2 = m["joueur1"], m["joueur2"]
                        s1, s2 = m["score"]
                        print(f"{j1} ({s1}) vs {j2} ({s2})")

            elif choice == "5":
                print(" Goodbye!")
                logging.info("Application closed")
                print("[DEBUG] Application terminated")
                break
            else:
                print(" Invalid choice.")
                logging.warning(f"Invalid choice entered: {choice}")
                print("[DEBUG] Invalid choice")
