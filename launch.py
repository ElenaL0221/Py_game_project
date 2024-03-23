import json
import game


def launch(screen, k):
    with open(f'data/levels/{k}.json', 'r') as file:
        file = json.load(file)
        player_pos = file["PLAYER_POSITION"]
        platform_size = file['PLATFORM_SIZE']
        level = file["LEVEL"]
        exit_position = file["EXIT_POSITION"]
        return game.main(screen, player_pos, platform_size, level, exit_position)
