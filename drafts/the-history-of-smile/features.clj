;; bb features.clj, from this folder. Writes features.html and features-data.js,
;; the timeline of what he asked of Smile and when it was built. Each asking is a
;; requirement of Smile in C:\Users\hanjo\Claude\Projects\Smile\Requirement
;; Timeline\timeline.edn, shown in his own words read from its harvest's
;; statements.jsonl. Each building is a commit of the thing's folder, from the
;; Smile Development Timeline's built dossiers. Mismatches show where something
;; was delivered otherwise than asked.
(load-file (str (babashka.fs/parent (babashka.fs/absolutize *file*)) "/build.clj"))
(ns features
  (:require [build :refer [esc tidy cut here buddha-eyes]]
            [clojure.edn :as edn]
            [clojure.string :as s]
            [babashka.fs :as fs]
            [cheshire.core :as json]))

(def smile "C:/Users/hanjo/Claude/Projects/Smile")
(def reqs (filter #(= "Smile" (:project %)) (edn/read-string (slurp (str smile "/Requirement Timeline/timeline.edn")))))
(def built (into {} (for [t (edn/read-string (slurp (str smile "/Smile Development Timeline/built-topics.edn")))]
                      [(:title t) (edn/read-string (slurp (:dossier t)))])))
(def statements
  (memoize (fn [harvest]
             (let [f (str smile "/Instance Harvest/harvests/" harvest "/statements.jsonl")]
               (if (fs/exists? f)
                 (into {} (for [l (s/split-lines (slurp f)) :when (s/starts-with? l "{") :let [m (json/parse-string l true)]] [(:number m) m]))
                 {})))))
(defn words [r] (vec (keep #(get-in (statements (:harvest r)) [% :words]) (:statements r))))
(defn day [ts] (subs (str ts) 0 10))
(defn pretty [d] (let [[y m dd] (s/split d #"-")] (str (Integer/parseInt dd) " " (["January" "February" "March" "April" "May" "June" "July" "August" "September" "October" "November" "December"] (dec (Integer/parseInt m))) " " y)))

(def ask-kinds #{"requested feature" "user requirement" "UX requirement"})
(def whole "the project as a whole")
(def things
  (->> (group-by :thing reqs)
       (map (fn [[thing rs]]
              (let [asks (filter #(ask-kinds (:kind %)) rs)
                    asks (if (= thing whole) (filter #(= "requested feature" (:kind %)) asks) asks)
                    otherwise (filter #(= "mismatch" (:kind %)) rs)
                    commits (:commits (built thing))]
                {:thing (if (= thing whole) "Smile as a whole" thing)
                 :asks (sort-by :first asks) :otherwise (sort-by :first otherwise) :commits (sort-by :date commits)})))
       (remove #(and (empty? (:asks %)) (empty? (:commits %))))
       (sort-by #(or (some-> % :asks first :first day) (some-> % :commits first :date) "9999"))))

(defn anchor [t] (str "f-" (s/replace (s/lower-case (:thing t)) #"[^a-z0-9]+" "-")))

(def data
  {:lanes (vec (for [t things]
                 {:name (:thing t) :a (anchor t)
                  :asks (vec (for [r (:asks t)] {:d (day (:first r)) :x (cut (or (first (words r)) (:title r)) 200)}))
                  :built (vec (for [c (:commits t)] {:d (:date c) :x (cut (:subject c) 160)}))
                  :otherwise (vec (for [r (:otherwise t)] {:d (day (:first r)) :x (cut (:title r) 200)}))}))})

(defn entry-html [t]
  (let [rows (sort-by first
                      (concat (for [r (:asks t)] [(day (:first r)) 0 r])
                              (for [c (:commits t)] [(:date c) 1 c])
                              (for [r (:otherwise t)] [(day (:first r)) 2 r])))]
    (str "<details class=\"more\" id=\"" (anchor t) "\"><summary><span>" (esc (:thing t))
         "<small class=\"meta\">" (count (:asks t)) " asked · " (count (:commits t)) " commits · " (count (:otherwise t)) " delivered otherwise</small></span></summary><div class=\"body\">\n<ol class=\"feat\">\n"
         (apply str
                (for [[d k x] rows]
                  (case k
                    0 (str "<li class=\"ask\"><span class=\"meta\">" (pretty d) " · asked</span>"
                           (let [ws (words x)]
                             (if (seq ws) (apply str (for [w ws] (str "<blockquote>" (esc (s/trim w)) "</blockquote>")))
                                 (str "<p>" (esc (:title x)) "</p>")))
                           "<p class=\"meta\">The harvest recorded it as “" (esc (:title x)) "”, " (esc (:harvest x)) " " (esc (:code x)) ".</p></li>\n")
                    1 (str "<li class=\"built\"><span class=\"meta\">" (pretty d) " · built · <code>" (esc (:hash x)) "</code></span><p>" (esc (:subject x)) "</p></li>\n")
                    2 (str "<li class=\"otherwise\"><span class=\"meta\">" (pretty d) " · delivered otherwise</span><p>" (esc (:title x)) "</p><p class=\"meta\">" (esc (:harvest x)) " " (esc (:code x)) ".</p></li>\n"))))
         "</ol></div></details>\n")))

(def n-asks (reduce + (map (comp count :asks) things)))
(def n-commits (reduce + (map (comp count :commits) things)))
(def n-other (reduce + (map (comp count :otherwise) things)))
(def title "What I Asked of Smile and When It Was Built, a Timeline of Features")

(spit (str here "/features-data.js") (str "window.F = " (json/generate-string data) "\n"))
;; The page features.html was folded into index.html on 18 October 2026, one post not two,
;; so only features-data.js is written now. The page below is kept for reference.
(comment (str here "/features.html")
      (str "<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>" (esc title) "</title>
<meta name=\"description\" content=\"Every feature I asked of Smile in my own words, dated to the minute, beside the commits that built it, from July to October 2026, part by part.\">
<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
<link href=\"https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,0..100;1,9..144,300..700,0..100&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap\" rel=\"stylesheet\">
<link rel=\"stylesheet\" href=\"../../../Blog Template/blog.css\">
<link rel=\"stylesheet\" href=\"history.css\">
<style>
  ol.feat{list-style:none;padding:0;margin:0}
  ol.feat li{margin:0 0 var(--sp2);padding-left:14px;border-left:3px solid var(--rule)}
  ol.feat li.ask{border-color:var(--accent)}
  ol.feat li.built{border-color:var(--hue-4)}
  ol.feat li.otherwise{border-color:var(--hue-2)}
  ol.feat li p{margin:4px 0}
  ol.feat blockquote{margin:6px 0;font-style:italic}
</style>
</head>
<body>
<div class=\"progress\"></div>
<div class=\"page\">
<article>
<p class=\"kicker\">AI › Prompt Engineering › Prompt Languages › Smile</p>
<p class=\"series\"><a href=\"index.html\">The History of Smile</a></p>
<h1>" (esc title) "</h1>
<p class=\"lede\">Each part of Smile, what I asked of it in my own words, the day each commit built it, and where it was delivered otherwise than asked.</p>
<div class=\"byline\"><span class=\"who\">Dr Thomas Ager</span><span class=\"dot\"></span><span>18 October 2026</span></div>
<p class=\"authorship\">(claude wrote this for me)</p>

<figure class=\"bleed reveal\" data-diagram=\"f\"><figcaption><b>Figure 1</b>One lane for each part of Smile. A blue dot is something I asked for, a green square a commit that built it, a rose cross something delivered otherwise than asked. " n-asks " askings, " n-commits " commits and " n-other " delivered otherwise, from July to October 2026. Press a lane to open it below.</figcaption></figure>

<p class=\"drop\">This timeline begins on 22 July 2026, when Smile's work moved into Claude Code and every chat began to be harvested. Each asking here is a requirement a harvest recorded, shown in the words I typed, with the harvest's own one-line record of it beneath. Each building is a commit to the folder of that part. The askings before July 2026, in ChatGPT, Claude and my documents, were never harvested in this way and are not yet in it, and some chats of August 2026 still wait for their harvest, which is why several parts show commits in August with no asking beside them.</p>

<h2 id=\"parts\">Each part, asked and built</h2>
" (apply str (map entry-html things)) "
<h3>Sources</h3>
<ol class=\"sources\">
<li>The timeline of my requirements, C:\\Users\\hanjo\\Claude\\Projects\\Smile\\Requirement Timeline\\timeline.edn, from the Instance Harvest.</li>
<li>My words, read from each harvest's statements.jsonl in C:\\Users\\hanjo\\Claude\\Projects\\Smile\\Instance Harvest\\harvests.</li>
<li>The commits of each folder, C:\\Users\\hanjo\\Claude\\Projects\\Smile\\Smile Development Timeline\\built.</li>
</ol>
</article>
</div>
<div class=\"toolbar\"><button id=\"restore\" type=\"button\" hidden>Restore removed</button><button id=\"theme\" type=\"button\">☾ Night</button></div>
<script src=\"https://cdn.jsdelivr.net/npm/d3@7.9.0\"></script>
<script src=\"features-data.js\"></script>
<script src=\"features.js\"></script>
<script src=\"../../../Blog Template/blog.js\"></script>
<script>
  const draw = el => { el.querySelectorAll('.slot').forEach(s => s.remove())
    const slot = document.createElement('div'); slot.className = 'slot'; el.prepend(slot); FD.draw(slot) }
  const all = () => document.querySelectorAll('[data-diagram]').forEach(draw)
  all(); document.addEventListener('blog:theme', all)
  let w = innerWidth; addEventListener('resize', () => { if ((w < 600) !== (innerWidth < 600)) all(); w = innerWidth })
</script>
" (buddha-eyes) "
</body>
</html>
"))
(println "features.html," (count things) "parts," n-asks "askings," n-commits "commits," n-other "delivered otherwise")
