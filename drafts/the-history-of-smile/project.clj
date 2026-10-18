;; bb project.clj <built-id> [...] | all | mark <built-id> <status>, from this folder.
;; Writes <built-id>\index.html and data.js for each project of Smile whose
;; prose-built\<built-id>.edn exists, from that prose and the project's dossier in
;; the Smile Development Timeline. In the prose, [[r]] cites the folder's README,
;; [[c:hash]] cites one commit, [[m:YYYY-MM-DD]] (or #2) one moment of his words,
;; [[t:topic-id]] links an idea post, [[p:built-id]] a project post, and
;; {{commits}}, {{began}}, {{last}}, {{moments}} are counted from the dossier.
(load-file (str (babashka.fs/parent (babashka.fs/absolutize *file*)) "/build.clj"))
(ns project
  (:require [build :refer [esc tidy cut topics topic-of src here buddha-eyes]]
            [clojure.edn :as edn]
            [clojure.string :as s]
            [babashka.fs :as fs]
            [cheshire.core :as json]))

(def built-file (str src "/built-topics.edn"))
(def projects (sort-by :order (edn/read-string (slurp built-file))))
(def by-id (into {} (map (juxt :id identity) projects)))
(def order (mapv :id projects))
(def idea (into {} (map (juxt :id identity) topics)))
(defn pretty-date [d]
  (if-not d "undated"
          (let [[y m dd] (s/split d #"-")]
            (str (Integer/parseInt dd) " " (["January" "February" "March" "April" "May" "June" "July" "August" "September" "October" "November" "December"] (dec (Integer/parseInt m))) " " y))))
(defn written?
  "A post counts as written when its page is on disk and its topic, idea or project, passed its check (:tested)."
  [id] (and (= :tested (:status (or (idea id) (by-id id)))) (fs/exists? (str here "/" id "/index.html"))))
(defn href [id] (when (written? id) (str "../" id "/index.html")))
(defn link [id text] (if-let [h (href id)] (str "<a href=\"" h "\">" text "</a>") text))
(defn section-id [name] (:id (topic-of name)))
(defn folder-name [p] (fs/file-name (:folder p)))

(defn render [text ctx notes]
  (let [local (atom [])
        add! (fn [html] (let [n (inc (count @notes))] (swap! notes conj html) (swap! local conj [n html]) (str "<sup class=\"fn\"><a href=\"#n" n "\">" n "</a></sup>")))
        out (-> text
                (s/replace #"\{\{([a-z]+)\}\}" (fn [[_ k]] (str (or ((:counts ctx) k) (throw (ex-info (str "no count " k) {}))))))
                (s/replace #"\[\[t:([a-z0-9-]+)\]\]" (fn [[_ id]] (let [t (or (idea id) (throw (ex-info (str "no idea " id) {})))] (link id (esc (:title t))))))
                (s/replace #"\[\[p:([a-z0-9-]+)\]\]" (fn [[_ id]] (let [t (or (by-id id) (throw (ex-info (str "no project " id) {})))] (link id (esc (:title t))))))
                ;; one pass over every citation, so sidenotes number in reading order
                (s/replace #"\[\[(r|c:[0-9a-f]+|m:[0-9-]+(?:#\d+)?)\]\]"
                           (fn [[_ tok]]
                             (add!
                              (cond
                                (= tok "r") (str "The README of the project folder, " (esc (str (fs/path (:readme (:p ctx))))) ", written by the instances who built it.")
                                (s/starts-with? tok "c:")
                                (let [h (subs tok 2) c (or (first (filter #(s/starts-with? (:hash %) h) (:commits ctx))) (throw (ex-info (str "no commit " h) {})))]
                                  (str (pretty-date (:date c)) ", commit <code>" (esc (:hash c)) "</code> to the Smile repository, “" (esc (:subject c)) "”, <a href=\"#commits\">every commit below</a>."))
                                :else
                                (let [[_ d k] (re-find #"m:([0-9-]+)(?:#(\d+))?" tok)
                                      ms (filter #(= d (:date %)) (:said ctx))
                                      m (or (nth ms (dec (Integer/parseInt (or k "1"))) nil) (throw (ex-info (str "no moment " d) {})))]
                                  (str (esc (tidy (or (:where m) (str "my words, " (pretty-date (:date m)))))) ", " (count (:quotes m)) " quote" (when (not= 1 (count (:quotes m))) "s") " of his, <a href=\"#m-" (:id m) "\">read them below</a>. Record <code>" (esc (:id m)) "</code>.")))))))]
    (str "<p>" out "</p>\n"
         (apply str (for [[n html] @local] (str "<p class=\"sn\" id=\"n" n "\"><span class=\"n\">" n "</span>" html "</p>\n"))))))

(defn page [id]
  (let [p (by-id id) d (edn/read-string (slurp (:dossier p)))
        prose (edn/read-string (slurp (str here "/prose-built/" id ".edn")))
        commits (sort-by :date (:commits d)) said (sort-by #(or (:date %) "9999") (:said d))
        counts {"commits" (count commits) "moments" (count said)
                "began" (pretty-date (:began p)) "last" (pretty-date (:last-commit p))}
        ctx {:p p :commits commits :said said :counts counts}
        notes (atom [])
        lede (render (:lede prose) ctx notes)
        body (apply str (map #(render % ctx notes) (:paras prose)))
        i (.indexOf order id) prev (when (pos? i) (by-id (order (dec i)))) nxt (by-id (get order (inc i)))
        series (str "<p class=\"series\"><a href=\"../index.html\">The History of Smile</a>, how it was built, project " (:order p) " of " (count projects)
                    (when prev (str " · " (link (:id prev) (str "← " (esc (:title prev))))))
                    (when nxt (str " · " (link (:id nxt) (str (esc (:title nxt)) " →")))) "</p>\n")
        title (:title prose) desc (:description prose) faq (:faq prose)
        by-day (sort-by key (group-by :date commits))
        data {:title (str (:title p) " commits")
              :moments (vec (for [[day cs] by-day] {:d day :q (count cs) :w (str (count cs) " commit" (when (not= 1 (count cs)) "s")) :x (cut (:subject (first cs)) 160) :a "commits"}))
              :beside (vec (concat (when (seq said) [{:name "My words on it" :dates (vec (keep :date said)) :href "#words"}])
                                   (for [sec (:sections p) :let [sid (section-id sec)] :when sid]
                                     {:name sec :dates (vec (keep #(when (= sec (:section %)) (:date %)) said)) :href (href sid)})))}
        words (count (re-seq #"\w+" (str body (s/join " " (map second faq)))))]
    {:data data
     :html
     (str "<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>" (esc title) "</title>
<meta name=\"description\" content=\"" (esc desc) "\">
<meta name=\"keywords\" content=\"" (esc (:keywords prose)) "\">
<meta name=\"author\" content=\"Dr Thomas Ager\">
<meta property=\"og:type\" content=\"article\">
<meta property=\"og:title\" content=\"" (esc title) "\">
<meta property=\"og:description\" content=\"" (esc desc) "\">
<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
<link href=\"https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,0..100;1,9..144,300..700,0..100&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap\" rel=\"stylesheet\">
<link rel=\"stylesheet\" href=\"../../../../Blog Template/blog.css\">
<link rel=\"stylesheet\" href=\"../history.css\">
<script type=\"application/ld+json\">
" (json/generate-string
   {"@context" "https://schema.org"
    "@graph" [{"@type" "BlogPosting" "headline" title "description" desc
               "author" {"@type" "Person" "name" "Dr Thomas Ager" "url" "https://github.com/DrThomasAger"}
               "datePublished" "2026-10-18" "inLanguage" "en"
               "isPartOf" {"@type" "CreativeWorkSeries" "name" "The History of the Smile Prompt Language, how it was built"}
               "position" (:order p) "about" ["Smile Prompt Language" (:title p) "prompt engineering"]}
              {"@type" "FAQPage" "mainEntity" (for [[q a] faq] {"@type" "Question" "name" q "acceptedAnswer" {"@type" "Answer" "text" a}})}]})
"
</script>
</head>
<body>
<div class=\"progress\"></div>
<div class=\"page\">
<article>
<p class=\"kicker\">AI › Prompt Engineering › Prompt Languages › Smile</p>
" series "
<h1>" (esc title) "</h1>
" (s/replace lede #"^<p>" "<p class=\"lede\">") "
<div class=\"byline\"><span class=\"who\">Dr Thomas Ager</span><span class=\"dot\"></span><span>18 October 2026</span><span class=\"dot\"></span><span>" (max 1 (Math/round (/ words 230.0))) " min read</span></div>
<p class=\"authorship\">(claude wrote this for me)</p>

<figure class=\"bleed reveal\" data-diagram=\"figure\"><figcaption><b>Figure 1</b>Every day of commits to " (esc (:title p)) ", " (count commits) " in all from " (counts "began") " to " (counts "last") (when (seq said) ", with the days he spoke of it and the ideas of THE MAP those words belong to") ".</figcaption></figure>

" (s/replace-first body #"^<p>" "<p class=\"drop\">") "
<h2 id=\"commits\">Every commit</h2>
<p>Each commit to " (esc (:title p)) " in the Smile repository on my PC, with its hash and its subject as written.</p>
<ol class=\"order-list\">
" (apply str (for [c commits] (str "<li><span class=\"meta\">" (pretty-date (:date c)) " · <code>" (esc (:hash c)) "</code></span><br>" (esc (:subject c)) "</li>\n"))) "</ol>
" (when (seq said)
    (str "<h2 id=\"words\">In my words</h2>\n<p>Each moment where I spoke of " (esc (:title p)) ", with every quote of mine from there, word for word.</p>\n"
         (apply str (for [m said]
                      (str "<details class=\"more\" id=\"m-" (:id m) "\"><summary><span>" (pretty-date (:date m))
                           "<small class=\"meta\">" (esc (tidy (or (:where m) (:section m)))) " · " (count (:quotes m)) " quote" (when (not= 1 (count (:quotes m))) "s") "</small></span></summary><div class=\"body\">\n"
                           (apply str (for [q (:quotes m)] (str "<blockquote>" (esc (s/trim q)) "</blockquote>\n")))
                           (when-let [sid (section-id (:section m))] (str "<p class=\"meta\">Part of the idea " (link sid (esc (:section m))) ".</p>\n"))
                           "<p class=\"meta\">Record <code>" (esc (:id m)) "</code>.</p></div></details>\n")))))
"
<h2 id=\"faq\" class=\"faq\">Questions</h2>
" (apply str (for [[q a] faq] (str "<h3>" (esc q) "</h3>\n<p>" (esc a) "</p>\n"))) "
<h3>Sources</h3>
<ol class=\"sources\">
<li>The README of the project, " (esc (str (fs/path (:readme p)))) ".</li>
<li>The dossier of the project, " (esc (str (fs/path (:dossier p)))) ", every commit and every quote of mine found word for word.</li>
</ol>
" series "
</article>
</div>
<div class=\"toolbar\"><button id=\"restore\" type=\"button\" hidden>Restore removed</button><button id=\"theme\" type=\"button\">☾ Night</button></div>
<script src=\"https://cdn.jsdelivr.net/npm/d3@7.9.0\"></script>
<script src=\"data.js\"></script>
<script src=\"../topic.js\"></script>
<script src=\"../../../../Blog Template/blog.js\"></script>
<script>
  const draw = el => { el.querySelectorAll('.slot').forEach(s => s.remove())
    const slot = document.createElement('div'); slot.className = 'slot'; el.prepend(slot)
    TD[el.dataset.diagram](slot) }
  const all = () => document.querySelectorAll('[data-diagram]').forEach(draw)
  all()
  document.addEventListener('blog:theme', all)
  let w = innerWidth; addEventListener('resize', () => { if ((w < 600) !== (innerWidth < 600)) all(); w = innerWidth })
</script>
" (buddha-eyes) "
</body>
</html>
")}))

(defn mark! [id status]
  (let [ts (edn/read-string (slurp built-file))
        post (str (s/replace here "\\" "/") "/" id "/index.html")]
    (spit built-file (with-out-str (clojure.pprint/pprint (mapv #(if (= id (:id %)) (assoc % :post post :status status) %) ts))))))

(defn build! [id]
  (let [{:keys [html data]} (page id)]
    (fs/create-dirs (str here "/" id))
    (spit (str here "/" id "/index.html") html)
    (spit (str here "/" id "/data.js") (str "window.T = " (json/generate-string data) "\n"))
    (println id "written," (count html) "chars")))

(let [args *command-line-args*]
  (cond (= "mark" (first args)) (do (mark! (second args) (keyword (nth args 2))) (println "marked" (second args) (nth args 2)))
        (= ["all"] args) (doseq [id order :when (fs/exists? (str here "/prose-built/" id ".edn"))] (build! id))
        :else (doseq [id args] (build! id))))
