(ns explore
  "The explore page of drthomasager.com, written from the ontology and its index.
  bb ontology/explore.clj    runs check.clj's index, then writes explore.html into ontology/ and site/

  Every view is a URL, e.g. explore.html#place=ai/agents&format=trial&sort=evidence&q=memory,
  so a reader can share a view and an MCP can name one."
  (:require [cheshire.core :as json]
            [babashka.fs :as fs]
            [clojure.string :as str]))

(def dir (str (fs/parent (fs/absolutize *file*))))
(load-file (str dir "/check.clj"))

(def page-template "<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
<title>Explore every post by place and tag, Dr Thomas Ager</title>
<meta name=\"description\" content=\"Every post of Dr Thomas Ager in one place, under AI or Buddhism, filtered by format, model, tool, method, project, practice, level and evidence, sorted by date, evidence, read time or depth.\">
<link rel=\"alternate\" type=\"application/json\" href=\"index.json\" title=\"Every post with its place and tags\">
<link rel=\"alternate\" type=\"application/json\" href=\"ontology.json\" title=\"The ontology\">
<link href=\"https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400..600&family=Newsreader:opsz,wght@6..72,400..500&family=Inter:wght@400;500;600&display=swap\" rel=\"stylesheet\">
<style>
:root{--paper:#f9f8f6;--surface:#f2f0ec;--ink:#22212a;--ink-2:#5f5d68;--rule:#e3e0da;--accent:#3d4fa1;--accent-soft:#e9ecf7;--rose:#b4495e}
@media (prefers-color-scheme: dark){:root:not([data-theme=light]){--paper:#151823;--surface:#1d2130;--ink:#e9e7f1;--ink-2:#a9a7b8;--rule:#2d3244;--accent:#9eb1f3;--accent-soft:#232a42;--rose:#ef97a8}}
:root[data-theme=dark]{--paper:#151823;--surface:#1d2130;--ink:#e9e7f1;--ink-2:#a9a7b8;--rule:#2d3244;--accent:#9eb1f3;--accent-soft:#232a42;--rose:#ef97a8}
*{box-sizing:border-box}
body{margin:0;background:var(--paper);color:var(--ink);font:400 17px/1.5 Newsreader,Georgia,serif}
.wrap{max-width:1180px;margin:0 auto;padding:32px 16px 84px}
h1{font:500 40px/1.1 Fraunces,Georgia,serif;margin:0 0 8px}
.lede{color:var(--ink-2);margin:0 0 24px;max-width:680px}
.grid{display:grid;grid-template-columns:280px 1fr;gap:32px}
@media (max-width:820px){.grid{grid-template-columns:1fr}}
aside{font-family:Inter,sans-serif;font-size:14px}
summary.label{cursor:pointer;margin-top:0}
.label{font:600 12px/1 Inter,sans-serif;letter-spacing:.12em;text-transform:uppercase;color:var(--ink-2);margin:20px 0 8px}
.tree a{display:flex;justify-content:space-between;color:var(--ink);text-decoration:none;padding:3px 6px;border-radius:6px}
.tree a:hover{background:var(--surface)}
.tree a.on{background:var(--accent-soft);color:var(--accent);font-weight:600}
.tree .n{color:var(--ink-2);font-variant-numeric:tabular-nums}
.chips{display:flex;flex-wrap:wrap;gap:6px}
.chip{border:1px solid var(--rule);background:var(--paper);color:var(--ink);border-radius:999px;padding:3px 10px;font:500 13px/1.4 Inter,sans-serif;cursor:pointer}
.chip.on{background:var(--accent);border-color:var(--accent);color:var(--paper)}
.chip[disabled]{opacity:.4;cursor:default}
.bar{display:flex;gap:10px;flex-wrap:wrap;align-items:center;margin-bottom:16px;font-family:Inter,sans-serif;font-size:14px}
.bar input{flex:1;min-width:180px;padding:8px 12px;border:1px solid var(--rule);border-radius:8px;background:var(--surface);color:var(--ink);font:inherit}
.bar select{padding:8px;border:1px solid var(--rule);border-radius:8px;background:var(--surface);color:var(--ink);font:inherit}
.count{color:var(--ink-2)}
.post{padding:16px 0;border-top:1px solid var(--rule)}
.kicker{font:600 12px/1.4 Inter,sans-serif;letter-spacing:.1em;text-transform:uppercase;color:var(--accent)}
.post h2{font:500 22px/1.25 Fraunces,Georgia,serif;margin:4px 0 6px}
.post h2 a{color:var(--ink);text-decoration:none}.post h2 a:hover{text-decoration:underline}
.meta{font:400 13px/1.5 Inter,sans-serif;color:var(--ink-2)}
.tags{margin-top:6px;display:flex;flex-wrap:wrap;gap:4px}
.tag{font:500 12px/1.4 Inter,sans-serif;background:var(--surface);color:var(--ink-2);border-radius:999px;padding:1px 8px}
button.reset{border:none;background:none;color:var(--rose);font:500 13px Inter,sans-serif;cursor:pointer;padding:0}
</style>
</head>
<body>
<div class=\"wrap\">
<h1>Explore</h1>
<p class=\"lede\">Every post lives at one place under AI or Buddhism, and carries its tags. Choose a place, any tags, a sort, or search. The view is kept in the address, so it can be shared, and the same data is in <a href=\"index.json\">index.json</a> and <a href=\"ontology.json\">ontology.json</a>.</p>
<div class=\"grid\">
<aside><details id=\"filters\" open><summary class=\"label\">Places and tags</summary><div class=\"label\">Place</div><nav class=\"tree\" id=\"tree\"></nav><div id=\"facets\"></div></details></aside>
<main>
<div class=\"bar\"><input id=\"q\" type=\"search\" placeholder=\"Search titles and places\" aria-label=\"Search\">
<select id=\"sort\" aria-label=\"Sort\"><option value=\"date\">Newest first</option><option value=\"evidence\">Measured first</option><option value=\"readtime\">Shortest first</option><option value=\"depth\">Most specific first</option></select>
<span class=\"count\" id=\"count\"></span><button class=\"reset\" id=\"reset\" type=\"button\">Clear</button></div>
<div id=\"list\"></div>
</main></div></div>
<script>
const ONTO = __ONTOLOGY__, POSTS = __INDEX__
const FACETS = Object.keys(ONTO.facets)
const EVIDENCE = [\"measured\", \"built\", \"experienced\", \"argued\"]
const nodes = []
const walk = (n, route) => { const r = [...route, n.id]; nodes.push({...n, route: r}); (n.children || []).forEach(c => walk(c, r)) }
ONTO.tree.forEach(n => walk(n, []))
const key = id => String(id).replace(/^:/, \"\")
const state = {place: null, q: \"\", sort: \"date\", tags: {}}
const read = () => { const h = new URLSearchParams(location.hash.slice(1)); state.place = h.get(\"place\"); state.q = h.get(\"q\") || \"\"; state.sort = h.get(\"sort\") || \"date\"
  state.tags = {}; FACETS.forEach(f => { const v = h.getAll(f); if (v.length) state.tags[f] = v }) }
const write = () => { const h = new URLSearchParams(); if (state.place) h.set(\"place\", state.place); if (state.q) h.set(\"q\", state.q); if (state.sort !== \"date\") h.set(\"sort\", state.sort)
  Object.entries(state.tags).forEach(([f, vs]) => vs.forEach(v => h.append(f, v))); history.replaceState(null, \"\", \"#\" + h.toString()); draw() }
const inPlace = (p, place) => !place || p.route.map(key).includes(place)
const hasTags = (p, tags) => Object.entries(tags).every(([f, vs]) => vs.every(v => (p.facets[f] || []).includes(v)))
const matches = (p, q) => !q || (p.title + \" \" + p.kicker).toLowerCase().includes(q.toLowerCase())
const shown = () => POSTS.filter(p => inPlace(p, state.place) && hasTags(p, state.tags) && matches(p, state.q))
const sorters = {date: (a, b) => (b.date || \"\").localeCompare(a.date || \"\"),
  evidence: (a, b) => Math.min(...(a.facets.evidence || [\"argued\"]).map(e => EVIDENCE.indexOf(e))) - Math.min(...(b.facets.evidence || [\"argued\"]).map(e => EVIDENCE.indexOf(e))),
  readtime: (a, b) => (a.readtime || 99) - (b.readtime || 99), depth: (a, b) => b.depth - a.depth}
function draw() {
  const list = shown().sort(sorters[state.sort])
  document.getElementById(\"q\").value = state.q; document.getElementById(\"sort\").value = state.sort
  document.getElementById(\"count\").textContent = list.length + (list.length === 1 ? \" post\" : \" posts\")
  const tree = document.getElementById(\"tree\"); tree.replaceChildren()
  nodes.forEach(n => { const id = key(n.id), c = POSTS.filter(p => inPlace(p, id) && hasTags(p, state.tags) && matches(p, state.q)).length
    if (!c && n.route.length > 1) return
    const a = document.createElement(\"a\"); a.href = \"#\"; a.style.paddingLeft = (6 + 14 * (n.route.length - 1)) + \"px\"
    a.className = state.place === id ? \"on\" : \"\"; a.title = n.definition
    a.innerHTML = `<span>${n.label}</span><span class=n>${c}</span>`
    a.onclick = e => { e.preventDefault(); state.place = state.place === id ? null : id; write() }; tree.appendChild(a) })
  const fx = document.getElementById(\"facets\"); fx.replaceChildren()
  FACETS.forEach(f => { const vals = Object.keys(ONTO.facets[f].values)
    const live = vals.filter(v => POSTS.some(p => (p.facets[f] || []).includes(v)))
    if (!live.length) return
    const l = document.createElement(\"div\"); l.className = \"label\"; l.textContent = f; l.title = ONTO.facets[f].definition; fx.appendChild(l)
    const box = document.createElement(\"div\"); box.className = \"chips\"
    live.forEach(v => { const on = (state.tags[f] || []).includes(v)
      const c = POSTS.filter(p => inPlace(p, state.place) && matches(p, state.q) && hasTags(p, {...state.tags, [f]: [...(state.tags[f] || []).filter(x => x !== v), v]})).length
      const b = document.createElement(\"button\"); b.type = \"button\"; b.className = \"chip\" + (on ? \" on\" : \"\"); b.textContent = v.replace(/-/g, \" \") + \" \" + c
      b.title = ONTO.facets[f].values[v]; if (!c && !on) b.disabled = true
      b.onclick = () => { const cur = state.tags[f] || []; state.tags[f] = on ? cur.filter(x => x !== v) : [...cur, v]; if (!state.tags[f].length) delete state.tags[f]; write() }
      box.appendChild(b) }); fx.appendChild(box) })
  const out = document.getElementById(\"list\"); out.replaceChildren()
  list.forEach(p => { const d = document.createElement(\"article\"); d.className = \"post\"
    const tags = Object.entries(p.facets).flatMap(([f, vs]) => vs.map(v => `<span class=tag title=\"${f}\">${v.replace(/-/g, \" \")}</span>`)).join(\"\")
    d.innerHTML = `<div class=kicker>${p.kicker}</div><h2><a href=\"${p.url}\">${p.title}</a></h2><div class=meta>${p.date || \"\"}${p.readtime ? \" · \" + p.readtime + \" min read\" : \"\"}</div><div class=tags>${tags}</div>`
    out.appendChild(d) })
}
document.getElementById(\"q\").oninput = e => { state.q = e.target.value; write() }
document.getElementById(\"sort\").onchange = e => { state.sort = e.target.value; write() }
document.getElementById(\"reset\").onclick = () => { state.place = null; state.q = \"\"; state.sort = \"date\"; state.tags = {}; write() }
addEventListener(\"hashchange\", () => { read(); draw() })
// on a phone the filters fold shut, so the posts come first
if (innerWidth < 820) document.getElementById(\"filters\").open = false
read(); draw()
</script>
</body>
</html>
")

(defn -main [& _]
  (let [html (-> page-template
                 (str/replace "__ONTOLOGY__" (json/generate-string check/onto))
                 (str/replace "__INDEX__" (json/generate-string (check/index))))
        site (str (fs/parent dir) "/site")]
    (spit (str dir "/explore.html") html)
    (when (fs/exists? site)
      (spit (str site "/explore.html") html)
      (fs/copy (str dir "/index.json") (str site "/index.json") {:replace-existing true})
      (fs/copy (str dir "/ontology.json") (str site "/ontology.json") {:replace-existing true}))
    (println "explore.html written," (count (check/index)) "posts")))

(when (= *file* (System/getProperty "babashka.file")) (-main))
