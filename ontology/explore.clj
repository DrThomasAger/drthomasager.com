(ns explore
  "The explore page of drthomasager.com, worn in the Blog Template.
  bb ontology/explore.clj

  The page links the Blog Template's blog.css and blog.js, copied from
  C:/Users/hanjo/Claude/Projects/Blog Template/ into site/assets/blog/, the
  Medium-like reading page with its rose madder palette that Hanjo made the
  blog aesthetic. It carries the interface alone, the two roots, a search, a
  sort, the places and the tags, and the posts as a reading list. It is written
  to site/explore.html with index.json and ontology.json beside it.

  Every view is a URL, e.g. explore.html#place=ai/agents&evidence=measured&q=memory,
  so a reader can share a view and an MCP can name one."
  (:require [cheshire.core :as json]
            [babashka.fs :as fs]
            [clojure.string :as str]))

(def dir (str (fs/parent (fs/absolutize *file*))))
(def root (str (fs/parent dir)))
(load-file (str dir "/check.clj"))

(def template "C:/Users/hanjo/Claude/Projects/Blog Template")

(def head "<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>Explore, Dr Thomas Ager</title>
<meta name=\"description\" content=\"Every post of Dr Thomas Ager by place and tag, under AI or Buddhism, filtered by format, model, tool, method, project, practice, level and evidence.\">
<link rel=\"alternate\" type=\"application/json\" href=\"index.json\" title=\"Every post with its place and tags\">
<link rel=\"alternate\" type=\"application/json\" href=\"ontology.json\" title=\"The ontology\">
<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
<link href=\"https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,0..100;1,9..144,300..700,0..100&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600&family=Inter:wght@400;500;600;700&display=swap\" rel=\"stylesheet\">
<link rel=\"stylesheet\" href=\"assets/blog/blog.css\">
<style>
/* the explore interface, drawn with the Blog Template's own tokens */
.roots{display:flex;gap:var(--sp3);border-bottom:1px solid var(--rule);margin:0 0 var(--sp3)}
.roots button{font:500 var(--s0)/1 var(--sans);color:var(--ink-2);background:none;border:0;border-bottom:2px solid transparent;padding:0 0 var(--sp1);margin-bottom:-1px;cursor:pointer}
.roots button.on{color:var(--ink);border-bottom-color:var(--ink)}
.bar{display:flex;flex-wrap:wrap;gap:var(--sp1);align-items:center;margin:0 0 var(--sp2)}
.bar input,.bar select{font:400 var(--s0)/1.3 var(--sans);color:var(--ink);background:var(--surface);border:0;border-radius:99px;padding:10px 16px}
.bar input{flex:1;min-width:12rem}
.bar .count{font:500 var(--s-1)/1 var(--sans);letter-spacing:.08em;text-transform:uppercase;color:var(--ink-2)}
.tree a{display:flex;justify-content:space-between;gap:var(--sp1);font:400 var(--s0)/1.3 var(--sans);text-decoration:none;padding:6px 10px;border-radius:8px}
.tree a.on{background:var(--accent-soft);color:var(--accent)}
.n{font-variant-numeric:tabular-nums;color:var(--ink-2)}
.facet+.facet{margin-top:var(--sp2)}
.facet .label{font:600 var(--s-1)/1 var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-2);margin:0 0 var(--sp1)}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chip{font:400 var(--s0)/1 var(--sans);color:var(--ink);background:none;border:1px solid var(--rule);border-radius:99px;padding:7px 13px;cursor:pointer}
.chip.on{background:var(--accent-soft);border-color:var(--accent);color:var(--accent)}
.chip[disabled]{opacity:.35;cursor:default}
.roots button[data-root=ai].on{color:var(--hue-1);border-bottom-color:var(--hue-1)}
.roots button[data-root=buddhism].on{color:var(--hue-2);border-bottom-color:var(--hue-2)}
.posts{margin-top:var(--sp3)}
.post{display:grid;grid-template-columns:1fr 168px;gap:var(--sp3);align-items:center;text-decoration:none;padding:var(--sp3) 0;border-bottom:1px solid var(--rule)}
.post .kicker{margin-bottom:var(--sp1);color:var(--h)}
.post h2{margin:0 0 8px;font-size:var(--s2);color:var(--ink);transition:color .2s}
.post:hover h2{color:var(--h)}
.post .text>p{color:var(--ink-2);margin:0 0 var(--sp1)}
.post .byline{margin:0}
.art{position:relative;aspect-ratio:1;border-radius:14px;overflow:hidden;display:grid;place-items:center;
  background:radial-gradient(120% 90% at 28% 18%,var(--paper) 0,var(--hs) 62%),var(--hs);transition:transform .4s ease}
.art::before{content:\"\";position:absolute;width:78%;aspect-ratio:1;border-radius:50%;border:1.5px solid color-mix(in srgb,var(--h) 22%,transparent);box-shadow:0 0 0 18px color-mix(in srgb,var(--h) 5%,transparent)}
.art .g{position:relative;font:500 72px/1 var(--display);font-variation-settings:\"opsz\" 144,\"SOFT\" 100;color:var(--h)}
.art .g.long{font-size:44px}
.art .proj{position:absolute;left:12px;bottom:10px;font:600 10px/1 var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--h);opacity:.8}
.post:hover .art{transform:scale(1.03)}
.post.lead{grid-template-columns:1fr;gap:var(--sp2);padding-top:0}
.post.lead .art{order:-1;aspect-ratio:16/7}
.post.lead .art::before{width:auto;height:84%}
.post.lead .art .g{font-size:132px}
.post.lead .art .g.long{font-size:84px}
.post.lead h2{font-size:var(--s3)}
@media(max-width:600px){.post{grid-template-columns:1fr 76px;gap:var(--sp1);align-items:start}.art .g{font-size:40px}.art .g.long{font-size:26px}.art .proj{display:none}
  .post.lead .art .g{font-size:96px}.post.lead .art .proj{display:block}}
</style>
</head>
<body>
<div class=\"page\">
<article>
<h1>Explore</h1>
<nav class=\"roots\" id=\"roots\" aria-label=\"Root\"></nav>
<div class=\"bar\"><input id=\"q\" type=\"search\" placeholder=\"Search\" aria-label=\"Search\">
<select id=\"sort\" aria-label=\"Sort\"><option value=\"date\">Newest</option><option value=\"evidence\">Measured first</option><option value=\"readtime\">Shortest</option><option value=\"depth\">Most specific</option></select>
<span class=\"count\" id=\"count\"></span></div>
<details class=\"more\" id=\"places\"><summary>Places</summary><div class=\"body\"><nav class=\"tree\" id=\"tree\"></nav></div></details>
<details class=\"more\" id=\"tags\"><summary>Tags</summary><div class=\"body\" id=\"facets\"></div></details>
<div class=\"posts\" id=\"list\"></div>
</article>
</div>
<div class=\"toolbar\"><button id=\"theme\" type=\"button\">☾ Night</button></div>
<script src=\"assets/blog/blog.js\"></script>
")

(def script "<script>
const ONTO = __ONTOLOGY__, POSTS = __INDEX__
const FACETS = Object.keys(ONTO.facets), EVIDENCE = ['measured', 'built', 'experienced', 'argued']
const HUE = {'Machine Learning': 1, 'Buddhism': 2, 'Sacred Travel': 2, 'Smile': 3, 'Videogames': 4}
const nodes = []
const walk = (n, route) => { const r = [...route, n.id]; nodes.push({...n, route: r}); (n.children || []).forEach(c => walk(c, r)) }
ONTO.tree.forEach(n => walk(n, []))
const key = id => String(id).replace(/^:/, '')
const state = {place: null, q: '', sort: 'date', tags: {}}
const read = () => { const h = new URLSearchParams(location.hash.slice(1)); state.place = h.get('place'); state.q = h.get('q') || ''; state.sort = h.get('sort') || 'date'
  state.tags = {}; FACETS.forEach(f => { const v = h.getAll(f); if (v.length) state.tags[f] = v }) }
const write = () => { const h = new URLSearchParams(); if (state.place) h.set('place', state.place); if (state.q) h.set('q', state.q); if (state.sort !== 'date') h.set('sort', state.sort)
  Object.entries(state.tags).forEach(([f, vs]) => vs.forEach(v => h.append(f, v))); history.replaceState(null, '', '#' + h.toString()); draw() }
const inPlace = (p, place) => !place || p.route.map(key).includes(place)
const hasTags = (p, tags) => Object.entries(tags).every(([f, vs]) => vs.every(v => (p.facets[f] || []).includes(v)))
const matches = (p, q) => !q || (p.title + ' ' + p.kicker + ' ' + (p.description || '')).toLowerCase().includes(q.toLowerCase())
const sorters = {date: (a, b) => (b.date || '').localeCompare(a.date || ''),
  evidence: (a, b) => Math.min(...(a.facets.evidence || ['argued']).map(e => EVIDENCE.indexOf(e))) - Math.min(...(b.facets.evidence || ['argued']).map(e => EVIDENCE.indexOf(e))),
  readtime: (a, b) => (a.readtime || 99) - (b.readtime || 99), depth: (a, b) => b.depth - a.depth}
const esc = s => String(s || '').replace(/[&<>\"]/g, c => ({'&': '&amp;', '<': '&lt;', '>': '&gt;', '\"': '&quot;'}[c]))
const day = d => d ? new Date(d + 'T12:00').toLocaleDateString('en-GB', {day: 'numeric', month: 'long', year: 'numeric'}) : ''
const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e }
const rootOf = place => place ? nodes.find(n => key(n.id) === place)?.route.map(key)[0] : null
function draw() {
  const list = POSTS.filter(p => inPlace(p, state.place) && hasTags(p, state.tags) && matches(p, state.q)).sort(sorters[state.sort])
  document.getElementById('q').value = state.q; document.getElementById('sort').value = state.sort
  document.getElementById('count').textContent = list.length + (list.length === 1 ? ' post' : ' posts')
  const roots = document.getElementById('roots'); roots.replaceChildren(); const cur = rootOf(state.place)
  ;[[null, 'All'], ...ONTO.tree.map(n => [key(n.id), n.label])].forEach(([id, label]) => {
    const b = el('button', cur === id ? 'on' : '', esc(label)); b.type = 'button'; if (id) b.dataset.root = id
    b.onclick = () => { state.place = id; write() }; roots.appendChild(b) })
  const tree = document.getElementById('tree'); tree.replaceChildren()
  nodes.forEach(n => { const id = key(n.id), c = POSTS.filter(p => inPlace(p, id) && hasTags(p, state.tags) && matches(p, state.q)).length
    if (!c && n.route.length > 1) return
    const a = el('a', state.place === id ? 'on' : '', `<span>${esc(n.label)}</span><span class=n>${c}</span>`)
    a.href = '#'; a.style.paddingLeft = (10 + 16 * (n.route.length - 1)) + 'px'; a.title = n.definition
    a.onclick = e => { e.preventDefault(); state.place = state.place === id ? null : id; write() }; tree.appendChild(a) })
  const fx = document.getElementById('facets'); fx.replaceChildren()
  if (Object.keys(state.tags).length) document.getElementById('tags').open = true
  FACETS.forEach(f => { const live = Object.keys(ONTO.facets[f].values).filter(v => POSTS.some(p => (p.facets[f] || []).includes(v)))
    if (!live.length) return
    const d = el('div', 'facet'); const s = el('div', 'label', esc(f)); s.title = ONTO.facets[f].definition; d.appendChild(s)
    const box = el('div', 'chips')
    live.forEach(v => { const on = (state.tags[f] || []).includes(v)
      const c = POSTS.filter(p => inPlace(p, state.place) && matches(p, state.q) && hasTags(p, {...state.tags, [f]: [...(state.tags[f] || []).filter(x => x !== v), v]})).length
      const b = el('button', 'chip' + (on ? ' on' : ''), `${esc(v.replace(/-/g, ' '))} <span class=n>${c}</span>`); b.type = 'button'
      b.title = ONTO.facets[f].values[v]; if (!c && !on) b.disabled = true
      b.onclick = () => { const cur = state.tags[f] || []; state.tags[f] = on ? cur.filter(x => x !== v) : [...cur, v]; if (!state.tags[f].length) delete state.tags[f]; write() }
      box.appendChild(b) }); d.appendChild(box); fx.appendChild(d) })
  const out = document.getElementById('list'); out.replaceChildren()
  list.forEach((p, i) => { const h = HUE[p['site-project']] || 1, g = String(p.glyph || '☀')
    const a = el('a', 'post' + (i === 0 ? ' lead' : ''),
      `<div class=text><p class=kicker>${esc(p.kicker)}</p><h2>${esc(p.title)}</h2><p>${esc(p.description)}</p>`
      + `<div class=byline><span class=who>Dr Thomas Ager</span>${p.date ? '<span class=dot></span><span>' + day(p.date) + '</span>' : ''}${p.readtime ? '<span class=dot></span><span>' + p.readtime + ' min read</span>' : ''}</div></div>`
      + `<div class=art aria-hidden=true><span class=\"g${[...g].length > 1 ? ' long' : ''}\">${esc(g)}</span><span class=proj>${esc(p['site-project'] || '')}</span></div>`)
    a.style.setProperty('--h', `var(--hue-${h})`); a.style.setProperty('--hs', `var(--hue-${h}-soft)`)
    a.href = p.url; out.appendChild(a) })
}
document.getElementById('q').oninput = e => { state.q = e.target.value; write() }
document.getElementById('sort').onchange = e => { state.sort = e.target.value; write() }
addEventListener('hashchange', () => { read(); draw() })
read(); draw()
</script>
</body>
</html>
")

(defn page []
  (str head
       (-> script (str/replace "__ONTOLOGY__" (json/generate-string check/onto))
           (str/replace "__INDEX__" (json/generate-string (check/index))))))

(defn -main [& _]
  (let [site (str root "/site") assets (str site "/assets/blog")]
    (fs/create-dirs assets)
    (doseq [f ["blog.css" "blog.js"]] (fs/copy (str template "/" f) (str assets "/" f) {:replace-existing true}))
    (spit (str site "/explore.html") (page))
    (doseq [f ["index.json" "ontology.json"]] (fs/copy (str dir "/" f) (str site "/" f) {:replace-existing true}))
    (println "explore.html written in the Blog Template," (count (check/index)) "posts")))

(when (= *file* (System/getProperty "babashka.file")) (-main))
