html_style = '''
<style>
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

.ibMVdI {
    background-color: var(--surface-s1);
    margin-top: 8px;
    margin-bottom: 8px;
    border-radius: 16px;
    box-shadow: 0 1px 4px var(--effect-elevation);
}

.cRYpNI {
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    flex-direction: column;
}
.khXvuo {
    display: flex;
    width: 100%;
    padding-bottom: 20px;
}
.hDYGGX {
    margin-top: 12px;
    margin-bottom: 8px;
    color: var(--on-surface-nLv1);
    text-align: left;
    font: 700 14px / 1.14 "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.dsybxc {
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: center;
    justify-content: center;
    flex-direction: column;
}
.cWGKPx {
    display: flex;
    width: 100%;
    margin-top: 8px;
    margin-bottom: 16px;
}
.bnpRyo {
    display: flex;
    -webkit-box-align: center;
    align-items: center;
    -webkit-box-pack: justify;
    justify-content: space-between;
}
.heNsMA {
    display: flex;
    width: 100%;
    padding-bottom: 8px;
}
.hKQtHc {
    text-align: left;
    flex: 1 1 0px;
}
.iZtpCa {
    padding-left: 12px;
    color: var(--on-surface-nLv1);
    text-align: left;
    font: 400 14px / 1.14 "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.fUNIGw {
    text-align: center;
    flex: 1 1 0px;
}
.lluFbU {
    padding-left: 4px;
    padding-right: 4px;
    color: var(--on-surface-nLv1);
    text-align: center;
    font: 500 12px / 1.33 "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
}
.fIiFyn {
    text-align: right;
    flex: 1 1 0px;
}
.dIhevN {
    display: flex;
    width: 100%;
    padding-left: 8px;
    padding-right: 8px;
}
.dHDlAv {
    overflow: hidden;
    background-color: var(--on-surface-nLv5);
    height: 6px;
    width: 100%;
    border-radius: 8px;
}
.gUiltw {
    background-color: var(--secondary-default);
    height: 100%;
}
.dHDlAv {
    overflow: hidden;
    background-color: var(--on-surface-nLv5);
    height: 6px;
    width: 100%;
    border-radius: 8px;
}
.cVOaja {
    background-color: var(--primary-default);
    height: 100%;
}
.lfzhVF {
    padding-right: 12px;
    color: var(--on-surface-nLv1);
    text-align: left;
    font: 400 14px / 1.14 "Sofascore Sans", -apple-system, system-ui, BlinkMacSystemFont, Dubai, "Segoe UI", Tahoma, "Noto Sans Arabic UI", "Dejavu Sans", Arial, sans-serif;
}
.gxCBJe {
    padding: 0px 8px;
}
</style>
'''

html_all_start = '''
<div elevation="2" class="Box ibMVdI">
<div class="gxCBJe">
'''

html_all_end = '''
</div>
</div>'''

html_section_start = '''
<div display="flex" direction="column" class="Box Flex khXvuo cRYpNI">
    <span class="Text hDYGGX">{section_name}</span>'''

html_section_end = '''</div>'''

html_item_template = '''
<div display="flex" direction="column" class="Box Flex cWGKPx dsybxc">
        <div display="flex" class="Box Flex heNsMA bnpRyo">
            <bdi class="Box hKQtHc"><span class="Text iZtpCa">{p1}</span></bdi>
            <bdi class="Box fUNIGw"><div cursor="default" class="Box gmloMx"><span class="Text lluFbU">{title}</span></div></bdi>
            <bdi class="Box fIiFyn"><span class="Text lfzhVF">{p2}</span></bdi>
        </div>
        <div display="flex" class="Box Flex dIhevN cQgcrM" style="gap: 16px;">
            <div role="progressbar" overflow="hidden" class="Box dHDlAv">
                <div class="Box gUiltw" style="width: {p1_cent}%; opacity: {p1_op}; float: right;"></div>
            </div>
            <div role="progressbar" overflow="hidden" class="Box dHDlAv">
                <div class="Box cVOaja" style="width: {p2_cent}%; opacity: {p2_op};"></div>
            </div>
        </div>
    </div>
'''

def generate_item(title, p1, p2, n1, n2, reverse = False):
    n1 = int(n1)
    n2 = int(n2)
    won_op = "1"
    lost_op = "0.25"
    p1_op = p2_op = (won_op if (not reverse) else lost_op)
    if n1 > n2:
        p2_op = lost_op if (not reverse) else won_op
    elif n2 > n1:
        p1_op = lost_op if (not reverse) else won_op

    p1_cent = p2_cent = 0
    total = n1 + n2
    if total:
        p1_cent = (n1 / total) * 100
        p2_cent = (n2 / total) * 100

    html_item = html_item_template.replace("{title}", title)\
        .replace("{p1}", str(p1))\
        .replace("{p2}", str(p2))\
        .replace("{p1_op}", str(p1_op))\
        .replace("{p2_op}", str(p2_op))\
        .replace("{p1_cent}", str(p1_cent))\
        .replace("{p2_cent}", str(p2_cent))
    
    return html_item

def split_to_ints(s):
    # Split the string by the '/' character
    parts = s.split('/')
    
    # Convert the parts to integers
    int1 = int(parts[0])
    int2 = int(parts[1])
    
    return int1, int2

def percent_to_float(s):
    # Remove the percentage sign and convert to float
    return float(s.strip('%')) / 100

def process_player(player):
    player.total_points_won = 0

def generate_pecent_item(title, p1_won, p1_all, p2_won, p2_all, reverse = False, default_100 = False):
    p1_percent = int(100*p1_won/p1_all) if p1_all != 0 else (0 if not default_100 else 100)
    p2_percent = int(100*p2_won/p2_all) if p2_all != 0 else (0 if not default_100 else 100)
    p1_str = f"{p1_won}/{p1_all} ({p1_percent}%)"
    p2_str = f"{p2_won}/{p2_all} ({p2_percent}%)"

    return generate_item(title, p1_str, p2_str, p1_percent, p2_percent, reverse)

def generate_item_not_empty(player1, player2, title, prefix, reverse=False):
    html_content = ''
    key = f"{title} {prefix}"
    v1 = int(player1.data[key])
    v2 = int(player2.data[key])

    if v1 and v2:
        return generate_item(title, v1, v2, v1, v2, reverse)

    return html_content

def get_statistics_html(player1, player2):
    # make sure data is right


    html_content = html_style + html_all_start

    # Point
    html_content += html_section_start.replace("{section_name}", "Points")
    
    html_content += generate_item("Total", player1.total_points_won, player2.total_points_won, player1.total_points_won, player2.total_points_won)

    p1_1s_won, p1_1s_all = split_to_ints(player1.data['1st Serve Points Won'])
    p1_2s_won, p1_2s_all = split_to_ints(player1.data['2nd Serve Points Won'])
    p1_1s_won_r, p1_1s_all_r = split_to_ints(player1.data['1st Return Points Won'])
    p1_2s_won_r, p1_2s_all_r = split_to_ints(player1.data['2nd Return Points Won'])
    p2_1s_won, p2_1s_all = split_to_ints(player2.data['1st Serve Points Won'])
    p2_2s_won, p2_2s_all = split_to_ints(player2.data['2nd Serve Points Won'])
    p2_1s_won_r, p2_1s_all_r = split_to_ints(player2.data['1st Return Points Won'])
    p2_2s_won_r, p2_2s_all_r = split_to_ints(player2.data['2nd Return Points Won'])

    p1_1s_percent = int((p1_1s_all / (p1_1s_all + p1_2s_all)) * 100)
    p2_1s_percent = int((p2_1s_all / (p2_1s_all + p2_2s_all)) * 100)
    p1_2s_percent = int(((p1_2s_all - int(player1.double_faults)) / p1_2s_all) * 100)
    p2_2s_percent = int(((p2_2s_all - int(player2.double_faults)) / p2_2s_all) * 100)

    p1_s_all = p1_1s_all + p1_2s_all
    p1_s_won = p1_1s_won + p1_2s_won
    p1_s_all_r = p1_1s_all_r + p1_2s_all_r
    p1_s_won_r = p1_1s_won_r + p1_2s_won_r
    P1_s_won_percent = (p1_s_won / p1_s_all) * 100
    P1_s_won__r_percent = (p1_s_won_r / p1_s_all_r) * 100

    p2_s_all = p2_1s_all + p2_2s_all
    p2_s_won = p2_1s_won + p2_2s_won
    p2_s_all_r = p2_1s_all_r + p2_2s_all_r
    p2_s_won_r = p2_1s_won_r + p2_2s_won_r
    P2_s_won_percent = (p2_s_won / p2_s_all) * 100
    P2_s_won__r_percent = (p2_s_won_r / p2_s_all_r) * 100


    html_content += generate_item("Service points won", p1_s_won, p2_s_won, p1_s_won, p2_s_won)
    html_content += generate_item("Receiver points won", p1_s_won_r, p2_s_won_r, p1_s_won_r, p2_s_won_r)
    html_content += generate_item("Max points in a row", player1.max_points_in_a_row, player2.max_points_in_a_row, player1.max_points_in_a_row, player2.max_points_in_a_row)

    if (player1.touch_5_8 + player2.touch_5_8 + player1.touch_9_plus + player2.touch_9_plus) > 0:
        html_content += generate_item("Touch 0-4", player1.touch_0_4, player2.touch_0_4, player1.touch_0_4, player2.touch_0_4)
        html_content += generate_item("Touch 5-8", player1.touch_5_8, player2.touch_5_8, player1.touch_5_8, player2.touch_5_8)
        html_content += generate_item("Touch 9+", player1.touch_9_plus, player2.touch_9_plus, player1.touch_9_plus, player2.touch_9_plus)
    
    html_content += html_section_end

    # Service
    html_content += html_section_start.replace("{section_name}", "Service")
    
    html_content += generate_item("Aces", player1.aces, player2.aces, player1.aces, player2.aces)
    html_content += generate_item("Double faults", player1.double_faults, player2.double_faults, player1.double_faults, player2.double_faults, True)
    
    p1_1s_str = f"{p1_1s_all}/{p1_1s_all + p1_2s_all} ({p1_1s_percent}%)"
    p2_1s_str = f"{p2_1s_all}/{p2_1s_all + p2_2s_all} ({p2_1s_percent}%)"
    #html_content += generate_item("First serve", p1_1s_str, p2_1s_str, p1_1s_percent, p2_1s_percent)
    html_content += generate_pecent_item("First serve", p1_1s_all, (p1_1s_all + p1_2s_all), p2_1s_all, (p2_1s_all + p2_2s_all))

    p1_2s_str = f"{p1_2s_all - int(player1.double_faults)}/{p1_2s_all} ({p1_2s_percent}%)"
    p2_2s_str = f"{p2_2s_all - int(player2.double_faults)}/{p2_2s_all} ({p2_2s_percent}%)"
    #html_content += generate_item("Second serve", p1_2s_str, p2_2s_str, p1_2s_percent, p2_2s_percent)
    html_content += generate_pecent_item("Second serve", (p1_2s_all - int(player1.double_faults)), p1_2s_all, (p2_2s_all - int(player2.double_faults)), p2_2s_all)
    
    P1_1s_won_str = f"{p1_1s_won}/{p1_1s_all} ({int(100*p1_1s_won/p1_1s_all)}%)"
    P2_1s_won_str = f"{p2_1s_won}/{p2_1s_all} ({int(100*p2_1s_won/p2_1s_all)}%)"
    #html_content += generate_item("First serve points", P1_1s_won_str, P2_1s_won_str, int(100*p1_1s_won/p1_1s_all), int(100*p2_1s_won/p2_1s_all))
    html_content += generate_pecent_item("First serve points", p1_1s_won, p1_1s_all, p2_1s_won, p2_1s_all)

    P1_2s_won_str = f"{p1_2s_won}/{p1_2s_all} ({int(100*p1_2s_won/p1_2s_all)}%)"
    P2_2s_won_str = f"{p2_2s_won}/{p2_2s_all} ({int(100*p2_2s_won/p2_2s_all)}%)"
    #html_content += generate_item("Second serve points", P1_2s_won_str, P2_2s_won_str, int(100*p1_2s_won/p1_2s_all), int(100*p2_2s_won/p2_2s_all))
    html_content += generate_pecent_item("Second serve points", p1_2s_won, p1_2s_all, p2_2s_won, p2_2s_all)

    p1_b_won, p1_b_all = split_to_ints(player1.data['Break Points Won'] if 'Break Points Won' in player1.data else player1.break_points_won)
    p1_bs_won, p1_bs_all = split_to_ints(player1.data['Break Points Saved'] if 'Break Points Saved' in player1.data else player1.break_points_saved)
    p1_b_percent = int(100*p1_b_won/p1_b_all) if p1_b_all != 0 else 0
    p1_bs_percent = int(100*p1_bs_won/p1_bs_all) if p1_bs_all !=0 else 100
    p1_b_str = f"{p1_b_won}/{p1_b_all} ({p1_b_percent}%)"
    p1_bs_str = f"{p1_bs_won}/{p1_bs_all} ({p1_bs_percent}%)"
    p2_b_won, p2_b_all = split_to_ints(player2.data['Break Points Won'] if 'Break Points Won' in player2.data else player2.break_points_won)
    p2_bs_won, p2_bs_all = split_to_ints(player2.data['Break Points Saved'] if 'Break Points Saved' in player2.data else player2.break_points_saved)
    p2_b_percent = int(100*p2_b_won/p2_b_all) if p2_b_all != 0 else 0
    p2_bs_percent = int(100*p2_bs_won/p2_bs_all) if p2_bs_all !=0 else 100
    p2_b_str = f"{p2_b_won}/{p2_b_all} ({p2_b_percent}%)"
    p2_bs_str = f"{p2_bs_won}/{p2_bs_all} ({p2_bs_percent}%)"
    #html_content += generate_item("Break points saved", p1_bs_str, p2_bs_str, p1_bs_percent, p2_bs_percent)
    html_content += generate_pecent_item("Break points saved", p1_b_won, p1_b_all, p2_b_won, p2_b_all)
    
    html_content += html_section_end

    if player1.is_old_format:
        html_content += html_section_start.replace("{section_name}", "Strokes")
        html_content += generate_item("Winners", player1.winners, player2.winners, player1.winners, player2.winners)
        html_content += generate_item("Forced errors", player1.forced_errors, player2.forced_errors, player1.forced_errors, player2.forced_errors, True)
        html_content += generate_item("Unforced errors", player1.unforced_errors, player2.unforced_errors, player1.unforced_errors, player2.unforced_errors, True)
        html_content += html_section_end
    else:
        html_content += html_section_start.replace("{section_name}", "Winners")
        p1_w_all = int(player1.data["Total Winner"])
        p2_w_all = int(player2.data["Total Winner"])
        html_content += generate_item("Total", p1_w_all, p2_w_all, p1_w_all, p2_w_all)
        prefix = "Winner"
        html_content += generate_item_not_empty(player1, player2, "Forehand", prefix)
        html_content += generate_item_not_empty(player1, player2, "Forehand Slice", prefix)
        html_content += generate_item_not_empty(player1, player2, "Forehand Volley", prefix)
        html_content += generate_item_not_empty(player1, player2, "Forehand Return", prefix)
        html_content += generate_item_not_empty(player1, player2, "Forehand Passing Shot", prefix)
        html_content += generate_item_not_empty(player1, player2, "Inside-Out", prefix)
        html_content += generate_item_not_empty(player1, player2, "Inside-In", prefix)
        html_content += generate_item_not_empty(player1, player2, "Backhand", prefix)
        html_content += generate_item_not_empty(player1, player2, "Backhand Slice", prefix)
        html_content += generate_item_not_empty(player1, player2, "Backhand Volley", prefix)
        html_content += generate_item_not_empty(player1, player2, "Backhand Return", prefix)
        html_content += generate_item_not_empty(player1, player2, "Backhand Passing Shot", prefix)
        html_content += generate_item_not_empty(player1, player2, "Approach", prefix)
        html_content += generate_item_not_empty(player1, player2, "Overhead", prefix)
        html_content += generate_item_not_empty(player1, player2, "Drop Shot", prefix)
        html_content += generate_item_not_empty(player1, player2, "Lob", prefix)
        html_content += html_section_end

        html_content += html_section_start.replace("{section_name}", "Forced Errors")
        p1_w_all = int(player1.data["Total Forced Error"])
        p2_w_all = int(player2.data["Total Forced Error"])
        html_content += generate_item("Total", p1_w_all, p2_w_all, p1_w_all, p2_w_all, True)
        prefix = "Forced Error"
        html_content += generate_item_not_empty(player1, player2, "Forehand", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Forehand Slice", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Forehand Volley", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Forehand Return", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Forehand Passing Shot", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Inside-Out", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Inside-In", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Backhand", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Backhand Slice", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Backhand Volley", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Backhand Return", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Backhand Passing Shot", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Approach", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Overhead", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Drop Shot", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Lob", prefix, True)
        html_content += html_section_end

        html_content += html_section_start.replace("{section_name}", "Unforced Errors")
        p1_w_all = int(player1.data["Total Unforced Error"])
        p2_w_all = int(player2.data["Total Unforced Error"])
        html_content += generate_item("Total", p1_w_all, p2_w_all, p1_w_all, p2_w_all, True)
        prefix = "Unforced Error"
        html_content += generate_item_not_empty(player1, player2, "Forehand", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Forehand Slice", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Forehand Volley", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Forehand Return", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Forehand Passing Shot", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Inside-Out", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Inside-In", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Backhand", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Backhand Slice", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Backhand Volley", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Backhand Return", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Backhand Passing Shot", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Approach", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Overhead", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Drop Shot", prefix, True)
        html_content += generate_item_not_empty(player1, player2, "Lob", prefix, True)
        html_content += html_section_end

    html_content += html_section_start.replace("{section_name}", "Return")

    html_content += generate_pecent_item("First serve return points", p1_1s_won_r, p1_1s_all_r, p2_1s_won_r, p2_1s_all_r)
    html_content += generate_pecent_item("Second serve return points", p1_2s_won_r, p1_2s_all_r, p2_2s_won_r, p2_2s_all_r)

    #html_content += generate_item("Break points won", p1_b_str, p2_b_str, p1_b_percent, p2_b_percent)
    html_content += generate_pecent_item("Break points saved", p1_bs_won, p1_bs_all, p2_bs_won, p2_bs_all, False, True)
    html_content += html_section_end

    html_content = html_content + html_all_end
    return html_content