/* BRUNOMEMAPP — the Art engine.
 *
 * Llull's Figure S as a working state machine (quaternary phase).
 * Data is embedded by build_site.py in #engine-data / #figure-s-data so the
 * page works from file:// as well as over http.
 *
 * ATTRIBUTION: this is Llull's Art, not Bruno's. See docs/design/ENGINE.md §1a.
 * HONESTY: the readout reports the state of the FIGURE, never of the user.
 */

(function () {
    const dataEl = document.getElementById('engine-data');
    const figEl = document.getElementById('figure-s-data');
    if (!dataEl || !figEl) return;

    const DATA = JSON.parse(dataEl.textContent);
    const FIG = JSON.parse(figEl.textContent);
    const question = DATA.questions[0];

    const speciesByLetter = Object.fromEntries(FIG.species.map(s => [s.letter, s]));
    const individualsBySpecies = FIG.individuals.reduce((acc, i) => {
        (acc[i.species] = acc[i.species] || []).push(i);
        return acc;
    }, {});

    // --- state -------------------------------------------------------------
    let state = {
        species: null,      // current species letter, or null before starting
        stageIndex: 0,
        log: [],
        finished: false,
    };

    const $ = id => document.getElementById(id);

    function esc(s) {
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
    }

    // --- Figure S table ----------------------------------------------------
    function renderFigure() {
        const powers = ['memory', 'intellect', 'will'];
        const order = ['E', 'I', 'N', 'R'];
        let html = '<table class="figure-s"><thead><tr><th></th>' +
            powers.map(p => `<th>${esc(p)}</th>`).join('') +
            '<th class="fs-label"></th></tr></thead><tbody>';

        for (const letter of order) {
            const sp = speciesByLetter[letter];
            const active = state.species === letter;
            const cells = powers.map(p => {
                const ind = (individualsBySpecies[letter] || []).find(i => i.power === p);
                if (!ind) return '<td></td>';
                return `<td><span class="ind-letter">${esc(ind.letter)}</span>` +
                    `<span class="ind-act">${esc(ind.act)}</span></td>`;
            }).join('');
            const flags = [];
            if (sp.is_goal_state) flags.push('<span class="fs-flag goal">goal</span>');
            if (sp.is_stuck_state) flags.push('<span class="fs-flag stuck">stuck</span>');
            html += `<tr class="fs-row${active ? ' fs-active' : ''}" data-species="${letter}">` +
                `<th class="fs-species" title="${esc(sp.gloss)}">${esc(letter)}</th>` +
                cells +
                `<td class="fs-label">${esc(sp.label)} ${flags.join('')}</td></tr>`;
        }
        html += '</tbody></table>';
        $('figure-s-mount').innerHTML = html;

        const sp = state.species ? speciesByLetter[state.species] : null;
        $('state-readout').innerHTML = sp
            ? `<span class="readout-letter">${esc(sp.letter)}</span>` +
              `<span class="readout-label">${esc(sp.label)}</span>` +
              `<span class="readout-gloss">${esc(sp.gloss)}</span>`
            : '<span class="readout-idle">The figure is not yet placed. Begin the first figure.</span>';
    }

    // --- stage -------------------------------------------------------------
    function renderStage() {
        const stages = question.stages;
        if (state.finished) {
            $('stage-mount').innerHTML =
                `<div class="stage-done">
                    <h3>Demonstratio completa</h3>
                    <p>You worked the contradiction through all four figures and returned S to
                    <strong>E</strong> — holding both horns together, which it could not do at the first figure.</p>
                    <p class="caveat-line">What was demonstrated is a fact about the figure, not about you.
                    Llull's Art claims this ordering changes the operator; this page models the notation and
                    makes no such claim on its behalf.</p>
                    <button id="btn-reset" class="engine-btn">Begin again</button>
                </div>`;
            $('btn-reset').onclick = reset;
            return;
        }

        const st = stages[state.stageIndex];
        const pips = stages.map((s, i) => {
            const cls = i < state.stageIndex ? 'done' : (i === state.stageIndex ? 'current' : '');
            return `<span class="pip ${cls}" title="${esc(s.name_en)}">${esc(s.name)}</span>`;
        }).join('<span class="pip-arrow">→</span>');

        const moves = st.moves.map((m, i) =>
            `<button class="engine-btn move" data-move="${i}">
                ${esc(m.label)}
                ${m.latin ? `<span class="move-latin">${esc(m.latin)}</span>` : ''}
             </button>`).join('');

        $('stage-mount').innerHTML = `
            <div class="stage-pips">${pips}</div>
            <div class="stage">
                <h3>${esc(st.name)} <span class="stage-en">${esc(st.name_en)}</span></h3>
                <p class="stage-situation">${esc(st.situation)}</p>
                <blockquote class="stage-quote">${esc(st.quote)}
                    <cite>Llull, via Bonner — ${esc(st.quote_kind)}</cite></blockquote>
                <div class="stage-moves">${moves}</div>
            </div>`;

        $('stage-mount').querySelectorAll('.move').forEach(btn => {
            btn.onclick = () => applyMove(st, st.moves[+btn.dataset.move]);
        });
    }

    function applyMove(stage, move) {
        state.species = move.to_species;
        state.log.push({ stage: stage.name, move: move.label, to: move.to_species, ok: move.correct });

        const sp = speciesByLetter[move.to_species];
        $('outcome-mount').innerHTML = `
            <div class="outcome ${move.correct ? 'ok' : 'off'}">
                <div class="outcome-head">
                    <span class="outcome-verdict">${move.correct ? 'The figure advances' : 'The figure does not advance'}</span>
                    <span class="outcome-state">S → ${esc(sp.letter)} · ${esc(sp.label)}</span>
                </div>
                <p>${esc(move.result)}</p>
                <p class="outcome-teaches"><strong>Why:</strong> ${esc(move.teaches)}</p>
                ${move.correct
                    ? '<button id="btn-next" class="engine-btn">Continue</button>'
                    : '<button id="btn-retry" class="engine-btn">Try this figure again</button>'}
            </div>`;

        renderFigure();

        if (move.correct) {
            $('btn-next').onclick = () => {
                state.stageIndex += 1;
                if (state.stageIndex >= question.stages.length) state.finished = true;
                $('outcome-mount').innerHTML = '';
                renderStage();
                renderFigure();
            };
        } else {
            $('btn-retry').onclick = () => {
                $('outcome-mount').innerHTML = '';
                renderStage();
            };
        }
    }

    function reset() {
        state = { species: null, stageIndex: 0, log: [], finished: false };
        $('outcome-mount').innerHTML = '';
        renderFigure();
        renderStage();
    }

    reset();
})();
