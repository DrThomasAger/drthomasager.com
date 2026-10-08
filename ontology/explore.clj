(ns explore
  "The explore page of drthomasager.com, worn in the Blog Template.
  bb ontology/explore.clj

  The page links the Blog Template's blog.css and blog.js, copied from
  C:/Users/hanjo/Claude/Projects/Blog Template/ into site/assets/blog/, the
  Medium-like reading page with its rose madder palette that Hanjo made the
  blog aesthetic. It reads as a contents page, the posts gathered by month,
  each with its glyph hanging in the margin in its project's hue.

  Every post is written into the HTML itself, with a CollectionPage and
  ItemList in JSON-LD, a canonical address and the social tags, so a crawler
  reads the whole list without running the script. The script only filters,
  sorts and searches what is already there.

  Every view is a URL, e.g. explore.html#place=ai/agents&evidence=measured&q=memory,
  so a reader can share a view and an MCP can name one."
  (:require [cheshire.core :as json]
            [babashka.fs :as fs]
            [clojure.string :as str]))

(def dir (str (fs/parent (fs/absolutize *file*))))
(def root (str (fs/parent dir)))
(load-file (str dir "/check.clj"))

(def template "C:/Users/hanjo/Claude/Projects/Blog Template")
(def base "https://drthomasager.github.io/drthomasager.com/")
(def title "Writing on AI and Buddhism, by place and tag | Dr Thomas Ager")
(def description "Every post of Dr Thomas Ager on AI and Buddhism, from AI agents, prompt languages and local models to insight contemplation, sacred geometry and Tibetan translation, filtered by place, format, model, tool, method and evidence.")

(def hue {"Machine Learning" 1 "Buddhism" 2 "Sacred Travel" 2 "Smile" 3 "Videogames" 4})
(def months ["January" "February" "March" "April" "May" "June" "July" "August" "September" "October" "November" "December"])

(defn esc [s] (-> (str s) (str/replace "&" "&amp;") (str/replace "<" "&lt;") (str/replace ">" "&gt;") (str/replace "\"" "&quot;")))
(defn month-of [d] (when d (str (months (dec (parse-long (subs d 5 7)))) " " (subs d 0 4))))
(defn day-of [d] (when d (str (parse-long (subs d 8 10)) " " (months (dec (parse-long (subs d 5 7)))) " " (subs d 0 4))))
(defn absolute [u] (when-not (str/starts-with? u "file:") (str base u)))

(def style "
<style>
/* the explore page as a contents page, drawn with the Blog Template's own tokens */
.masthead{font:600 var(--s-1)/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;margin:0 0 var(--sp2)}
.masthead a{text-decoration:none;color:var(--ink-2)}
h1{margin-bottom:var(--sp3)}
.roots{display:flex;align-items:baseline;gap:var(--sp1);font:600 var(--s-1)/1 var(--sans);letter-spacing:.14em;text-transform:uppercase;margin:0 0 var(--sp3)}
.roots a{text-decoration:none;color:var(--ink-2);padding-bottom:6px;border-bottom:1.5px solid transparent}
.roots a.on{color:var(--ink);border-bottom-color:currentColor}
.roots a.on[data-root=ai]{color:var(--hue-1)} .roots a.on[data-root=buddhism]{color:var(--hue-2)}
.roots .sep{color:var(--rule)}
.find{display:flex;flex-wrap:wrap;gap:var(--sp2);align-items:baseline;border-bottom:1px solid var(--ink);padding-bottom:10px;margin:0 0 var(--sp2)}
.find input{flex:1;min-width:10rem;font:italic 400 var(--s2)/1.2 var(--serif);color:var(--ink);background:none;border:0;padding:0;outline:none}
.find input::placeholder{color:var(--ink-2);opacity:.7}
.find select{font:italic 400 var(--s0)/1.2 var(--serif);color:var(--ink-2);background:none;border:0;cursor:pointer}
.find .count{font:600 var(--s-1)/1 var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-2)}
.tree a{display:flex;justify-content:space-between;gap:var(--sp1);font:400 var(--s0)/1.35 var(--serif);text-decoration:none;padding:5px 0}
.tree a.on{color:var(--accent);font-style:italic}
.n{font:400 var(--s-1)/1 var(--sans);font-variant-numeric:tabular-nums;color:var(--ink-2)}
.facet+.facet{margin-top:var(--sp2)}
.facet .label{font:600 var(--s-1)/1 var(--sans);letter-spacing:.12em;text-transform:uppercase;color:var(--ink-2);margin:0 0 10px}
.chips{display:flex;flex-wrap:wrap;gap:4px 14px;font:400 var(--s0)/1.5 var(--serif)}
.chip{font:inherit;color:var(--ink);background:none;border:0;padding:0;cursor:pointer;text-decoration:underline;text-decoration-color:var(--rule);text-underline-offset:4px}
.chip:hover{text-decoration-color:var(--accent)}
.chip.on{color:var(--accent);font-style:italic;text-decoration-color:var(--accent)}
.chip[disabled]{color:var(--ink-2);opacity:.45;cursor:default;text-decoration:none}
.chip .n{margin-left:3px}
.month{margin-top:var(--sp4)}
.month>h2{font:italic 400 var(--s2)/1.2 var(--display);font-variation-settings:\"opsz\" 72,\"SOFT\" 100;color:var(--ink-2);margin:0 0 var(--sp1);display:flex;align-items:center;gap:var(--sp2)}
.month>h2::after{content:\"\";flex:1;border-top:1px solid var(--rule)}
ol.contents{list-style:none;margin:0;padding:0}
.entry{position:relative;padding:var(--sp2) 0 var(--sp2) 3.4rem}
.entry+.entry{border-top:1px solid color-mix(in srgb,var(--rule) 60%,transparent)}
.entry .mark{position:absolute;left:0;top:calc(var(--sp2) + 1.35rem);width:2.4rem;text-align:center;font:400 1.7rem/1 var(--display);font-variation-settings:\"opsz\" 144,\"SOFT\" 100;color:var(--h)}
.entry .kicker{font-size:10.5px;color:var(--h);margin:0 0 10px}
.entry h3{font:500 var(--s2)/1.2 var(--display);font-variation-settings:\"opsz\" 72,\"SOFT\" 50;letter-spacing:-.008em;margin:0 0 8px;text-wrap:balance}
.entry h3 a{text-decoration:none}
.entry h3 a:hover{color:var(--h)}
.entry h3 a::after{content:\"\";position:absolute;inset:0}
.entry .desc{color:var(--ink-2);margin:0 0 8px;font-size:calc(var(--s1) * .92)}
.entry .when{font:italic 400 var(--s0)/1.3 var(--serif);color:var(--ink-2)}
.entry:hover .mark{transform:translateY(-1px)}
.entry .mark{transition:transform .3s}
.flat .month{display:none}
.empty{font:italic 400 var(--s1)/1.5 var(--serif);color:var(--ink-2);margin-top:var(--sp4)}
@media(max-width:600px){.find input{flex-basis:100%}.find select{margin-right:auto}.entry{padding-left:2.6rem}.entry .mark{width:1.8rem;font-size:1.35rem}}
</style>")

(defn entry [p]
  (let [h (get hue (:site-project p) 1)]
    (str "<li class=\"entry\" data-slug=\"" (esc (:slug p)) "\" style=\"--h:var(--hue-" h ")\">"
         "<span class=\"mark\" aria-hidden=\"true\">" (esc (or (:glyph p) "☀")) "</span>"
         "<p class=\"kicker\">" (esc (:kicker p)) "</p>"
         "<h3><a href=\"" (esc (:url p)) "\">" (esc (:title p)) "</a></h3>"
         "<p class=\"desc\">" (esc (:description p)) "</p>"
         "<p class=\"when\"><time datetime=\"" (esc (:date p)) "\">" (esc (day-of (:date p))) "</time>"
         (when (:readtime p) (str ", " (:readtime p) " minutes")) "</p></li>")))

(defn listing [posts]
  (let [by (partition-by #(month-of (:date %)) (sort-by :date #(compare %2 %1) posts))]
    (str "<div id=\"list\">"
         (apply str (for [g by]
                      (str "<section class=\"month\"><h2>" (esc (month-of (:date (first g)))) "</h2><ol class=\"contents\">"
                           (apply str (map entry g)) "</ol></section>")))
         "<ol class=\"contents\" id=\"flat\" hidden></ol><p class=\"empty\" id=\"empty\" hidden>Nothing here yet.</p></div>")))

(defn ld [posts]
  (json/generate-string
   {"@context" "https://schema.org" "@type" "CollectionPage" "name" title "description" description
    "url" (str base "explore.html") "inLanguage" "en"
    "author" {"@type" "Person" "name" "Dr Thomas Ager" "url" base}
    "about" [{"@type" "Thing" "name" "Artificial intelligence"} {"@type" "Thing" "name" "Buddhism"}]
    "mainEntity" {"@type" "ItemList" "numberOfItems" (count posts)
                  "itemListElement" (vec (map-indexed (fn [i p] {"@type" "ListItem" "position" (inc i)
                                                                 "item" (cond-> {"@type" "BlogPosting" "headline" (:title p)
                                                                                 "description" (:description p) "datePublished" (:date p)
                                                                                 "articleSection" (:kicker p) "author" {"@type" "Person" "name" "Dr Thomas Ager"}}
                                                                          (absolute (:url p)) (assoc "url" (absolute (:url p))))})
                                                      (sort-by :date #(compare %2 %1) posts)))}}))

(defn head [posts]
  (str "<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>" (esc title) "</title>
<meta name=\"description\" content=\"" (esc description) "\">
<meta name=\"robots\" content=\"index, follow, max-snippet:-1, max-image-preview:large\">
<link rel=\"canonical\" href=\"" base "explore.html\">
<meta property=\"og:type\" content=\"website\"><meta property=\"og:site_name\" content=\"Dr Thomas Ager\">
<meta property=\"og:title\" content=\"" (esc title) "\"><meta property=\"og:description\" content=\"" (esc description) "\">
<meta property=\"og:url\" content=\"" base "explore.html\">
<meta name=\"twitter:card\" content=\"summary\"><meta name=\"twitter:title\" content=\"" (esc title) "\"><meta name=\"twitter:description\" content=\"" (esc description) "\">
<link rel=\"icon\" type=\"image/svg+xml\" href=\"assets/favicon.svg\">
<link rel=\"alternate\" type=\"application/atom+xml\" title=\"Dr Thomas Ager\" href=\"" base "atom.xml\">
<link rel=\"alternate\" type=\"application/json\" href=\"index.json\" title=\"Every post with its place and tags\">
<link rel=\"alternate\" type=\"application/json\" href=\"ontology.json\" title=\"The ontology\">
<script type=\"application/ld+json\">" (ld posts) "</script>
<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
<link href=\"https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,0..100;1,9..144,300..700,0..100&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600&family=Inter:wght@400;500;600;700&display=swap\" rel=\"stylesheet\">
<link rel=\"stylesheet\" href=\"assets/blog/blog.css\">" style "
</head>
<body>
<div class=\"page\">
<main><article>
<p class=\"masthead\"><a href=\"index.html\">Dr Thomas Ager</a></p>
<h1>Writing on AI and Buddhism</h1>
<nav class=\"roots\" id=\"roots\" aria-label=\"AI or Buddhism\"><a href=\"#\" data-root=\"\">All</a><span class=\"sep\">·</span><a href=\"#place=ai\" data-root=\"ai\">AI</a><span class=\"sep\">·</span><a href=\"#place=buddhism\" data-root=\"buddhism\">Buddhism</a></nav>
<div class=\"find\"><input id=\"q\" type=\"search\" placeholder=\"Search the writing\" aria-label=\"Search the writing\">
<select id=\"sort\" aria-label=\"Order\"><option value=\"date\">newest first</option><option value=\"evidence\">measured first</option><option value=\"readtime\">shortest first</option><option value=\"depth\">most specific first</option></select>
<span class=\"count\" id=\"count\">" (count posts) " posts</span></div>
<details class=\"more\" id=\"places\"><summary>Places</summary><div class=\"body\"><nav class=\"tree\" id=\"tree\"></nav></div></details>
<details class=\"more\" id=\"tags\"><summary>Tags</summary><div class=\"body\" id=\"facets\"></div></details>
" (listing posts) "
</article></main>
</div>
<div class=\"toolbar\"><button id=\"theme\" type=\"button\">☾ Night</button></div>
<script src=\"assets/blog/blog.js\"></script>
"))

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
const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e }
const rootOf = place => place ? nodes.find(n => key(n.id) === place)?.route.map(key)[0] : ''
const LI = Object.fromEntries([...document.querySelectorAll('.entry')].map(li => [li.dataset.slug, {li, home: li.parentNode}]))
function draw() {
  const shown = new Set(POSTS.filter(p => inPlace(p, state.place) && hasTags(p, state.tags) && matches(p, state.q)).map(p => p.slug))
  document.getElementById('q').value = state.q; document.getElementById('sort').value = state.sort
  document.getElementById('count').textContent = shown.size + (shown.size === 1 ? ' post' : ' posts')
  document.getElementById('empty').hidden = shown.size > 0
  const cur = rootOf(state.place); document.querySelectorAll('#roots a').forEach(a => a.classList.toggle('on', a.dataset.root === cur))
  const flat = document.getElementById('flat'), list = document.getElementById('list')
  if (state.sort === 'date') { POSTS.slice().sort(sorters.date).forEach(p => LI[p.slug] && LI[p.slug].home.appendChild(LI[p.slug].li)); flat.hidden = true; list.classList.remove('flat') }
  else { POSTS.slice().sort(sorters[state.sort]).forEach(p => LI[p.slug] && flat.appendChild(LI[p.slug].li)); flat.hidden = false; list.classList.add('flat') }
  Object.entries(LI).forEach(([s, {li}]) => li.hidden = !shown.has(s))
  document.querySelectorAll('.month').forEach(m => m.hidden = ![...m.querySelectorAll('.entry')].some(li => !li.hidden))
  const tree = document.getElementById('tree'); tree.replaceChildren()
  nodes.forEach(n => { const id = key(n.id), c = POSTS.filter(p => inPlace(p, id) && hasTags(p, state.tags) && matches(p, state.q)).length
    if (!c && n.route.length > 1) return
    const a = el('a', state.place === id ? 'on' : '', `<span>${esc(n.label)}</span><span class=n>${c}</span>`)
    a.href = '#place=' + id; a.style.paddingLeft = (16 * (n.route.length - 1)) + 'px'; a.title = n.definition
    a.onclick = e => { e.preventDefault(); state.place = state.place === id ? null : id; write() }; tree.appendChild(a) })
  const fx = document.getElementById('facets'); fx.replaceChildren()
  if (Object.keys(state.tags).length) document.getElementById('tags').open = true
  FACETS.forEach(f => { const live = Object.keys(ONTO.facets[f].values).filter(v => POSTS.some(p => (p.facets[f] || []).includes(v)))
    if (!live.length) return
    const d = el('div', 'facet'); const s = el('div', 'label', esc(f)); s.title = ONTO.facets[f].definition; d.appendChild(s)
    const box = el('div', 'chips')
    live.forEach(v => { const on = (state.tags[f] || []).includes(v)
      const c = POSTS.filter(p => inPlace(p, state.place) && matches(p, state.q) && hasTags(p, {...state.tags, [f]: [...(state.tags[f] || []).filter(x => x !== v), v]})).length
      const b = el('button', 'chip' + (on ? ' on' : ''), `${esc(v.replace(/-/g, ' '))}<span class=n>${c}</span>`); b.type = 'button'
      b.title = ONTO.facets[f].values[v]; if (!c && !on) b.disabled = true
      b.onclick = () => { const cur = state.tags[f] || []; state.tags[f] = on ? cur.filter(x => x !== v) : [...cur, v]; if (!state.tags[f].length) delete state.tags[f]; write() }
      box.appendChild(b) }); d.appendChild(box); fx.appendChild(d) })
}
document.querySelectorAll('#roots a').forEach(a => a.onclick = e => { e.preventDefault(); state.place = a.dataset.root || null; write() })
document.getElementById('q').oninput = e => { state.q = e.target.value; write() }
document.getElementById('sort').onchange = e => { state.sort = e.target.value; write() }
addEventListener('hashchange', () => { read(); draw() })
read(); draw()
</script>
</body>
</html>
")

(defn page []
  (let [posts (check/index)]
    (str (head posts)
         (-> script (str/replace "__ONTOLOGY__" (json/generate-string check/onto))
             (str/replace "__INDEX__" (json/generate-string posts))))))

(defn -main [& _]
  (let [site (str root "/site") assets (str site "/assets/blog")]
    (fs/create-dirs assets)
    (doseq [f ["blog.css" "blog.js"]] (fs/copy (str template "/" f) (str assets "/" f) {:replace-existing true}))
    (spit (str site "/explore.html") (page))
    (doseq [f ["index.json" "ontology.json"]] (fs/copy (str dir "/" f) (str site "/" f) {:replace-existing true}))
    (println "explore.html written in the Blog Template," (count (check/index)) "posts")))

(when (= *file* (System/getProperty "babashka.file")) (-main))
