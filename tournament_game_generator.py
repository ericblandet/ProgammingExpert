"""
First version,
in a script way
"""

ask_number_of_teams = "Enter the number of teams in the tournament: "
ask_number_of_games_played = "Enter the number of games played by each team: "
ask_team_name = "Enter the name for team #"
ask_number_of_games = "Enter the number of games played by each team: "
ask_number_of_wins = "Enter the number of wins Team "

err_minimum_number_of_teams = "The minimum number of teams is 2, try again."
err_mimimum_chars_for_names = "Team names must have at least 2 characters, try again."
err_max_words_for_names = "Team names may have at most 2 words, try again."
err_number_of_games = "Invalid number of games. Each team plays each other at least once in the regular season, try again."
err_min_number_of_wins = "The minimum number of wins is 0, try again."
err_max_number_of_wins = "The minimum number of wins is MAX_NUM, try again."

gen_games_to_be_played = "Generating the games to be played in the first round of the tournament..."


while True:
    number_of_teams = int(input(ask_number_of_teams))
    if number_of_teams < 2:
        print(err_minimum_number_of_teams)
    else:
        break

teams = {}
for i in range(number_of_teams):
    while True:
        team_name = input(f"{ask_team_name}{i+1}: ")
        if len(team_name) < 2:
            print(err_mimimum_chars_for_names)
        elif len(team_name.split(" ")) > 2:
            print(err_max_words_for_names)
        else:
            break
    teams[team_name] = 0

while True:
    number_of_played_games = int(input(ask_number_of_games))
    if number_of_played_games >= len(teams)-1:
        break
    print(err_number_of_games)

for team in teams.keys():
    while True:
        team_wins = int(input(f"{ask_number_of_wins}{team}: "))
        if team_wins < 0:
            print(err_min_number_of_wins)
        elif team_wins > number_of_played_games:
            print(err_max_number_of_wins.replace(
                "MAX_NUM", str(number_of_played_games)))
        else:
            teams[team] = team_wins
            break

sorted_teams = sorted(teams.items(), key=lambda x: x[1], reverse=True)
print(sorted_teams)

for i in range(int(len(sorted_teams)/2)):
    print(f"HOME: {sorted_teams[-(i+1)][0]} VS AWAY: {sorted_teams[i][0]}")
