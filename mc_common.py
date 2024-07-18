def did_player1_won_game(player_one_scores, player_two_scores, player_one_game, player_two_game, game_number, set_number, games):
    is_player_one_won = True
    is_player_one_won = did_player_one_win(player_one_scores[-1], player_two_scores[-1])
    if player_one_scores[-1] == '40' and player_two_scores[-1] == '40':
        player1_game = int(player_one_game)
        player2_game = int(player_two_game)
        if game_number == 1:
            is_player_one_won = True if player1_game > player2_game else False
        else:
            prev_player1_game = 0
            if game_number > 1:
                prev_game = games[(set_number, game_number - 1)]
                if prev_game:
                    for point in prev_game:
                        if (point[5] == '0' and point[6] == '0'):
                            prev_player1_game = int(point[3])
                            break
                if player1_game > prev_player1_game:
                    is_player_one_won = True
                else:
                    is_player_one_won = False
    return is_player_one_won

def did_player_one_win(player_one_score, player_two_score):
    # Convert "A" to 100
    if player_one_score == "A":
        player_one_score = 100
    else:
        player_one_score = int(player_one_score)

    if player_two_score == "A":
        player_two_score = 100
    else:
        player_two_score = int(player_two_score)

    # Determine if player one won
    return player_one_score > player_two_score