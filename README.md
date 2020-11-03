# diabotical_leaderboard
cli api for getting deabotical players stats


Queries are executed with requests lib.
CL arguments are parsed with getopt.


- To get data about <N> players in <MODE> game mode type:

  python leaderboard.py --mode <MODE> [--count <N>]

without N specified all the results will be printed


- To get data about user with <USER_ID> in specific <MODE>, considering <N> use:
  
  python leaderboard.py --mode <MODE> --user_id <USER_ID> --count <N>


- To count number of players in <MODE> from <COUNTRY> use:
  
  python leaderboard.py --mode <MODE> --country <COUNTRY> --count <N>
  
 where <COUNTRY> is country code that contains 2 letters(gb, de, ru, etc.)
