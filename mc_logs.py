from mc_common import did_player1_won_game

html_log_styles = '''
<style>
.score-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #e1e1e1;
    font: 400 14px / 20px "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.score-finish-row {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    align-items: center;
    padding: 10px 0;
    border-bottom: 1px solid #e1e1e1;
    color: #000;
    font: 400 14px / 20px "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.top-row, .bottom-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 0;
    width: 100%;
}
.score-row:last-child {
    border-bottom: none;
}
.player-score, .opponent-score {
    width: 60px;
    text-align: center;
    color: #333;
}
.event-detail {
    flex: 1;
    margin: 0 40px;
    color: #666;
}
.arrow {
    color: #222226;
    margin-left: 25px;
    margin-right: 10px; /* Spacing between arrow and data */
    transition: transform 0.3s; /* Smooth transition for rotating the arrow */
}
.expanded-content {
    display: none;
}
.expanded-content {
    display: none;
}
.log-container {
    display: none;
}
</style>
'''

html_container_start = '''<div elevation="2" class="Box ibMVdI">'''
html_div_end = "</div>"

html_scripts = '''
<script src="https://cdn.startbootstrap.com/sb-forms-latest.js"></script>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

        <script>
            $(document).ready(function() {
            $('.score-finish-row').click(function() {
                $(this).next('.expanded-content').toggle();

                // Check the current rotation state
                if ($(this).find('.arrow').css('transform') === 'none') {
                    $(this).find('.arrow').css('transform', 'rotate(90deg)');
                } else {
                    $(this).find('.arrow').css('transform', '');
                }
            });
        });
        </script>
'''

html_in_score_scripts = '''
<script src="https://cdn.startbootstrap.com/sb-forms-latest.js"></script>
        <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>

        <script>
            $(document).ready(function() {
                $('.game-item-for-log').click(function() {
                    var $nextSibling = $(this).next();
                    
                    // Check if the next sibling has the .log-container class
                    if ($nextSibling.hasClass('log-container')) {
                        $nextSibling.slideToggle(400);
                    } else {
                        // Find the first child element with the class .log-container and toggle it
                        $nextSibling.find('.log-container').first().slideToggle(400);
                    }
                });
            });

        </script>
'''

html_finish_row = '''
<div class="score-finish-row">
    <div class="top-row">
        <span class="player-score" style="font-weight: bold;">{player1_set_score}</span>
        <span class="event-detail" align="center" style="font-weight: bold;color:#333">{game_details}</span>
        <span class="opponent-score" style="font-weight: bold;">{player2_set_score}</span>
    </div>
    <div class="bottom-row">
        {toggle_placeholder}
        <span class="event-detail" align="center" style="color:#333">{details}</span>
        {toggle_placeholder2}
    </div>
</div>
'''

html_toggle_placeholder = '''<span class="arrow">&#x25B6;</span>'''
html_toggle_placeholder2 = '''<span class="opponent-score"></span>'''

html_score_row = '''
<div class="score-row">
    <span class="player-score">{player1_set_score}</span>
    <span class="event-detail" align="center">{details}</span>
    <span class="opponent-score">{player2_set_score}</span>
</div>
'''

html_game_start = '''<div class="expanded-content">'''

html_div_start = "<div>"

html_game_container_start = '''<div class="log-container">'''

def get_team_name(player):
    return f"{player.name}/{player.double_name}" if player.double_name else player.name

def get_game_log_html(sets, games, player1, player2, set, game_number, game_start, show_in_scores = False):
    player_one_scores = []
    player_two_scores = []
    player1_name = get_team_name(player1)
    player2_name = get_team_name(player2)
    game = games[(set, game_number)]
    player_one_scores = []
    player_two_scores = []
    game_content = ''
    for point in game:
        #print(point)
        point_content = ''
        if (point[5] == '0' and point[6] == '0'):
            player_one_game = str(point[3])
            player_two_game = str(point[4])
            is_player_one_won = did_player1_won_game(player_one_scores, player_two_scores, player_one_game, player_two_game, game_number, set, games)
            team_won = player1_name if is_player_one_won else player2_name
            is_last_game = game_number == len(sets[set])
            is_last_set = set == len(sets)
            last_game = "Set, " if is_last_game else ''
            last_set = "Match, " if (is_last_set and last_game) else ''
            game_details = f'Game, {last_game}{last_set}{team_won}'
            point_content = html_finish_row.replace("{player1_set_score}", "" if show_in_scores else point[3])\
                .replace("{player2_set_score}", "" if show_in_scores else point[4])\
                .replace("{details}", point[8])\
                .replace("{game_details}", "" if show_in_scores else game_details)\
                .replace("{toggle_placeholder}", "" if show_in_scores else html_toggle_placeholder)\
                .replace("{toggle_placeholder2}", "" if show_in_scores else html_toggle_placeholder2)
            
            point_content = point_content + html_div_start if show_in_scores else html_game_start
            game_start = True
        else:
            player_one_scores.append(point[5])
            player_two_scores.append(point[6])
            point_content = html_score_row.replace("{player1_set_score}", point[5])\
                .replace("{player2_set_score}", point[6])\
                .replace("{details}", point[8])
            if game_start:
                point_content = point_content + html_div_end
                game_start = False

        game_content = point_content + game_content
    game_content = html_game_container_start + game_content + html_div_end
    return game_content, game_start

def get_logs_html(sets, games, player1, player2):
    html_content = ""
    game_start = True

    for (set, game_number), game in games.items():
        game_content, game_start = get_game_log_html(sets, games, player1, player2, set, game_number, game_start)
        html_content = game_content + html_content

    if not game_start:
        html_content = "<div>" + html_content

    html_content = html_log_styles + html_container_start + html_content + html_div_end + html_scripts
    return html_content