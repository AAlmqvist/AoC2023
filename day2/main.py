import sys
sys.path.append('../')

from tools.parsing import read_by_line

CUBE_LIMITS = {
    "red": 12,
    "green": 13,
    "blue": 14
    }

# data has form:
# Game X: <set>; <set>; <set>;...
# where each set is:
# X red, Y green, Z blue
# in any order of colors
def parse_data(s):
    game = []
    set_data = s.split(": ")[1]
    for set in set_data.split("; "):
        cubes = {}
        for cube in set.split(", "):
            info = cube.split(" ")
            cubes[info[1]] = int(info[0])
        game.append(cubes)
    return game

def run():
    # Read and parse the data line-by-line
    games = read_by_line("input.txt", parse_func=parse_data)

    # Set up the varaiables that saves the final 
    count_possible = 0
    total_game_power = 0
    # Iterate over each game
    for (g_id, game) in enumerate(games):
        # Minimum required cubes for each color in the game
        # (Assume at least one of each color, mulitplication still gives us a value if not)
        min_req_cubes = {
            "red": 1,
            "green": 1,
            "blue": 1
        }
        # Assume game is possible until we see that it is not
        possible_game = True
        # Iterate over the sets in the game
        for set in game:
            for color, number in set.items():
                # If number is bigger than the allowed limit game is not
                if CUBE_LIMITS[color] < number:
                    possible_game = False
                # Update records if we need more than previously seen
                if min_req_cubes[color] < number:
                    min_req_cubes[color] = number
        # If game was possible, add its id to the possible-counter
        if possible_game:
            count_possible += g_id+1
        # Calculate the games power and save it to the total
        power = 1
        for _, minimum in min_req_cubes.items():
            power *= minimum
        total_game_power += power
    print(count_possible)
    print(total_game_power)

if __name__ == "__main__":
    run()