import argparse
import logging
from .controllers.player_controller import PlayerController
from .controllers.match_controller import MatchController
from .views.menu import MenuView
from .logger import setup_logging

logger = logging.getLogger(__name__)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--quiet", action="store_true", help="Suppress info logs")
    args = parser.parse_args()

    setup_logging(quiet=args.quiet)
    logger.info("Logger initialized")

    logger.info("Initializing controllers")
    player_controller = PlayerController()
    match_controller = MatchController(player_controller)
    menu = MenuView(player_controller, match_controller)

    logger.info("Starting application")
    menu.run()


if __name__ == "__main__":
    main()
