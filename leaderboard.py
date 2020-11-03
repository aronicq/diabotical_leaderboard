import requests
import sys
from getopt import getopt, GetoptError


def parse_args(argv):
    # decomposing string
    opts = ""
    flag_explain = False
    try:
        opts, args = getopt(argv, "h", ['mode=', 'count=', 'user_id=', 'country='])
    except GetoptError:
        flag_explain = True

    count = 0
    game_mode = user_id = country = ""
    for opt, arg in opts:
        if opt == '--mode':
            game_mode = arg

        elif opt == '-h':
            flag_explain = True

        elif opt == '--count':
            try:
                count = int(arg)
            except ValueError:
                print("--count N should be a number")
                sys.exit(2)

            if count < 1:
                print("--count should be > 0. Ignoring this argument")
                count = 0

        elif opt == '--user_id':
            user_id = arg

        elif opt == '--country':
            country = arg.lower()
            if len(country) != 2:
                print("Country code should contain 2 letters. Ignoring this argument")
                country = ""

    if game_mode == "" and user_id == "" and country == "":
        flag_explain = True

    if flag_explain:
        print('''
        usage: python leaderboard.py    [-h]                    - this message, 
                                        --mode <MODE>           - specify game mode (string)
                                        [--count N]             - first N occurrences (integer)
                                        [--user_id <user_id>]   - select specific uaer_id(str)
                                        [--country <country>]   - specify country(2 letter code: GB, DE etc.))
        
        --mode <MODE> [--count N]                                           print N players that play in MODE gamemode
        --mode <MODE> --user_id <user_id> [--count N]                       print N players from MODE with USER_ID
        --mode <MODE> --country <country> [--count N]                       print number of players from COUNTRY with maximum of N
        ''')
        sys.exit(2)

    if game_mode == "":
        print("game mode is not specified")

    if game_mode not in ['r_macguffin', 'r_wo', 'r_rocket_arena_2', 'r_shaft_arena_1', 'r_ca_2', 'r_ca_1']:
        print("possible game modes: r_macguffin, r_wo, r_rocket_arena_2, r_shaft_arena_1, r_ca_2, r_ca_1")

    return game_mode, {"count": count,
                       "user_id": user_id,
                       "country": country}


def filter_by_args(unfiltered_set, args):
    user_id = args["user_id"]
    country = args["country"]
    res = unfiltered_set

    if int(args["count"]) > 0:
        count = int(args["count"])
    else:
        count = len(res)

    for entry in res:
        entry.pop('user_id')

    if user_id:
        res = list(filter(lambda x: user_id == x["user_id"], res))
    elif country:
        return len(list(filter(lambda x: country == x["country"], res)))

    res = res[:count]

    return res


if __name__ == '__main__':
    mode, arguments = parse_args(sys.argv[1:])

    try:
        full_table = requests.get("https://www.diabotical.com/api/v0/stats/leaderboard?mode=" + mode)
    except requests.exceptions.ConnectionError:
        print("Connection error. Try again later")
        sys.exit()

    print({"queried_data": filter_by_args(full_table.json()["leaderboard"], arguments)})
