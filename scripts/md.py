"""
md.py — minimal Markdown -> HTML for the design docs.

Deliberately small and dependency-free: headings, paragraphs, bold/italic/code,
links, fenced code, blockquotes, lists, tables, hr. Enough for docs/design/*.md,
which is all it is asked to render.
"""

import html
import re


def _inline(s):
    s = html.escape(s, quote=False)
    s = re.sub(r'`([^`]+)`', r'<code>\1</code>', s)
    s = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', s)
    s = re.sub(r'(?<!\*)\*([^*\n]+)\*(?!\*)', r'<em>\1</em>', s)
    # [text](target) -> link; .md targets are rewritten to local .html pages
    def link(m):
        text, href = m.group(1), m.group(2)
        if href.endswith('.md'):
            href = 'design-' + href[:-3].lower().replace('/', '-') + '.html'
        return f'<a href="{html.escape(href, quote=True)}">{text}</a>'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', link, s)


def _table(rows):
    if len(rows) < 2:
        return ''
    def cells(r):
        return [c.strip() for c in r.strip().strip('|').split('|')]
    head = cells(rows[0])
    body = [cells(r) for r in rows[2:]]
    th = ''.join(f'<th>{_inline(c)}</th>' for c in head)
    tr = ''.join('<tr>' + ''.join(f'<td>{_inline(c)}</td>' for c in r) + '</tr>'
                 for r in body)
    return (f'<div class="table-scroll"><table class="doc-table">'
            f'<thead><tr>{th}</tr></thead><tbody>{tr}</tbody></table></div>')


def render(text):
    out, i = [], 0
    lines = text.split('\n')
    n = len(lines)

    while i < n:
        line = lines[i]
        stripped = line.strip()

        if not stripped:
            i += 1
            continue

        # fenced code
        if stripped.startswith('```'):
            i += 1
            buf = []
            while i < n and not lines[i].strip().startswith('```'):
                buf.append(html.escape(lines[i], quote=False))
                i += 1
            i += 1
            out.append('<pre class="doc-pre"><code>' + '\n'.join(buf) + '</code></pre>')
            continue

        # horizontal rule
        if re.fullmatch(r'-{3,}|\*{3,}', stripped):
            out.append('<hr>')
            i += 1
            continue

        # heading
        m = re.match(r'^(#{1,6})\s+(.*)$', stripped)
        if m:
            lvl = len(m.group(1))
            out.append(f'<h{lvl} class="doc-h{lvl}">{_inline(m.group(2))}</h{lvl}>')
            i += 1
            continue

        # table
        if stripped.startswith('|'):
            buf = []
            while i < n and lines[i].strip().startswith('|'):
                buf.append(lines[i])
                i += 1
            out.append(_table(buf))
            continue

        # blockquote
        if stripped.startswith('>'):
            buf = []
            while i < n and lines[i].strip().startswith('>'):
                buf.append(lines[i].strip().lstrip('>').strip())
                i += 1
            out.append('<blockquote class="doc-quote">' +
                       _inline(' '.join(buf)) + '</blockquote>')
            continue

        # list (ordered or unordered, flat)
        if re.match(r'^[-*]\s+|^\d+\.\s+', stripped):
            ordered = bool(re.match(r'^\d+\.\s+', stripped))
            buf = []
            while i < n:
                s = lines[i].strip()
                m2 = re.match(r'^(?:[-*]|\d+\.)\s+(.*)$', s)
                if m2:
                    buf.append(m2.group(1))
                    i += 1
                elif s and not re.match(r'^(#{1,6}\s|\||>|```)', s) and buf:
                    buf[-1] += ' ' + s          # continuation line
                    i += 1
                else:
                    break
            tag = 'ol' if ordered else 'ul'
            out.append(f'<{tag} class="doc-list">' +
                       ''.join(f'<li>{_inline(b)}</li>' for b in buf) + f'</{tag}>')
            continue

        # paragraph
        buf = []
        while i < n and lines[i].strip() and not re.match(
                r'^(#{1,6}\s|\||>|```|-{3,}|[-*]\s|\d+\.\s)', lines[i].strip()):
            buf.append(lines[i].strip())
            i += 1
        if buf:
            out.append('<p>' + _inline(' '.join(buf)) + '</p>')

    return '\n'.join(out)
