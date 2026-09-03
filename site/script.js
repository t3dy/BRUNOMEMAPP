/* BRUNOMEMAPP — search. Cribbed verbatim from WitcherPortal/script.js (generic pattern).
 * On the search page, fetches search-index.json and filters live.
 */

(function () {
    const input = document.getElementById('search-input');
    const results = document.getElementById('search-results');
    if (!input || !results) return;

    let index = [];
    let loaded = false;

    function load() {
        if (loaded) return Promise.resolve();
        return fetch('search-index.json')
            .then(r => r.json())
            .then(data => { index = data; loaded = true; });
    }

    function escapeHtml(s) {
        if (s == null) return '';
        return String(s)
            .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;').replace(/'/g, '&#39;');
    }

    function render(items) {
        if (!items.length) {
            results.innerHTML = '<p class="section-intro">No matches.</p>';
            return;
        }
        results.innerHTML = items.slice(0, 60).map(item => `
            <a class="search-result" href="${escapeHtml(item.href)}">
                <div class="search-result-type">${escapeHtml(item.type)}</div>
                <h4>${escapeHtml(item.title)}</h4>
                ${item.summary ? `<p>${escapeHtml(item.summary)}</p>` : ''}
            </a>`).join('');
    }

    function score(item, q) {
        const ql = q.toLowerCase();
        const t = (item.title || '').toLowerCase();
        const s = (item.summary || '').toLowerCase();
        if (t === ql) return 100;
        if (t.startsWith(ql)) return 80;
        if (t.includes(ql)) return 60;
        if (s.includes(ql)) return 30;
        return 0;
    }

    function filter() {
        const q = input.value.trim();
        if (!q) { results.innerHTML = '<p class="section-intro">Type to search across works, images, scholars, dictionary, disputes, timeline, essays, and app-mode ideas.</p>'; return; }
        const matches = index
            .map(item => ({ item, s: score(item, q) }))
            .filter(x => x.s > 0)
            .sort((a, b) => b.s - a.s)
            .map(x => x.item);
        render(matches);
    }

    input.addEventListener('input', () => { load().then(filter); });
    load().then(() => { filter(); });
})();
