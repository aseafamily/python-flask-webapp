var_styles = '''
:root {
    --on-color-primary: #ffffff;
    --on-surface-nLv1: #222226;
    --on-surface-nLv3: rgba(34, 34, 38, 0.45);
    --on-surface-nLv4: rgba(34, 34, 38, 0.15);
    --on-surface-nLv5: rgba(34, 34, 38, 0.06);
    --error-default: #c7361f;
    --surface-s0: #edf1f6;
    --surface-s1: #ffffff;
    --playoffs-promotion-to-x-playoff: #0a8dff;
    --effect-elevation: rgba(34, 34, 38, 0.08);
    --primary-default: #374df5;
    --secondary-default: #0bb32a;
    --terrain-grass:#62bd40;
    --sofa-singles-value:#e59c03;
}
'''

all_styles = '''
.ibMVdI {
    background-color: var(--surface-s1);
    margin-top: 8px;
    margin-bottom: 8px;
    border-radius: 16px;
    box-shadow: 0 1px 4px var(--effect-elevation);
}

.fTPNOD {
    padding-bottom: 8px;
}

.kFvGEE {
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
}
.cXlkKQ {
    display: flex;
    height: 40px;
    padding-top: 16px;
    padding-bottom: 8px;
    cursor: pointer;
}
.jankPa {
    color: var(--on-surface-nLv3);
    text-align: center;
    font: 500 12px / 100% "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.cQgcrM {
    display: flex;
}
.kfFlmy {
    display: flex;
    padding-left: 8px;
    padding-right: 8px;
}
.dflyPx {
    padding-top: 8px;
    padding-bottom: 8px;
}
.fDdOoq {
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: end;
    justify-content: flex-end;
}
.fYweFT {
    display: flex;
    height: 20px;
    width: 48px;
    padding-right: 8px;
}
.hykCvB {
    min-width: 20px;
    color: var(--on-surface-nLv3);
    text-align: center;
    font: 400 14px "Sofascore Sans Condensed", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.beJYhm {
    background-color: transparent;
    height: 8px;
    width: 8px;
    margin-left: 2px;
    border-radius: 4px;
}
.iDpWxX {
    min-width: 20px;
    color: var(--on-surface-nLv1);
    text-align: center;
    font: 400 14px "Sofascore Sans Condensed", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.jJmlRA {
    background-color: var(--secondary-default);
    height: 8px;
    width: 8px;
    margin-left: 2px;
    border-radius: 4px;
}
.kKsFYo {
    display: inline-block;
    flex: 0 0 1px;
    align-self: stretch;
    width: 1px;
    background-color: var(--on-surface-nLv4);
    margin-top: 8px;
    margin-bottom: 8px;
}
.IBiIm {
    display: flex;
    padding-left: 9px;
}
.kpyaMP {
    display: flex;
    flex-wrap: wrap;
}
.fZBqrX {
    margin-right: 4px;
    padding-top: 8px;
    padding-bottom: 8px;
}
.gcTSCL {
    height: 20px;
    width: 24px;
    color: var(--on-surface-nLv3);
    text-align: center;
    font: 400 14px / 20px "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.ifCmHJ {
    height: 20px;
    width: 24px;
    color: var(--on-surface-nLv1);
    text-align: center;
    font: 400 14px / 20px "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.gGggNo {
    height: 20px;
    width: 24px;
    color: var(--secondary-default);
    text-align: center;
    font: 400 14px / 20px "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.match_point {
    font-weight:bold;
}
.dBlMgN {
    height: 20px;
    width: 24px;
    color: var(--sofa-singles-value);
    text-align: center;
    font: 400 14px / 20px "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.bebVlb {
    margin-right: 2px;
}
.BalFY {
    display: block;
    margin: 0px;
    border-right-width: initial;
    border-bottom-width: initial;
    border-left-width: initial;
    border-style: solid none none;
    border-image: initial;
    border-top-width: 1px;
    border-color: var(--on-surface-nLv4);
    background: none;
}
'''

toggle_script_html = '''
<script>
    document.addEventListener("DOMContentLoaded", function() {
        const toggleDivs = document.querySelectorAll(".cXlkKQ");

        toggleDivs.forEach(function(toggleDiv) {
            toggleDiv.addEventListener("click", function() {
                const siblings = Array.from(toggleDiv.parentNode.children).filter(function(child) {
                    return child !== toggleDiv && child.tagName.toLowerCase() === 'div'
                });

                let allHidden = false;
                siblings.forEach(function(sibling) {
                    if (sibling.style.display === "flex" || sibling.style.display === "") {
                        sibling.style.display = "none";
                        allHidden = true;
                    } else {
                        sibling.style.display = "flex";
                        allHidden = false;
                    }
                });

                const svgPath = toggleDiv.querySelector("svg path");
                if (allHidden) {
                    svgPath.setAttribute("d", "M11.99 18 4 9.942 5.42 8.51l6.57 6.636 6.6-6.646L20 9.922z");
                } else {
                    svgPath.setAttribute("d", "M11.99 6 4 14.058l1.42 1.432 6.57-6.636 6.6 6.646L20 14.078z");
                }
            });
        });
    });
</script>'''

divider_html = '''<hr class="HorizontalDivider BalFY">'''

set_header_html = '''<div display="flex" cursor="pointer" class="Box Flex cXlkKQ kFvGEE">
            <div color="onSurface.nLv3" class="Text jankPa">{SET_NAME}</div>
            <svg width="24" height="24" viewBox="0 0 24 24" fill="var(--on-surface-nLv1)" class="SvgWrapper bhEsNK">
                <path fill="var(--on-surface-nLv1)" d="M11.99 6 4 14.058l1.42 1.432 6.57-6.636 6.6 6.646L20 14.078z" fill-rule="evenodd" ml="4px"></path>
            </svg>
        </div>'''

game_header_html = '''<div class="Box dflyPx">
                <div class="Box klGMtt">
                    <div display="flex" class="Box Flex fYweFT fDdOoq">
                        {player_one_break}
                        <div color="onSurface.nLv3" class="Text {player_one_style_name}">{player_one_game}</div>
                        {player_one_serve_html}
                    </div>
                    <div display="flex" class="Box Flex fYweFT fDdOoq">
                        {player_two_break}
                        <div color="onSurface.nLv1" class="Text {player_two_style_name}">{player_two_game}</div>
                        {player_two_serve_html}
                    </div>
                </div>
            </div>
            <div class="VerticalDivider kKsFYo"></div>'''

div_end = '</div>'
match_div_start = '''<div elevation="2" class="Box ibMVdI">'''
set_div_start = '''<div class="Box fTPNOD">'''
game_div_start = '''<div display="flex" class="Box Flex kfFlmy cQgcrM">'''
color_won_style_name = 'iDpWxX'
color_lost_style_name = 'hykCvB'
serve_html = '''<div class="Box jJmlRA"></div>'''
receive_html = '''<div class="Box beJYhm"></div>'''
player_one_break_html = '''<svg width="8" height="12" viewBox="0 0 8 12" fill="var(--secondary-default)" class="SvgWrapper bebVlb">
                            <path d="M6.956 3.31c.029.224.044.455.044.69 0 1.741-.834 3.223-2 3.772V11a1 1 0 0 1-2 0V7.772c-.562-.265-1.047-.747-1.4-1.37L6.957 3.31zM4 0c1.057 0 1.986.728 2.52 1.829L1.088 4.965A5.286 5.286 0 0 1 1 4c0-2.21 1.343-4 3-4z" fill="var(--secondary-default)" fill-rule="evenodd" mr="xxs"></path>
                        </svg>'''
player_two_break_html = '''<svg width="8" height="12" viewBox="0 0 8 12" fill="var(--primary-default)" class="SvgWrapper bebVlb">
                            <path d="M6.956 3.31c.029.224.044.455.044.69 0 1.741-.834 3.223-2 3.772V11a1 1 0 0 1-2 0V7.772c-.562-.265-1.047-.747-1.4-1.37L6.957 3.31zM4 0c1.057 0 1.986.728 2.52 1.829L1.088 4.965A5.286 5.286 0 0 1 1 4c0-2.21 1.343-4 3-4z" fill="var(--primary-default)" fill-rule="evenodd" mr="xxs"></path>
                        </svg>'''
game_scores_div_start = '''<div display="flex" wrap="wrap" class="Box Flex IBiIm kpyaMP">'''
game_score_html = '''<div class="Box fZBqrX">
                    <div color="onSurface.nLv3" class="Text {player1_point_style}">{player1_score}</div>
                    <div color="onSurface.nLv1" class="Text {player2_point_style}">{player2_score}</div>
                </div>'''
point_won_style_name = 'ifCmHJ'
point_lost_style_name = 'gcTSCL'
break_point_style_name = 'dBlMgN'
set_point_style_name = 'gGggNo'

def ordinal(n):
    """Convert an integer into its ordinal representation"""
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

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

def get_styles(include_var):
    result = "<style>"
    if include_var:
        result += var_styles
    result += all_styles
    result += "</style>"
    return result

def get_set_header_html(set_name):
    set_header_content = set_header_html.replace("{SET_NAME}", set_name)
    return set_header_content

def get_game_header_html(player_one_game, player_two_game, is_player_one_serve, is_player_one_won, is_tie_break):
    player_one_break = ''
    player_two_break = ''

    if not is_tie_break:
        if is_player_one_serve:
            if not is_player_one_won:
                player_two_break = player_two_break_html
        else:
            if is_player_one_won:
                player_one_break = player_one_break_html
    
    game_header_content = game_header_html.replace("{player_one_game}", player_one_game)\
        .replace("{player_two_game}", player_two_game)\
        .replace("{player_one_style_name}", color_won_style_name if is_player_one_won else color_lost_style_name)\
        .replace("{player_two_style_name}", color_lost_style_name if is_player_one_won else color_won_style_name)\
        .replace("{player_one_serve_html}", receive_html if is_tie_break else (serve_html if is_player_one_serve else receive_html))\
        .replace("{player_two_serve_html}", receive_html if is_tie_break else (receive_html if is_player_one_serve else serve_html))\
        .replace("{player_one_break}", player_one_break)\
        .replace("{player_two_break}", player_two_break)
    
    return game_header_content

def get_game_score_html(player1_score, player2_score, last_player1_score, last_player2_score, is_ad_scoring, is_player_one_serve, is_player1_set_point, is_player2_set_point, is_match_point):
    is_player1_won_point = did_player_one_win(player1_score, last_player1_score)
    player1_point_style = point_won_style_name if is_player1_won_point else point_lost_style_name
    player2_point_style = point_lost_style_name if is_player1_won_point else point_won_style_name

    if player1_score == "A":
        player_one_score = 100
    else:
        player_one_score = int(player1_score)

    if player2_score == "A":
        player_two_score = 100
    else:
        player_two_score = int(player2_score)

    if is_ad_scoring:
        if is_player_one_serve:
            if player_two_score == 100 or (player_two_score == 40 and player_one_score < 40):
                player2_point_style = break_point_style_name
        else:
            if player_one_score == 100 or (player_one_score == 40 and player_two_score < 40):
                player1_point_style = break_point_style_name
    else:
        if is_player_one_serve:
            if player_two_score == 40:
                player2_point_style = break_point_style_name
        else:
            if player_one_score == 40:
                player1_point_style = break_point_style_name

    last_style = set_point_style_name
    if is_match_point:
        last_style += " match_point"
    player1_point_style = last_style if is_player1_set_point else player1_point_style
    player2_point_style = last_style if is_player2_set_point else player2_point_style

    game_score_content = game_score_html.replace("{player1_score}", player1_score)\
        .replace("{player2_score}", player2_score)\
        .replace("{player1_point_style}", player1_point_style)\
        .replace("{player2_point_style}", player2_point_style)

    return game_score_content

