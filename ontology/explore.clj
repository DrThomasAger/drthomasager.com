(ns explore
  "The explore page of drthomasager.com, in the site's own writerly look.
  bb ontology/explore.clj

  The page is made from one of the writerly site's own pages,
  platform/sites/drthomasager/out/buddhism.html, its head, header, hero, footer
  and popup kept whole, with the explore view set in its main. Each post is the
  site's own card, as card() in build.py makes it, its art in the deep shade of
  its project's colour and its title on that project's shadow. It is written to
  platform/sites/drthomasager/out/ and to site/, with index.json and ontology.json.

  Every view is a URL, e.g. explore.html#place=ai/agents&evidence=measured&q=memory,
  so a reader can share a view and an MCP can name one."
  (:require [cheshire.core :as json]
            [babashka.fs :as fs]
            [clojure.string :as str]))

(def dir (str (fs/parent (fs/absolutize *file*))))
(def root (str (fs/parent dir)))
(load-file (str dir "/check.clj"))

(def writerly (str root "/platform/sites/drthomasager/out"))

;; build.py's colours, the Five Buddha Families, and its card(), in Clojure
(def project-colours {"Buddhism" "#ffffff" "Smile" "#f5c542" "Videogames" "#62d194"
                      "Sacred Travel" "#ff7f8d" "Machine Learning" "#6f9ce4"})
(defn- hx [c] (mapv #(Integer/parseInt (subs c % (+ % 2)) 16) [1 3 5]))
(defn- mix [a b t] (let [x (hx a) y (hx b)] (apply str "#" (map #(format "%02x" (Math/round (double (+ (x %) (* (- (y %) (x %)) t))))) (range 3)))))
(defn deep [c] (mix c "#000000" 0.55))
(defn shadow [c] (if (= c "#ffffff") "#cfcfcf" c))

(def style "
<style>
/* the explore view, drawn only with the theme's own tokens */
.explore{display:grid;grid-template-columns:16rem 1fr;gap:2.5rem;align-items:start}
@media (max-width:820px){.explore{grid-template-columns:1fr}}
.explore aside{font-family:var(--font-body);color:var(--ink)}
.explore details > summary{cursor:pointer;font-family:var(--font-head);font-size:1.15rem;margin-bottom:.6rem}
.explore .facet-name{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;margin:1.4rem 0 .5rem}
.explore .tree a{display:flex;justify-content:space-between;gap:.6rem;color:var(--ink);text-decoration:none;padding:.18rem .4rem;border-radius:var(--btn-radius)}
.explore .tree a:hover{text-decoration:underline}
.explore .tree a.on{background:var(--ink);color:var(--page-bg)}
.explore .tree .n,.explore .count{font-variant-numeric:tabular-nums;opacity:.75}
.explore .chips{display:flex;flex-wrap:wrap;gap:.4rem}
.explore .chip{font:inherit;font-size:.85rem;color:var(--ink);background:var(--page-bg);border:var(--card-art-border);border-radius:var(--btn-radius);padding:.15rem .55rem;cursor:pointer}
.explore .chip.on{background:var(--ink);color:var(--page-bg);box-shadow:var(--btn-shadow)}
.explore .chip[disabled]{opacity:.35;cursor:default}
.explore .bar{display:flex;flex-wrap:wrap;gap:.8rem;align-items:center;margin-bottom:1.6rem}
.explore .bar input,.explore .bar select{font:inherit;color:var(--ink);background:var(--callout-bg);border:var(--callout-border);border-radius:var(--field-radius);padding:.45rem .7rem}
.explore .bar input{flex:1;min-width:12rem}
.explore .bar button{font:inherit;background:none;border:none;color:var(--ink);text-decoration:underline;cursor:pointer}
.explore .route{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;margin:.5rem 0 .25rem;opacity:.85}
.explore .meta{font-size:.85rem;opacity:.75;margin-top:.4rem}
</style>")

(def main-html "<main><section class=\"band\"><div class=\"band-head\"><h2>Every post, by place and tag</h2></div>
<div class=\"explore\">
<aside><details id=\"filters\" open><summary>Places and tags</summary><div class=\"facet-name\">Place</div><nav class=\"tree\" id=\"tree\"></nav><div id=\"facets\"></div></details></aside>
<div><div class=\"bar\"><input id=\"q\" type=\"search\" placeholder=\"Search titles and places\" aria-label=\"Search\">
<select id=\"sort\" aria-label=\"Sort\"><option value=\"date\">Newest first</option><option value=\"evidence\">Measured first</option><option value=\"readtime\">Shortest first</option><option value=\"depth\">Most specific first</option></select>
<span class=\"count\" id=\"count\"></span><button id=\"reset\" type=\"button\">Clear</button></div>
<div class=\"grid\" id=\"list\"></div></div>
</div></section></main>")

(def script "<script>
const ONTO = __ONTOLOGY__, POSTS = __INDEX__
const FACETS = Object.keys(ONTO.facets), EVIDENCE = ['measured', 'built', 'experienced', 'argued']
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
function draw() {
  const list = POSTS.filter(p => inPlace(p, state.place) && hasTags(p, state.tags) && matches(p, state.q)).sort(sorters[state.sort])
  document.getElementById('q').value = state.q; document.getElementById('sort').value = state.sort
  document.getElementById('count').textContent = list.length + (list.length === 1 ? ' post' : ' posts')
  const tree = document.getElementById('tree'); tree.replaceChildren()
  nodes.forEach(n => { const id = key(n.id), c = POSTS.filter(p => inPlace(p, id) && hasTags(p, state.tags) && matches(p, state.q)).length
    if (!c && n.route.length > 1) return
    const a = document.createElement('a'); a.href = '#'; a.style.paddingLeft = (0.4 + 0.9 * (n.route.length - 1)) + 'rem'
    a.className = state.place === id ? 'on' : ''; a.title = n.definition
    a.innerHTML = `<span>${esc(n.label)}</span><span class=n>${c}</span>`
    a.onclick = e => { e.preventDefault(); state.place = state.place === id ? null : id; write() }; tree.appendChild(a) })
  const fx = document.getElementById('facets'); fx.replaceChildren()
  FACETS.forEach(f => { const live = Object.keys(ONTO.facets[f].values).filter(v => POSTS.some(p => (p.facets[f] || []).includes(v)))
    if (!live.length) return
    const l = document.createElement('div'); l.className = 'facet-name'; l.textContent = f; l.title = ONTO.facets[f].definition; fx.appendChild(l)
    const box = document.createElement('div'); box.className = 'chips'
    live.forEach(v => { const on = (state.tags[f] || []).includes(v)
      const c = POSTS.filter(p => inPlace(p, state.place) && matches(p, state.q) && hasTags(p, {...state.tags, [f]: [...(state.tags[f] || []).filter(x => x !== v), v]})).length
      const b = document.createElement('button'); b.type = 'button'; b.className = 'chip' + (on ? ' on' : ''); b.textContent = v.replace(/-/g, ' ') + ' ' + c
      b.title = ONTO.facets[f].values[v]; if (!c && !on) b.disabled = true
      b.onclick = () => { const cur = state.tags[f] || []; state.tags[f] = on ? cur.filter(x => x !== v) : [...cur, v]; if (!state.tags[f].length) delete state.tags[f]; write() }
      box.appendChild(b) }); fx.appendChild(box) })
  const out = document.getElementById('list'); out.replaceChildren()
  list.forEach(p => { const a = document.createElement('a'); a.className = 'card'; a.href = p.url
    a.innerHTML = `<div class=\"card-art\" aria-hidden=\"true\" style=\"color:${p.art}\"><span>${esc(p.glyph || '☀')}</span></div>`
      + `<div class=\"route\">${esc(p.kicker)}</div><h3 class=\"ptx-shadow card-title\" style=\"--pc:${p.pc}\">${esc(p.title)}</h3>`
      + `<p>${esc(p.description)}</p><div class=\"meta\">${esc(p.date)}${p.readtime ? ' · ' + p.readtime + ' min read' : ''}</div>`
    out.appendChild(a) })
}
document.getElementById('q').oninput = e => { state.q = e.target.value; write() }
document.getElementById('sort').onchange = e => { state.sort = e.target.value; write() }
document.getElementById('reset').onclick = () => { state.place = null; state.q = ''; state.sort = 'date'; state.tags = {}; write() }
addEventListener('hashchange', () => { read(); draw() })
if (innerWidth < 820) document.getElementById('filters').open = false
read(); draw()
</script>")

(defn posts []
  (vec (for [p (check/index) :let [c (get project-colours (:site-project p) "#ffffff")]]
         (assoc p :art (deep c) :pc (shadow c)))))

(defn page []
  (let [shell (slurp (str writerly "/buddhism.html"))
        body (-> shell
                 (str/replace #"<title>[^<]*</title>" "<title>Explore — Dr Thomas Ager</title>")
                 (str/replace #"<meta name=\"description\" content=\"[^\"]*\">"
                              "<meta name=\"description\" content=\"Every post of Dr Thomas Ager by place and tag, under AI or Buddhism, filtered by format, model, tool, method, project, practice, level and evidence.\">\n<link rel=\"alternate\" type=\"application/json\" href=\"index.json\" title=\"Every post with its place and tags\">\n<link rel=\"alternate\" type=\"application/json\" href=\"ontology.json\" title=\"The ontology\">")
                 (str/replace "</head>" (str style "</head>"))
                 (str/replace "<h1>Buddhism</h1><p class=\"hero-sub\">The dharma as lived, translated, and walked into.</p>"
                              "<h1>Explore</h1><p class=\"hero-sub\">Every post lives at one place under AI or Buddhism, and carries its tags. Choose a place, any tags, a sort, or search.</p>"))
        i (str/index-of body "<main>") j (+ (str/index-of body "</main>") 7)]
    (assert (str/includes? body "<h1>Explore</h1>") "the hero was not found in the shell")
    (str (subs body 0 i) main-html
         (-> script (str/replace "__ONTOLOGY__" (json/generate-string check/onto)) (str/replace "__INDEX__" (json/generate-string (posts))))
         (subs body j))))

(defn -main [& _]
  (let [html (page) site (str root "/site")]
    (spit (str writerly "/explore.html") html)
    (doseq [f ["index.json" "ontology.json"]] (fs/copy (str dir "/" f) (str writerly "/" f) {:replace-existing true}))
    ;; the live site carries the writerly theme beside its own, for this page alone
    (fs/copy (str writerly "/assets/theme.css") (str site "/assets/writerly.css") {:replace-existing true})
    (fs/copy (str writerly "/assets/base.css") (str site "/assets/writerly-base.css") {:replace-existing true})
    (spit (str site "/explore.html") (-> html (str/replace "href=\"assets/base.css\"" "href=\"assets/writerly-base.css\"")
                                         (str/replace "href=\"assets/theme.css\"" "href=\"assets/writerly.css\"")))
    (doseq [f ["index.json" "ontology.json"]] (fs/copy (str dir "/" f) (str site "/" f) {:replace-existing true}))
    (fs/delete-if-exists (str dir "/explore.html"))
    (println "explore.html written in the writerly look," (count (posts)) "posts")))

(when (= *file* (System/getProperty "babashka.file")) (-main))
