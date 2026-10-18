;; bb topic.clj <topic-id> [...], from this folder, or bb topic.clj all.
;; Writes <topic-id>\index.html and <topic-id>\data.js for each topic whose
;; prose\<topic-id>.edn exists, from that prose and the topic's dossier in the
;; Smile Development Timeline. In the prose, [[m:YYYY-MM-DD]] (or
;; [[m:YYYY-MM-DD#2]] for the second moment of a day) becomes a sidenote naming
;; that moment's source, [[t:topic-id]] a link to that idea's post or its place
;; in the timeline, and {{moments}}, {{quotes}}, {{first}}, {{last}} counts.
(load-file (str (babashka.fs/parent (babashka.fs/absolutize *file*)) "/build.clj"))
(ns topic
  (:require [build :refer [esc tidy cut topics topic-of src here buddha-eyes]]
            [clojure.edn :as edn]
            [clojure.string :as s]
            [babashka.fs :as fs]
            [cheshire.core :as json]))

(def by-id (into {} (map (juxt :id identity) topics)))
(def order (vec (map :id topics)))
(defn dossier [id] (edn/read-string (slurp (str src "/topics/" id ".edn"))))
(defn written?
  "A post counts as written when its page is on disk and its topic passed its check (:tested), the same rule as build.clj."
  [id] (and (= :tested (:status (by-id id))) (fs/exists? (str here "/" id "/index.html"))))
(defn href
  "A link to a post only when it is written, otherwise nil, so an unwritten post is named without a link."
  [id] (when (written? id) (str "../" id "/index.html")))
(defn link [id text] (if-let [h (href id)] (str "<a href=\"" h "\">" text "</a>") text))
(defn id-of-section [name] (:id (topic-of name)))

(declare pretty-date)

;; Why each moment belongs to its feature, one sentence per said id, written by
;; smile-96 from its whole reading into for-the-posts\why.edn, batch by batch.
(def why-of
  (let [f (str src "/for-the-posts/why.edn")]
    (if (fs/exists? f) (edn/read-string (slurp f)) {})))

;; What was built for each idea, so the series is one blog. A project belongs to
;; an idea when its dossier names the idea in :sections, or when the idea's
;; entry in features-timeline.md names the project as what was built.
(def projects (edn/read-string (slurp (str src "/built-topics.edn"))))
(def feature-text
  "Each feature's whole entry in features-timeline.md, by its name."
  (let [ls (s/split-lines (slurp (str src "/reading/features-timeline.md")))]
    (loop [[l & more] ls cur nil acc {}]
      (cond (nil? l) acc
            (re-find #"^ {8}\( .+ \($" l) (recur more (s/trim (subs (s/trim l) 1 (- (count (s/trim l)) 1))) acc)
            (and cur (re-find #"^ {8}\) End " l)) (recur more nil acc)
            cur (recur more cur (update acc cur str " " (s/trim l)))
            :else (recur more cur acc)))))
(def feature-alias {"A universal language of prompting" "Precursor, a universal language of prompting"
                    "The prompt that explains itself" "Meta-instruction, the prompt that explains itself"
                    "The section with a strong middle" "Section" "Integrity, the linter" "Integrity"
                    "Sensing and Smile-ification" "Sensing / Smile-ification" "Transfer, densifying" "Transfer" "Transfer, one prompt across models" "Transfer"
                    "The life of an instance, harvested" "The life of an instance"})
;; Projects neither :sections nor the features timeline place, set by their READMEs.
(def placed-by-readme
  {"Smile Zettelkasten" "Memory"
   "Client Decomposition" "Module" "Frame Custody" "Recording" "Live Prompt Delivery" "Conditions and actions"
   "Zoom Meetings" "Recording"
   "Execution" "The work in hand"
   "Requirement Timeline" "The work in hand"})
;; Placements the features timeline names that do not connect obviously, cut.
(def not-obvious #{["THE MAP Viewer" "Card"] ["Prompt Coach" "The Prompt Doctor"] ["Modularization" "Composing from inside a prompt"] ["Smile Composing Door" "Composing from inside a prompt"] ["Pair Extraction" "Lens"] ["C-explain D3 and Paper.js" "Offering"] ["Prompt Specs" "Card"] ["Requirement Timeline" "The work in hand"] ["Steering Harness" "Infrastructure"]})
(defn built-for
  "The projects built for an idea, in the order they began."
  [t]
  (let [sec (last (:pillar t))
        text (s/join " " (for [[k v] feature-text :when (= (:title t) (feature-alias k k))] v))]
    (->> projects
         (remove (fn [p] (not-obvious [(:title p) (:title t)])))
         (filter (fn [p] (or (= (placed-by-readme (:title p)) (:title t))
                             (and (seq text) (re-find (re-pattern (str (java.util.regex.Pattern/quote (str (:title p))) "(?! [A-Z])(?![A-Za-z])")) text)))))
         (sort-by :began))))
;; How much of each feature the code carries today, from the Map session's reading
;; of every amendment against the code, keyed by post slug.
(def build-state
  (let [f "C:/Users/hanjo/Claude/Projects/Smile/Smile Prompt Language/THE MAP with his amendments/build state by section.json"]
    (if (fs/exists? f) (json/parse-string (slurp f)) {})))
(defn state-html [t]
  (when-let [s (build-state (:id t))]
    (let [n #(or (s %) 0)]
      (str "<p class=\"state\">In the code today it is " (esc (s "state")) ", with " (n "built") " of my amendments to it built, "
           (n "part built") " part built and " (n "not built") " not yet built."
           (when-let [sum (s "summary")] (str " " (esc sum)))
           "</p>\n"))))
(defn built-html [t]
  (let [ps (built-for t) st (state-html t)]
    (when (or (seq ps) st)
      (str "<h2 id=\"built\">What was built</h2>\n" st
           (when (seq ps) (str "<p>The project folders I began for " (esc (:title t))
           ", each a folder on my PC with its own README and commits.</p>\n"))
           (apply str
                  (for [p ps :let [f (str here "/prose-built/" (:id p) ".edn")
                                   lede (when (fs/exists? f) (:lede (edn/read-string (slurp f))))
                                   n (if (number? (:commits p)) (:commits p) (count (:commits p)))]]
                    (str "<div class=\"built\"><h3>" (esc (:title p)) "</h3>\n"
                         "<p class=\"meta\">Begun " (pretty-date (:began p)) ", " n " commit" (when (not= 1 n) "s")
                         (when (:readme p) (str ", README at <code>" (esc (str (:readme p))) "</code>")) ".</p>\n"
                         (when (and lede (not (re-find #"“|\[\[" lede))) (str "<p>" (esc lede) "</p>\n"))
                         "</div>\n")))))))
(defn pretty-date [d]
  (if-not d "undated"
          (let [[y m dd] (s/split d #"-")]
            (str (Integer/parseInt dd) " " (["January" "February" "March" "April" "May" "June" "July" "August" "September" "October" "November" "December"] (dec (Integer/parseInt m))) " " y))))

(defn where-of [m]
  ;; a source line with no date of its own ends in a bare dot, and its day is the latest it can have been said
  (let [w (tidy (:where m))]
    (if (re-find #"·\s*$" w) (str (s/trim (s/replace w #"·\s*$" "")) ", by " (pretty-date (:date m))) w)))

(defn render [text ctx notes]
  (let [local (atom [])
        out (-> text
                (s/replace #"\{\{([a-z]+)\}\}" (fn [[_ k]] (str (or ((:counts ctx) k) (throw (ex-info (str "no count " k) {}))))))
                (s/replace #"\[\[t:([a-z0-9-]+)\]\]"
                           (fn [[_ id]] (let [t (or (by-id id) (throw (ex-info (str "no topic " id) {})))]
                                          (link id (esc (:title t))))))
                (s/replace #"\[\[m:([0-9-]+|undated)(?:#(\d+))?\]\]"
                           (fn [[_ d k]]
                             (let [ms (filter #(= d (or (:date %) "undated")) (:moments ctx))
                                   m (or (nth ms (dec (Integer/parseInt (or k "1"))) nil) (throw (ex-info (str "no moment " d) {})))
                                   n (inc (count @notes))
                                   html (str (esc (where-of m)) ", " (count (:quotes m)) " quote" (when (not= 1 (count (:quotes m))) "s")
                                             " of mine, <a href=\"#m-" (:id m) "\">read them below</a>. Record <code>" (esc (:id m)) "</code>.")]
                               (swap! notes conj html) (swap! local conj [n html])
                               (str "<sup class=\"fn\"><a href=\"#n" n "\">" n "</a></sup>")))))]
    (str "<p>" out "</p>\n"
         (apply str (for [[n html] @local] (str "<p class=\"sn\" id=\"n" n "\"><span class=\"n\">" n "</span>" html "</p>\n"))))))

(defn beside [moments self]
  (->> moments (mapcat (fn [m] (map #(vector % (:date m)) (:said-beside m))))
       (remove #(= self (first %)))
       (group-by first)
       (map (fn [[k v]] {:name k :dates (vec (sort (keep second v))) :n (count v)}))
       (sort-by (comp - :n))))

(defn page [id]
  (let [t (by-id id) d (dossier id) prose (edn/read-string (slurp (str here "/prose/" id ".edn")))
        ;; moments the reading judged not to speak of this feature are left out, from the prose's :exclude
        moments (sort-by #(or (:date %) "9999") (remove #((set (:exclude prose)) (:id %)) (:moments d)))
        dated (keep :date moments)
        counts {"moments" (count moments) "quotes" (reduce + (map (comp count :quotes) moments))
                "first" (pretty-date (first dated)) "last" (pretty-date (last dated))}
        ctx {:moments moments :counts counts}
        notes (atom [])
        body (apply str (map #(render % ctx notes) (:paras prose)))
        lede (render (:lede prose) ctx notes)
        bs (beside moments (:title t))
        i (.indexOf order id) prev (when (pos? i) (by-id (order (dec i)))) nxt (by-id (get order (inc i)))
        series (str "<p class=\"series\"><a href=\"../index.html\">The History of Smile</a>, part " (:order t) " of " (count topics)
                    (when prev (str " · " (link (:id prev) (str "← " (esc (:title prev))))))
                    (when nxt (str " · " (link (:id nxt) (str (esc (:title nxt)) " →")))) "</p>\n")
        title (:title prose)
        desc (:description prose)
        faq (:faq prose)
        archive (apply str
                       (for [m moments]
                         (str "<details class=\"more\" id=\"m-" (:id m) "\"><summary><span>" (pretty-date (:date m))
                              "<small class=\"meta\">" (esc (where-of m)) " · " (count (:quotes m)) " quote" (when (not= 1 (count (:quotes m))) "s") "</small></span></summary><div class=\"body\">\n"
                              (when-let [w (why-of (:id m))] (str "<p class=\"why\">" (esc w) "</p>\n"))
                              (apply str (for [q (:quotes m)] (str "<blockquote>" (esc (s/trim q)) "</blockquote>\n")))
                              (when (seq (:said-beside m))
                                (str "<p class=\"meta\">Said in the same place as "
                                     (s/join ", " (for [o (:said-beside m) :let [oid (id-of-section o)]]
                                                    (if oid (link oid (esc o)) (esc o)))) ".</p>\n"))
                              "<p class=\"meta\">Record <code>" (esc (:id m)) "</code>.</p></div></details>\n")))
        data {:title (:title t)
              :moments (vec (for [m moments] {:d (:date m) :q (count (:quotes m)) :w (where-of m) :x (cut (first (:quotes m)) 180) :a (str "m-" (:id m))}))
              :beside (vec (for [b (take 6 bs) :let [oid (id-of-section (:name b))]]
                             {:name (:name b) :dates (:dates b) :href (if oid (href oid) "../index.html#pillars")}))}
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
               "isPartOf" {"@type" "CreativeWorkSeries" "name" "The History of the Smile Prompt Language"}
               "position" (:order t)
               "about" ["Smile Prompt Language" (:title t) "prompt engineering"]}
              {"@type" "FAQPage" "mainEntity" (for [[q a] faq] {"@type" "Question" "name" q "acceptedAnswer" {"@type" "Answer" "text" a}})}
              {"@type" "BreadcrumbList" "itemListElement"
               (map-indexed (fn [i [n u]] {"@type" "ListItem" "position" (inc i) "name" n "item" u})
                            [["AI" "https://drthomasager.com/ai"] ["Prompt Engineering" "https://drthomasager.com/ai/prompt-engineering"]
                             ["Prompt Languages" "https://drthomasager.com/ai/prompt-engineering/prompt-languages"]
                             ["Smile" "https://drthomasager.com/ai/prompt-engineering/prompt-languages/smile"]])}]})
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

<figure class=\"bleed reveal\" data-diagram=\"figure\"><figcaption><b>Figure 1</b>Every moment I spoke of " (esc (:title t)) ", " (counts "moments") " in all, and below it the ideas I spoke of in the same places most often. Press a dot to read my words.</figcaption></figure>

" (s/replace-first body #"^<p>" (str "<p class=\"drop illuminated\" data-symbol=\"smile\" data-hue=\"3\" data-seed=\"" id "\">")) "
" (built-html t) "
<h2 id=\"moments\">Every moment, in my words</h2>
<p>Each moment is one conversation, document or recording where I spoke of " (esc (:title t)) ", from " (counts "first") " to " (counts "last") ", with every quote of mine from there, word for word.</p>
" archive "
<h2 id=\"beside\">The ideas it grew beside</h2>
<p>How many times each idea was spoken of in the same place as " (esc (:title t)) ".</p>
<ol class=\"order-list\">
" (apply str (for [b (take 10 bs) :let [oid (id-of-section (:name b))]]
               (str "<li>" (if oid (link oid (esc (:name b))) (esc (:name b))) " <span class=\"meta\">" (:n b) "</span></li>\n"))) "
</ol>

<h2 id=\"faq\" class=\"faq\">Questions</h2>
" (apply str (for [[q a] faq] (str "<h3>" (esc q) "</h3>\n<p>" (esc a) "</p>\n"))) "
<h3>Sources</h3>
<ol class=\"sources\">
<li>The dossier of " (esc (:title t)) ", C:\\Users\\hanjo\\Claude\\Projects\\Smile\\Smile Development Timeline\\topics\\" id ".edn, every quote found word for word in its source.</li>
<li>THE MAP, C:\\Users\\hanjo\\Claude\\Projects\\Smile\\Smile Prompt Language\\THE MAP.md, " (if-let [sec (get-in build-state [id "section"])] (str "the section " (esc sec)) "which does not yet give this idea a section of its own") ".</li>
<li>The public Smile repository, <a href=\"https://github.com/DrThomasAger/smile\">https://github.com/DrThomasAger/smile</a>.</li>
</ol>
" series "
</article>
</div>
<div class=\"toolbar\"><button id=\"restore\" type=\"button\" hidden>Restore removed</button><button id=\"theme\" type=\"button\">☾ Night</button></div>
<script src=\"https://cdn.jsdelivr.net/npm/d3@7.9.0\"></script>
<script src=\"data.js\"></script>
<script src=\"../topic.js\"></script>
<script src=\"../../../../Blog Template/blog.js\"></script>
<script src=\"../../../../Blog Template/initial.js\"></script>
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
  ;; writes :post and :status into the topic in topics.edn, keeping its order and every other field
  (let [f (str src "/topics.edn")
        ts (edn/read-string (slurp f))
        post (str (s/replace here "\\" "/") "/" id "/index.html")
        ts' (mapv #(if (= id (:id %)) (assoc % :post post :status status) %) ts)]
    (spit f (with-out-str (clojure.pprint/pprint ts')))))

(defn build! [id]
  (let [{:keys [html data]} (page id)]
    (fs/create-dirs (str here "/" id))
    (spit (str here "/" id "/index.html") html)
    (spit (str here "/" id "/data.js") (str "window.T = " (json/generate-string data) "\n"))
    (println id "written," (count html) "chars")))

(let [args *command-line-args*
      ids (if (= ["all"] args) (keep #(when (fs/exists? (str here "/prose/" % ".edn")) %) order) args)]
  (if (= "mark" (first args))
    (do (mark! (second args) (keyword (nth args 2))) (println "marked" (second args) (nth args 2)))
    (doseq [id ids] (build! id))))
