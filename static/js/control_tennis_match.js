// File: static/js/tennis-match-control.js

(function($) {
    $.fn.tennisMatch = function(options) {
        var defaults = {
            playerApiEndpoint: '/api/players',
            submitEndpoint: '/submit-match',
            formSelector: 'form',
            id: 'match1'
        };
        var settings = $.extend({}, defaults, options);

        return this.each(function() {
            var $container = $(this);
            var $form = $(settings.formSelector);

            // Generate HTML
            var html = `
                <div class="tennis-match" id="tennis-match-${settings.id}">
                    <div class="match-type">
                        <label><input type="radio" name="${settings.id}_match_type" value="singles" checked> Singles</label>
                        <label><input type="radio" name="${settings.id}_match_type" value="doubles"> Doubles</label>
                    </div>
                    <div class="match-details">
                        <table class="pos-table">
                            ${generatePlayerInputs(1, 2)}
                            ${generatePlayerInputs(3, 4, 'doubles')}
                        </table>
                    </div>
                    <div class="set-scores">
                        <table class="pos-table">
                            ${generateScoreInputs(1)}
                            ${generateScoreInputs(2)}
                        </table>
                    </div>
                    <div class="match-outcome">
                        <label><input type="radio" name="${settings.id}_match_outcome" value="team1_won"> Team 1 Won</label>
                        <label><input type="radio" name="${settings.id}_match_outcome" value="team2_won"> Team 2 Won</label>
                    </div>
                </div>
            `;

            $container.html(html);

            // Implement functionality
            $container.find(`input[name="${settings.id}_match_type"]`).change(toggleDoublesVisibility);
            $container.find('.set_score').on('input', handleScoreInput);
            $container.find('.player-input').autocomplete({
                source: settings.playerApiEndpoint,
                minLength: 2,
                select: handlePlayerSelect
            });

            function toggleDoublesVisibility() {
                var isDoubles = $container.find(`input[name="${settings.id}_match_type"]:checked`).val() === 'doubles';
                $container.find('.doubles-row').toggle(isDoubles);
            }

            function handleScoreInput() {
                checkScores();
                calculateMatchOutcome();
            }

            function checkScores() {
                for (let i = 1; i <= 3; i++) {
                    let team1_set = parseInt($container.find(`input[name="${settings.id}_team1_set${i}"]`).val()) || 0;
                    let team2_set = parseInt($container.find(`input[name="${settings.id}_team2_set${i}"]`).val()) || 0;
                    let scoreDifference = Math.abs(team1_set - team2_set);
                    
                    $container.find(`input[name="${settings.id}_team1_set${i}_tb"], input[name="${settings.id}_team2_set${i}_tb"]`).toggle(scoreDifference === 1);
                }
            }

            function calculateMatchOutcome() {
                let team1_sets_won = 0;
                let team2_sets_won = 0;

                for (let i = 1; i <= 3; i++) {
                    let team1_set_score = parseInt($container.find(`input[name="${settings.id}_team1_set${i}"]`).val()) || 0;
                    let team2_set_score = parseInt($container.find(`input[name="${settings.id}_team2_set${i}"]`).val()) || 0;

                    if (team1_set_score > team2_set_score) team1_sets_won++;
                    else if (team2_set_score > team1_set_score) team2_sets_won++;
                }

                if (team1_sets_won > team2_sets_won) {
                    $container.find(`input[name="${settings.id}_match_outcome"][value="team1_won"]`).prop('checked', true);
                } else if (team2_sets_won > team1_sets_won) {
                    $container.find(`input[name="${settings.id}_match_outcome"][value="team2_won"]`).prop('checked', true);
                }
            }

            function handlePlayerSelect(event, ui) {
                var $input = $(event.target);
                var playerNum = $input.attr('id').replace(`${settings.id}_player`, '');
                $container.find(`#${settings.id}_player${playerNum}_id`).val(ui.item.id);
                $container.find(`#${settings.id}_player${playerNum}_wtn`).val(ui.item.wtn);
                $container.find(`#${settings.id}_player${playerNum}_utr`).val(ui.item.utr);
                $container.find(`#${settings.id}_player${playerNum}_usta`).val(ui.item.usta);
            }

            function generatePlayerInputs(start, end, className = '') {
                let html = '';
                for (let i = start; i <= end; i++) {
                    html += `
                        <tr class="${className}">
                            <td>Player ${i}: </td>
                            <td>
                                <input type="text" name="${settings.id}_player${i}_seed" id="${settings.id}_player${i}_seed" placeholder="Seed" style="width: 4ch;">
                                <input type="text" name="${settings.id}_player${i}" id="${settings.id}_player${i}" class="player-input">
                                <input type="hidden" id="${settings.id}_player${i}_id" name="${settings.id}_player${i}_id">
                                <div style="display: flex; margin-top: 5px;">
                                    <input type="text" name="${settings.id}_player${i}_wtn" id="${settings.id}_player${i}_wtn" placeholder="WTN" style="width: 6ch;">
                                    <input type="text" name="${settings.id}_player${i}_utr" id="${settings.id}_player${i}_utr" placeholder="UTR" style="width: 6ch;margin-left: 10px;">
                                    <input type="text" name="${settings.id}_player${i}_usta" id="${settings.id}_player${i}_usta" placeholder="USTA" style="width: 4ch;margin-left: 10px;">
                                </div>
                            </td>
                        </tr>
                    `;
                }
                return html;
            }

            function generateScoreInputs(teamNum) {
                let html = `
                    <tr id="${settings.id}_team${teamNum}_score">
                        <td>Team ${teamNum}</td>
                `;
                for (let i = 1; i <= 3; i++) {
                    html += `
                        <td>
                            <input type="text" name="${settings.id}_team${teamNum}_set${i}" placeholder="S${i}" class="set_score" size="1" maxlength="1" inputmode="decimal">
                            <input type="text" name="${settings.id}_team${teamNum}_set${i}_tb" class="tiebreak_score" style="display: none;" size="2" maxlength="2" inputmode="decimal">
                        </td>
                    `;
                }
                html += '</tr>';
                return html;
            }

            toggleDoublesVisibility();
        });
    };
}(jQuery));