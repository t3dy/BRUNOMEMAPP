/* BRUNOMEMAPP — interactive diagram gallery.
 *
 * Llull's and Bruno's figures drawn as SVG from the harvested data rather than
 * reproduced as scans. That is what makes them manipulable: a scan of a wheel
 * cannot be turned, and a scan of Figure A cannot tell you which compartment
 * you just formed.
 *
 * Every figure states its own attestation. Where a structure could not be
 * recovered reliably it is NOT approximated -- see data/diagrams.json
 * not_reconstructed.
 */

(function () {
    const get = id => document.getElementById(id);
    const need = ['diagrams-data', 'figure-s-data', 'atria-data', 'alphabet-data'].map(get);
    if (need.some(n => !n)) return;
    const [DIA, FIG, ATRIA, ALPHA] = need.map(n => JSON.parse(n.textContent));

    const SVGNS = 'http://www.w3.org/2000/svg';
    const el = (t, a = {}) => {
        const n = document.createElementNS(SVGNS, t);
        for (const k in a) n.setAttribute(k, a[k]);
        return n;
    };
    const svg = (w, h) => el('svg', {
        viewBox: `0 0 ${w} ${h}`, class: 'fig-svg',
        preserveAspectRatio: 'xMidYMid meet'
    });
    const esc = s => String(s == null ? '' : s)
        .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

    // polar helper: index i of n around a circle, 12 o'clock first
    const pt = (cx, cy, r, i, n) => {
        const a = (i / n) * Math.PI * 2 - Math.PI / 2;
        return [cx + r * Math.cos(a), cy + r * Math.sin(a)];
    };

    function say(slug, html) {
        const o = get('out-' + slug);
        if (o) o.innerHTML = html;
    }

    // ---------------------------------------------------------------- Figure A
    function figureA(fig, mount) {
        const W = 620, C = W / 2, R = 232, terms = fig.terms, n = terms.length;
        const s = svg(W, W);
        const chords = el('g', { class: 'fig-chords' });
        for (let i = 0; i < n; i++) {
            for (let j = i + 1; j < n; j++) {
                const [x1, y1] = pt(C, C, R, i, n), [x2, y2] = pt(C, C, R, j, n);
                const l = el('line', { x1, y1, x2, y2, class: 'chord', 'data-i': i, 'data-j': j });
                chords.appendChild(l);
            }
        }
        s.appendChild(chords);
        s.appendChild(el('circle', { cx: C, cy: C, r: R, class: 'fig-ring' }));
        s.appendChild(el('circle', { cx: C, cy: C, r: 30, class: 'fig-hub' }));
        const a = el('text', { x: C, y: C + 8, class: 'fig-hub-label' });
        a.textContent = fig.centre;
        s.appendChild(a);

        let sel = [];
        terms.forEach((term, i) => {
            const [x, y] = pt(C, C, R, i, n);
            const g = el('g', { class: 'vertex', 'data-i': i });
            g.appendChild(el('circle', { cx: x, cy: y, r: 15 }));
            const lbl = el('text', { x, y: y + 4 });
            lbl.textContent = String.fromCharCode(66 + i); // B, C, D…
            g.appendChild(lbl);
            const [tx, ty] = pt(C, C, R + 40, i, n);
            const t2 = el('text', {
                x: tx, y: ty + 4, class: 'vertex-name',
                'text-anchor': tx < C - 8 ? 'end' : (tx > C + 8 ? 'start' : 'middle')
            });
            t2.textContent = term;
            g.appendChild(t2);
            g.addEventListener('click', () => {
                const k = sel.indexOf(i);
                if (k >= 0) sel.splice(k, 1); else sel.push(i);
                if (sel.length > 2) sel.shift();
                s.querySelectorAll('.vertex').forEach(v =>
                    v.classList.toggle('on', sel.includes(+v.dataset.i)));
                s.querySelectorAll('.chord').forEach(c => {
                    const hit = sel.length === 2 &&
                        sel.includes(+c.dataset.i) && sel.includes(+c.dataset.j);
                    c.classList.toggle('lit', hit);
                    c.classList.toggle('dim', sel.length === 2 && !hit);
                });
                if (sel.length === 2) {
                    const [p, q] = sel.map(i2 => terms[i2]);
                    const ls = sel.map(i2 => String.fromCharCode(66 + i2)).join(' ');
                    say(fig.slug, `<strong>Compartment ${esc(ls)}</strong> — ` +
                        `<em>${esc(p)}</em> with <em>${esc(q)}</em>. Llull builds arguments ` +
                        `out of exactly these binary units; because every dignity is ` +
                        `concordant with every other, all 120 of them are available.`);
                } else {
                    say(fig.slug, sel.length
                        ? `<em>${esc(terms[sel[0]])}</em> — choose a second dignity.`
                        : '');
                }
            });
            s.appendChild(g);
        });
        mount.appendChild(s);
        say(fig.slug, `<span class="muted">${n} dignities · ${n * (n - 1) / 2} compartments. Click two.</span>`);
    }

    // ---------------------------------------------------------------- Figure V
    function figureV(fig, mount) {
        const W = 620, C = W / 2, R = 200;
        const virt = fig.pairs.map(p => p.virtue), vice = fig.pairs.map(p => p.vice);
        const s = svg(W, W);
        let show = 'both';

        function draw() {
            s.innerHTML = '';
            [['virtue', virt, 180, 'v-blue'], ['vice', vice, 118, 'v-red']].forEach(
                ([kind, list, r, cls]) => {
                    if (show !== 'both' && show !== kind) return;
                    const n = list.length;
                    const g = el('g', { class: 'fig-chords ' + cls });
                    for (let i = 0; i < n; i++)
                        for (let j = i + 1; j < n; j++) {
                            const [x1, y1] = pt(C, C, r, i, n), [x2, y2] = pt(C, C, r, j, n);
                            g.appendChild(el('line', { x1, y1, x2, y2, class: 'chord ' + cls }));
                        }
                    s.appendChild(g);
                    list.forEach((term, i) => {
                        const [x, y] = pt(C, C, r, i, n);
                        const vg = el('g', { class: 'vertex ' + cls });
                        vg.appendChild(el('circle', { cx: x, cy: y, r: 11 }));
                        const [tx, ty] = pt(C, C, r + (kind === 'virtue' ? 42 : -34), i, n);
                        const t = el('text', {
                            x: tx, y: ty + 4, class: 'vertex-name ' + cls,
                            'text-anchor': 'middle'
                        });
                        t.textContent = term;
                        vg.appendChild(t);
                        vg.addEventListener('click', () => say(fig.slug,
                            `<strong>${esc(term)}</strong> — a ${kind}. It connects to every ` +
                            `other ${kind} and to no ${kind === 'virtue' ? 'vice' : 'virtue'}. ` +
                            `That separation is the figure's entire claim.`));
                        s.appendChild(vg);
                    });
                });
        }
        draw();
        const bar = document.createElement('div');
        bar.className = 'fig-controls';
        [['both', 'Both'], ['virtue', 'Virtues only'], ['vice', 'Vices only']].forEach(([k, lbl]) => {
            const b = document.createElement('button');
            b.className = 'engine-btn small' + (k === 'both' ? ' on' : '');
            b.textContent = lbl;
            b.onclick = () => {
                show = k; draw();
                bar.querySelectorAll('button').forEach(x => x.classList.remove('on'));
                b.classList.add('on');
            };
            bar.appendChild(b);
        });
        mount.appendChild(bar);
        mount.appendChild(s);
    }

    // ---------------------------------------------------------------- Figure X
    function figureX(fig, mount) {
        const W = 620, C = W / 2, R = 210;
        const flat = [];
        fig.pairs.forEach(p => { flat.push(p.a); flat.push(p.b); });
        const n = flat.length, s = svg(W, W);
        s.appendChild(el('circle', { cx: C, cy: C, r: R, class: 'fig-ring' }));
        fig.pairs.forEach((p, k) => {
            const i = k, j = k + fig.pairs.length;
            const [x1, y1] = pt(C, C, R, i, n), [x2, y2] = pt(C, C, R, j, n);
            const l = el('line', { x1, y1, x2, y2, class: 'chord opp', 'data-k': k });
            s.appendChild(l);
        });
        flat.forEach((term, i) => {
            const [x, y] = pt(C, C, R, i, n);
            const k = i % fig.pairs.length;
            const g = el('g', { class: 'vertex', 'data-k': k });
            g.appendChild(el('circle', { cx: x, cy: y, r: 13 }));
            const [tx, ty] = pt(C, C, R + 44, i, n);
            const t = el('text', {
                x: tx, y: ty + 4, class: 'vertex-name',
                'text-anchor': tx < C - 8 ? 'end' : (tx > C + 8 ? 'start' : 'middle')
            });
            t.textContent = term;
            g.appendChild(t);
            g.addEventListener('click', () => {
                s.querySelectorAll('.opp').forEach(o =>
                    o.classList.toggle('lit', +o.dataset.k === k));
                s.querySelectorAll('.vertex').forEach(v =>
                    v.classList.toggle('on', +v.dataset.k === k));
                const p = fig.pairs[k];
                const isFirst = k === 0;
                say(fig.slug, `<strong>${esc(p.a)}</strong> against <strong>${esc(p.b)}</strong>. ` +
                    (isFirst
                        ? `This is the contradiction worked through in <a href="engine.html">the Art Engine</a> — ` +
                          `affirmation, denial, doubt, resolution.`
                        : `A contrariety the Art exists to resolve, by finding the compartment at ` +
                          `which both can be affirmed together.`));
            });
            s.appendChild(g);
        });
        mount.appendChild(s);
        if (fig.incomplete) {
            const w = document.createElement('p');
            w.className = 'caveat-line';
            w.textContent = fig.incomplete_note;
            mount.appendChild(w);
        }
    }

    // ---------------------------------------------------------------- Figure S
    function figureS(fig, mount) {
        const W = 600, C = W / 2, R = 205, s = svg(W, W);
        const order = ['E', 'I', 'N', 'R'];
        const byLetter = Object.fromEntries(FIG.species.map(x => [x.letter, x]));
        const indBy = FIG.individuals.reduce((a, i) => {
            (a[i.species] = a[i.species] || []).push(i); return a;
        }, {});
        s.appendChild(el('circle', { cx: C, cy: C, r: R, class: 'fig-ring' }));
        order.forEach((L, k) => {
            const rot = (k * 90) / 4;
            const g = el('g', {
                class: 'sq sq-' + L, 'data-L': L,
                transform: `rotate(${rot} ${C} ${C})`
            });
            const p = [0, 1, 2, 3].map(i => pt(C, C, R, i, 4).join(',')).join(' ');
            g.appendChild(el('polygon', { points: p }));
            const [lx, ly] = pt(C, C, R - 34, k, 4);
            const t = el('text', { x: lx, y: ly + 9, class: 'sq-label' });
            t.textContent = L;
            g.appendChild(t);
            g.addEventListener('click', () => {
                s.querySelectorAll('.sq').forEach(q => q.classList.toggle('on', q.dataset.L === L));
                const sp = byLetter[L];
                const trip = (indBy[L] || []).map(i =>
                    `<span class="op"><strong>${esc(i.letter)}</strong> ${esc(i.power)} ${esc(i.act)}</span>`
                ).join(' ');
                const flag = sp.is_goal_state ? '<span class="fs-flag goal">goal</span>'
                    : sp.is_stuck_state ? '<span class="fs-flag stuck">stuck</span>' : '';
                say(fig.slug, `<strong>${esc(L)} — ${esc(sp.label)}</strong> ${flag}<br>` +
                    `<span class="muted">${esc(sp.gloss)}</span><div class="op-row">${trip}</div>` +
                    `<p class="muted">${esc(sp.note || '')}</p>`);
            });
            s.appendChild(g);
        });
        mount.appendChild(s);
        say(fig.slug, '<span class="muted">Four inscribed squares — one per species of the soul. Click one.</span>');
    }

    // ----------------------------------------------------------------- Atrium
    function atrium(fig, mount) {
        const W = 620, C = W / 2, R = 215;
        const list = ATRIA.transcribed;
        let cur = 0;
        const wrap = document.createElement('div');

        const sel = document.createElement('select');
        sel.className = 'fig-select';
        list.forEach((a, i) => {
            const o = document.createElement('option');
            o.value = i;
            o.textContent = `${a.number}. ${a.name}` +
                (a.position_mapping_attestation === 'ATTESTED' ? '  (mapping attested)' : '');
            sel.appendChild(o);
        });
        wrap.appendChild(sel);
        const host = document.createElement('div');
        wrap.appendChild(host);

        function draw() {
            host.innerHTML = '';
            const a = list[cur], s = svg(W, W);
            // quadrangle
            const corners = [0, 1, 2, 3].map(i => pt(C, C, R, i, 4));
            s.appendChild(el('polygon', {
                points: corners.map(p => p.join(',')).join(' '), class: 'atr-frame'
            }));
            // 8 points: 4 corners + 4 mid-sides, each with L/R collateral = 24
            const names = ['E corner', 'S corner', 'W corner', 'N corner',
                           'S side', 'W side', 'N side', 'E side'];
            let idx = 0;
            for (let p8 = 0; p8 < 8; p8++) {
                const base = p8 < 4 ? pt(C, C, R, p8, 4) : pt(C, C, R * 0.78, (p8 - 4) + 0.5, 4);
                for (let c = 0; c < 3; c++) {
                    const off = (c - 1) * 30;
                    const ang = (p8 / 8) * Math.PI * 2 - Math.PI / 2;
                    const x = base[0] + Math.cos(ang + Math.PI / 2) * off;
                    const y = base[1] + Math.sin(ang + Math.PI / 2) * off;
                    // Capture the index by value: the click handler fires long
                    // after the loop has finished, so closing over `idx` itself
                    // would report the final count for every position.
                    const at = idx;
                    const label = a.positions[at] || '—';
                    const g = el('g', { class: 'atr-pos' });
                    g.appendChild(el('circle', { cx: x, cy: y, r: 13 }));
                    const t = el('text', { x, y: y + 3.5 });
                    t.textContent = String(at + 1);
                    g.appendChild(t);
                    const role = ['left', '', 'right'][c];
                    g.addEventListener('click', () => {
                        s.querySelectorAll('.atr-pos').forEach(q => q.classList.remove('on'));
                        g.classList.add('on');
                        say(fig.slug,
                            `<strong>${esc(label)}</strong><br><span class="muted">position ` +
                            `${at + 1} of 24 — ${esc(names[p8])}${role ? ', ' + role : ''}, in the ` +
                            `atrium of ${esc(a.name)}.</span>` +
                            (a.position_mapping_attestation === 'ATTESTED'
                                ? '<p class="muted">Position mapping attested in prose (ch. 6).</p>'
                                : '<p class="muted">Inventory attested; this <em>position</em> is reconstructed from plate order and may not be geometrically faithful.</p>'));
                    });
                    s.appendChild(g);
                    idx++;
                }
            }
            const hub = el('circle', { cx: C, cy: C, r: 34, class: 'fig-hub' });
            s.appendChild(hub);
            const ht = el('text', { x: C, y: C + 5, class: 'fig-hub-label small' });
            ht.textContent = a.centre;
            s.appendChild(ht);
            host.appendChild(s);
            say(fig.slug, `<span class="muted">Atrium ${a.number} of 24 — ` +
                `${a.position_count} positions. Centre: the earth and the eye. Click a position.</span>`);
        }
        sel.onchange = () => { cur = +sel.value; draw(); };
        draw();
        mount.appendChild(wrap);
    }

    // ------------------------------------------------------------------ Wheel
    function wheel(fig, mount) {
        const W = 620, C = W / 2, s = svg(W, W);
        const keys = ALPHA.simple_keys;
        const n = keys.length;
        let rot = 0;

        const outer = el('g'), inner = el('g', { class: 'wheel-inner' });
        s.appendChild(el('circle', { cx: C, cy: C, r: 240, class: 'fig-ring' }));
        s.appendChild(el('circle', { cx: C, cy: C, r: 160, class: 'fig-ring' }));
        s.appendChild(outer); s.appendChild(inner);

        keys.forEach((k, i) => {
            const [x, y] = pt(C, C, 240, i, n);
            const g = el('g', { class: 'vertex' });
            g.appendChild(el('circle', { cx: x, cy: y, r: 16 }));
            const t = el('text', { x, y: y + 5 });
            t.textContent = k.key;
            g.appendChild(t);
            outer.appendChild(g);
        });

        function drawInner() {
            inner.innerHTML = '';
            keys.forEach((k, i) => {
                const ops = k.entries.filter(e => e.kind === 'OPERATOR' && !e.ocr_suspect);
                const op = ops[((rot % ops.length) + ops.length) % ops.length];
                const [x, y] = pt(C, C, 160, i, n);
                const g = el('g', { class: 'vertex small' });
                g.appendChild(el('circle', { cx: x, cy: y, r: 13 }));
                const t = el('text', { x, y: y + 4, class: 'wheel-op' });
                t.textContent = op ? op.form.slice(0, 4) : '—';
                g.appendChild(t);
                g.addEventListener('click', () => say(fig.slug,
                    `<strong>${esc(k.key)}</strong> → <em>${esc(op ? op.form : '—')}</em>` +
                    (op && op.gloss ? ` — ${esc(op.gloss)}` : '') +
                    `<p class="muted">One of ${ops.length} operators this key commands. ` +
                    `Turn the inner ring to bring a different one into alignment.</p>`));
                inner.appendChild(g);
            });
        }
        drawInner();

        const bar = document.createElement('div');
        bar.className = 'fig-controls';
        [['◀ turn', -1], ['turn ▶', 1]].forEach(([lbl, d]) => {
            const b = document.createElement('button');
            b.className = 'engine-btn small';
            b.textContent = lbl;
            b.onclick = () => {
                rot += d;
                inner.style.transition = 'transform .25s';
                inner.style.transform = `rotate(${rot * (360 / n) * 0.35}deg)`;
                inner.style.transformOrigin = '50% 50%';
                drawInner();
            };
            bar.appendChild(b);
        });
        mount.appendChild(bar);
        mount.appendChild(s);
        say(fig.slug, '<span class="muted">Outer ring: letter-keys. Inner ring: the operator currently aligned. Turn it.</span>');
    }

    const RENDER = {
        'complete_graph': figureA, 'disconnected_graph': figureV,
        'opposition_circle': figureX, 'inscribed_squares': figureS,
        'atrium': atrium, 'concentric_wheel': wheel,
    };

    DIA.figures.forEach(fig => {
        const mount = get('fig-' + fig.slug);
        if (mount && RENDER[fig.kind]) {
            try { RENDER[fig.kind](fig, mount); }
            catch (e) { mount.innerHTML = '<p class="caveat-line">This figure failed to draw.</p>'; }
        }
    });
})();
