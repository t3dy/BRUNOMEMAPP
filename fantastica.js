/* BRUNOMEMAPP — logica fantastica.
 *
 * Llull's Figure S run on IMAGES rather than letter-variables, which is what
 * Bruno's version of the Art requires (Mertens; Rossi, "La logica fantastica
 * di Giordano Bruno"). Compose an image from three attested systems:
 *
 *   memory    <- the image alphabet   (an operator to hold it by)
 *   intellect <- the atria            (an apt address)
 *   will      <- the planetary courts (an affective register)
 *
 * The resulting triple determines which species of Figure S you land in.
 *
 * STATUS: the COMBINATION is a SCHOLARLY_RECONSTRUCTION. Every component is
 * attested; Bruno leaves no worked example of wiring them together this way.
 * See data/fantastica.json _provenance.
 */

(function () {
    const el = id => document.getElementById(id);
    const nodes = ['fantastica-data', 'figure-s-data', 'alphabet-data', 'atria-data', 'courts-data']
        .map(el);
    if (nodes.some(n => !n)) return;

    const [FA, FIG, ALPHA, ATRIA, COURTS] = nodes.map(n => JSON.parse(n.textContent));
    const Q = FA.question;

    const speciesByLetter = Object.fromEntries(FIG.species.map(s => [s.letter, s]));
    const valenceByCourt = Object.fromEntries(FA.court_valences.map(c => [c.court, c]));

    function esc(s) {
        return String(s == null ? '' : s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;')
            .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // Operators available for a letter key (simple keys only; clusters share
    // the same shape but are not needed by the seeded question).
    function operatorsFor(key) {
        const row = ALPHA.simple_keys.find(r => r.key === key.toUpperCase());
        if (!row) return [];
        return row.entries.filter(e => e.kind === 'OPERATOR' && !e.ocr_suspect);
    }

    const atriumNames = ATRIA.transcribed.map(a => a.name);
    const courtNames = COURTS.courts.map(c => c.planet);

    let state = { stageIndex: 0, pick: {}, species: null, finished: false };

    // ---- resolution ------------------------------------------------------
    function resolve(stage, pick) {
        const court = valenceByCourt[pick.court] || {};
        const clarifies = court.valence === 'clarify';
        const memory = !!pick.operator;
        const intellect = stage.apt_atria.includes(pick.atrium) || clarifies;
        let will = court.valence;
        if (clarifies) will = null;              // Mercury/Sun do not move the will

        if (!memory) {
            return { species: 'N', why: 'No operator: the memory has nothing to hold the image by. K, forgetting.' };
        }
        if (!intellect) {
            return { species: 'N', why: `The ${esc(pick.atrium)} is not an apt address for this term, and the court supplies no clarity of its own. L, not knowing.` };
        }
        if (will === 'mutable') {
            return { species: 'R', why: "Luna's retinue is split by phase, so the will cannot settle. Held and understood, but all possibilities stand open at once." };
        }
        if (will === null) {
            return { species: 'N', why: `${esc(pick.court)} sharpens the intellect but does not incline the will. Without love or hatred the soul only supposes.` };
        }
        return {
            species: will === 'love' ? 'E' : 'I',
            why: `${esc(pick.court)} — ${esc(court.register)} — inclines the will to ${will === 'love' ? 'love (D)' : 'hatred (H)'}. With the operator holding it and the ${esc(pick.atrium)} placing it, all three powers act.`
        };
    }

    // ---- render ----------------------------------------------------------
    function renderFigure() {
        const order = ['E', 'I', 'N', 'R'];
        let html = '<table class="figure-s"><tbody>';
        for (const L of order) {
            const sp = speciesByLetter[L];
            const active = state.species === L;
            const flags = (sp.is_goal_state ? '<span class="fs-flag goal">goal</span>' : '') +
                          (sp.is_stuck_state ? '<span class="fs-flag stuck">stuck</span>' : '');
            html += `<tr class="fs-row${active ? ' fs-active' : ''}">` +
                `<th class="fs-species">${esc(L)}</th>` +
                `<td class="fs-label">${esc(sp.label)} ${flags}</td>` +
                `<td class="ind-act">${esc(sp.gloss)}</td></tr>`;
        }
        el('fantastica-figure').innerHTML = html + '</tbody></table>';
    }

    function pickerRow(label, source, key, options, render) {
        const opts = options.map(o => {
            const v = typeof o === 'string' ? o : o.form;
            const sel = state.pick[key] === v ? ' selected' : '';
            return `<button class="chip-pick${sel}" data-key="${key}" data-val="${esc(v)}">${render(o)}</button>`;
        }).join('');
        return `<div class="picker">
            <div class="picker-head"><span class="picker-power">${esc(label)}</span>
                <span class="picker-source">${esc(source)}</span></div>
            <div class="picker-opts">${opts}</div></div>`;
    }

    function renderStage() {
        if (state.finished) {
            el('fantastica-stage').innerHTML = `
                <div class="stage-done">
                    <h3>Demonstratio per imagines</h3>
                    <p>You ran the same dialectic Llull ran with letters, using images composed from
                    Bruno's own alphabet, atria and courts.</p>
                    <p class="caveat-line"><strong>Reconstruction.</strong> Every component here is
                    attested. The wiring — operator to memory, atrium to intellect, court to will —
                    is this project's construction from the <em>similitudo</em> principle. Bruno leaves
                    no worked example of composing a dialectic this way.</p>
                    <button id="fa-reset" class="engine-btn">Begin again</button>
                </div>`;
            el('fa-reset').onclick = reset;
            return;
        }

        const st = Q.stages[state.stageIndex];
        const pips = Q.stages.map((s, i) =>
            `<span class="pip ${i < state.stageIndex ? 'done' : (i === state.stageIndex ? 'current' : '')}">${esc(s.name)}</span>`
        ).join('<span class="pip-arrow">→</span>');

        const ops = operatorsFor(st.letter_key).slice(0, 5);

        el('fantastica-stage').innerHTML = `
            <div class="stage-pips">${pips}</div>
            <div class="stage">
                <h3>${esc(st.name)} <span class="stage-en">${esc(st.name_en)}</span></h3>
                <p class="stage-situation"><strong>${esc(st.term)}</strong> — ${esc(st.brief)}</p>
                <p class="stage-target">Target species: <strong>${esc(st.target_species)}</strong>
                   — ${esc(speciesByLetter[st.target_species].label)}</p>

                ${pickerRow('memory', `alphabet · key ${st.letter_key}`, 'operator', ops,
                    o => `${esc(o.form)}${o.gloss ? `<span class="chip-gloss">${esc(o.gloss)}</span>` : ''}`)}

                ${pickerRow('intellect', 'atria · 24 addresses', 'atrium', atriumNames,
                    a => esc(a))}

                ${pickerRow('will', 'planetary courts', 'court', courtNames,
                    c => {
                        const v = valenceByCourt[c];
                        return `${esc(c)}${v ? `<span class="chip-gloss">${esc(v.register)}</span>` : ''}`;
                    })}

                <button id="fa-compose" class="engine-btn compose" ${
                    (state.pick.operator && state.pick.atrium && state.pick.court) ? '' : 'disabled'
                }>Compose the image</button>
                <p class="apt-hint">Apt addresses for this figure: <em>${esc(st.apt_atria.join(', '))}</em>
                   — ${esc(st.apt_reason)}</p>
            </div>`;

        el('fantastica-stage').querySelectorAll('.chip-pick').forEach(b => {
            b.onclick = () => { state.pick[b.dataset.key] = b.dataset.val; renderStage(); };
        });
        const btn = el('fa-compose');
        if (btn && !btn.disabled) btn.onclick = () => compose(st);
    }

    function compose(stage) {
        const r = resolve(stage, state.pick);
        state.species = r.species;
        const hit = r.species === stage.target_species;
        const sp = speciesByLetter[r.species];

        el('fantastica-outcome').innerHTML = `
            <div class="outcome ${hit ? 'ok' : 'off'}">
                <div class="outcome-head">
                    <span class="outcome-verdict">${hit ? 'The figure advances' : 'Not this figure'}</span>
                    <span class="outcome-state">S → ${esc(sp.letter)} · ${esc(sp.label)}</span>
                </div>
                <p class="composed">
                    <em>${esc(state.pick.operator)}</em>, placed in the atrium of
                    <em>${esc(state.pick.atrium)}</em>, drawn from the court of
                    <em>${esc(state.pick.court)}</em>.
                </p>
                <p>${r.why}</p>
                ${hit
                    ? '<button id="fa-next" class="engine-btn">Continue</button>'
                    : `<p class="outcome-teaches">You reached <strong>${esc(sp.letter)}</strong>;
                       this figure wants <strong>${esc(stage.target_species)}</strong>. Recompose.</p>
                       <button id="fa-retry" class="engine-btn">Try again</button>`}
            </div>`;

        renderFigure();

        if (hit) {
            el('fa-next').onclick = () => {
                state.stageIndex += 1;
                state.pick = {};
                if (state.stageIndex >= Q.stages.length) state.finished = true;
                el('fantastica-outcome').innerHTML = '';
                renderStage(); renderFigure();
            };
        } else {
            el('fa-retry').onclick = () => { el('fantastica-outcome').innerHTML = ''; renderStage(); };
        }
    }

    function reset() {
        state = { stageIndex: 0, pick: {}, species: null, finished: false };
        el('fantastica-outcome').innerHTML = '';
        renderFigure(); renderStage();
    }

    reset();
})();
