;; bb build.clj, run from this folder, writes index.html and data.js from the
;; Smile Development Timeline that smile-96 gathers. Every number in the page
;; is counted here from those files, and every citation is resolved here.
(ns build
  (:require [clojure.edn :as edn]
            [clojure.string :as s]
            [babashka.fs :as fs]
            [cheshire.core :as json]
            [babashka.process]))

(def src "C:/Users/hanjo/Claude/Projects/Smile/Smile Development Timeline")
(def here (str (fs/parent (fs/absolutize *file*))))
(defn rd [f] (edn/read-string (slurp (str src "/" f))))
;; Figure 1, the chains of features and how much of each is built, drawn fresh on every build
(babashka.process/shell {:dir here} "bb" "chains.clj")

(def events (rd "events.edn"))
(def pillars (rd "pillars.edn"))
(def topics (sort-by :order (rd "topics.edn")))

(defn esc [x] (-> (str x) (s/replace "&" "&amp;") (s/replace "<" "&lt;") (s/replace ">" "&gt;") (s/replace "\"" "&quot;")))
(defn tidy [x] (-> (str x) (s/replace #"\s+" " ") (s/replace " — " ", ") (s/replace "—" ", ") s/trim))
(defn cut [x n] (let [t (tidy x)] (if (> (count t) n) (str (s/trim (subs t 0 n)) "…") t)))

(def topic-of (into {} (map (fn [t] [(last (:pillar t)) t]) topics)))
(defn anchor [section] (str "s-" (:id (topic-of section) (s/replace (s/lower-case section) #"[^a-z0-9]+" "-"))))

;; ---------------------------------------------------------------- counts
(def said (filter #(= :said (:kind %)) events))
(def built (filter #(= :built (:kind %)) events))
(def folders (filter #(= :folder (:kind %)) events))
(defn public? [b] (boolean (re-find #"public" (:title b))))
(defn ncommits [bs] (reduce + (map (comp count :commits) bs)))
(defn month [e] (some-> (:date e) (subs 0 7)))
(defn in-months [lo hi es] (filter #(when-let [m (month %)] (and (<= 0 (compare m lo)) (<= (compare m hi) 0))) es))
(def first-flagged (into {} (map (juxt :section identity) (filter :first-of-section said))))
(def said-by-id (into {} (map (juxt :id identity) said)))
(defn first-of
  "The first event of a section, or, when the reading moved its first quote,
  the earliest moment of the topic dossier, carrying that moment's own quotes."
  [sec]
  (or (first-flagged sec)
      (when-let [t (topic-of sec)]
        (let [f (str src "/topics/" (:id t) ".edn")]
          (when (.exists (java.io.File. f))
            (when-let [m (first (sort-by :date (:moments (edn/read-string (slurp f)))))]
              (merge (said-by-id (:id m)) (select-keys m [:id :date :quotes]) {:source {:where (:where m)}})))))))
(def built-on (group-by :date built))
(def folder-named (into {} (map (fn [f] [(s/replace (:title f) #"^Project begun, " "") f]) folders)))

(def busiest (apply max-key (comp count :commits) (filter public? built)))
(def N {"events" (count events)
        "said" (count said)
        "quotes" (reduce + (map (comp count :quotes) said))
        "sections" (count (mapcat :sections (mapcat :threads pillars)))
        "regions" (count pillars)
        "threads" (count (mapcat :threads pillars))
        "topics" (count topics)
        "public-commits" (ncommits (filter public? built))
        "public-aug-nov" (ncommits (in-months "2025-08" "2025-11" (filter public? built)))
        "pc-commits" (ncommits (remove public? built))
        "busiest-n" (count (:commits busiest))
        "first-2023-10-03" (count (filter #(and (:first-of-section %) (= "2023-10-03" (:date %))) said))
        "quiet" (count (in-months "2023-11" "2025-06" said))
        "aug-oct-2026" (count (in-months "2026-08" "2026-10" said))
        "folders" (count folders)
        "undated" (count (remove :date said))
        "aug-oct-pct" (Math/round (* 100.0 (/ (count (in-months "2026-08" "2026-10" said)) (count (filter :date said)))))})

;; ---------------------------------------------------------------- citations
;; In the prose, [[first:Section]], [[built:YYYY-MM-DD]] and [[folder:Name]]
;; become a numbered sidenote naming the source, {{key}} becomes a count from N,
;; and [[quote:Section]] becomes the first words of his on that section.
(def notes (atom []))

(defn note-html [kind arg]
  (case kind
    "first" (let [e (or (first-of arg) (throw (ex-info (str "no first event for " arg) {})))]
              (str (esc (tidy (get-in e [:source :where]))) ", the first moment of "
                   "<a href=\"#" (anchor arg) "\">" (esc arg) "</a>, " (count (:quotes e)) " quote"
                   (when (not= 1 (count (:quotes e))) "s") " of mine. Record <code>" (esc (:id e)) "</code>."))
    "built" (let [bs (or (built-on arg) (throw (ex-info (str "no commits on " arg) {})))
                  b (first bs) c (first (:commits b))]
              (str arg ", " (count (:commits b)) " commit" (when (not= 1 (count (:commits b))) "s")
                   (if (public? b) " to the public repository" " to the Smile repository on my PC")
                   ", the first of the day "
                   (if (:url c) (str "<a href=\"" (esc (:url c)) "\">“" (esc (:subject c)) "”</a>")
                       (str "“" (esc (:subject c)) "” (" (esc (:hash c)) ")")) "."))
    "folder" (let [f (or (folder-named arg) (throw (ex-info (str "no folder " arg) {})))]
               (str "The project folder " (esc arg) ", begun " (:date f) ", in C:\\Users\\hanjo\\Claude\\Projects\\Smile."))))

(defn render-para [text]
  (let [local (atom [])
        body (-> text
                 (s/replace #"\{\{([a-z0-9-]+)\}\}" (fn [[_ k]] (format "%,d" (or (N k) (throw (ex-info (str "no count " k) {}))))))
                 (s/replace #"\[\[quote:([^\]]+)\]\]"
                            (fn [[_ sec]] (str "“" (esc (s/replace (cut (first (:quotes (first-of sec))) 200) #"[.]$" "")) "”")))
                 (s/replace #"\[\[(first|built|folder):([^\]]+)\]\]"
                            (fn [[_ k a]]
                              (let [n (inc (count @notes)) html (note-html k a)]
                                (swap! notes conj html)
                                (swap! local conj [n html])
                                (str "<sup class=\"fn\"><a href=\"#n" n "\">" n "</a></sup>")))))]
    (str "<p>" body "</p>\n"
         (apply str (for [[n html] @local]
                      (str "<p class=\"sn\" id=\"n" n "\"><span class=\"n\">" n "</span>" html "</p>\n"))))))

;; ---------------------------------------------------------------- the features
;; The eras and features come from smile-96's reading\features-timeline.md,
;; a Smile file. Depth 1 sections are eras, depth 2 are features. In a
;; feature the lines before the > line say when and where he first asked, the
;; > line is his asking kept exactly, and the lines after it say what was built
;; and how the meaning moved.
(def feature-alias {"A universal language of prompting" "Precursor, a universal language of prompting"
                    "The prompt that explains itself" "Meta-instruction, the prompt that explains itself"
                    "The section with a strong middle" "Section"
                    "Integrity, the linter" "Integrity"
                    "Sensing and Smile-ification" "Sensing / Smile-ification"
                    "Transfer, densifying" "Transfer" "Transfer, one prompt across models" "Transfer"
                    "The life of an instance, harvested" "The life of an instance"})
(def topic-by-title (into {} (map (juxt :title identity) topics)))

(defn header [l] (second (re-find #"^\s*\(\s+(.+?)\s+\($" l)))
(defn footer? [l] (re-find #"^\s*\)\s+End " l))
(defn depth [l] (quot (count (re-find #"^\s*" l)) 4))

(defn parse-features []
  (let [ls (s/split-lines (slurp (str src "/reading/features-timeline.md")))]
    (loop [[l & more] ls eras [] cur nil]
      (cond
        (nil? l) eras
        (and (header l) (= 1 (depth l))) (recur more (conj eras {:era (header l) :features []}) nil)
        (and (header l) (= 2 (depth l))) (recur more eras {:name (header l) :lines []})
        (and (footer? l) (= 2 (depth l)) cur)
        (recur more (update-in eras [(dec (count eras)) :features] conj cur) nil)
        cur (recur more eras (update cur :lines conj (s/trim l)))
        :else (recur more eras cur)))))

(defn feature-parts [{:keys [lines]}]
  (let [[before [q & after]] (split-with #(not (s/starts-with? % ">")) lines)]
    (if q
      {:when (s/join " " before) :quote (s/trim (subs q 1)) :moved (s/join " " after)}
      {:when "" :quote nil :moved (s/join " " before)})))

(def eras (vec (remove #(= "What this file is" (:era %)) (parse-features))))

(defn written?
  "A post counts as written when its page is on disk and its topic passed its check (:tested)."
  [t]
  (and t (= :tested (:status t)) (.exists (java.io.File. (str here "/" (:id t) "/index.html")))))

(defn feature-link [name]
  (let [t (topic-by-title (feature-alias name name))]
    (cond (written? t) (str "<a href=\"" (:id t) "/index.html\">" (esc name) "</a>")
          :else (esc name))))

;; Why each first asking belongs to its feature, written for Hanjo's ask to
;; know why a quote is related to its idea.
(def feature-why (edn/read-string (slurp (str here "/features-why.edn"))))
(defn feature-moments
  "Every moment I spoke of the feature, from its topic dossier, in date order."
  [name]
  (when-let [t (topic-by-title (feature-alias name name))]
    (let [f (str src "/topics/" (:id t) ".edn")]
      (when (.exists (java.io.File. f))
        (sort-by #(or (:date %) "9999") (:moments (edn/read-string (slurp f))))))))
(defn source-of
  "The instance or document a moment came from, its where line without the date."
  [m]
  (-> (tidy (:where m)) (s/replace #"\s*·\s*\d{4}-\d{2}-\d{2}\s*$" "") (s/replace #"\s*·\s*$" "")))
(defn mentions-html [name]
  (let [ms (feature-moments name)
        by-source (sort-by (comp #(or (:date %) "9999") first val) (group-by source-of ms))]
    (when (seq ms)
      (str "<details class=\"mentions\"><summary>Every time I spoke of it, " (count ms) " moments in "
           (count by-source) " places</summary><ul>\n"
           (apply str (for [[src ms] by-source]
                        (str "<li><span class=\"where\">" (esc src) "</span> "
                             (s/join ", " (map #(or (:date %) "undated") ms)) "</li>\n")))
           "</ul></details>\n"))))
(defn connected-html
  "Up to three features this one's own post names as connected, in the order its prose links them."
  [name]
  (let [t (topic-by-title (feature-alias name name))
        f (str here "/prose/" (:id t) ".edn")
        ids (when (.exists (java.io.File. f))
              (->> (re-seq #"\[\[t:([a-z0-9-]+)\]\]" (slurp f)) (map second) distinct
                   (remove #{(:id t)}) (take 3)))
        by-id (into {} (map (juxt :id identity) topics))]
    (when (seq ids)
      (str "<p class=\"connected\"><span>Connected to</span>"
           (s/join "" (for [id ids :let [ct (by-id id)] :when ct]
                        (str "<span class=\"c\">" (if (written? ct) (str "<a href=\"" id "/index.html\">" (esc (:title ct)) "</a>") (esc (:title ct))) "</span>")))
           "</p>\n"))))

(defn features-html []
  (apply str
         (for [[i {:keys [era features]}] (map-indexed vector eras)]
           (str "<h3 id=\"era-" i "\">" (esc era) "</h3>\n"
                (apply str
                       (for [f features :let [{w :when q :quote m :moved} (feature-parts f)]]
                         (str "<div class=\"feature\"><h4>" (feature-link (:name f)) "</h4>\n"
                              (when (seq w) (str "<p class=\"meta\">" (esc w) "</p>\n"))
                              (when q (str "<blockquote>" (esc q) "</blockquote>\n"))
                              (when-let [y (feature-why (:name f))] (str "<p class=\"why\">" (esc y) "</p>\n"))
                              (when (seq m) (str "<p>" (esc m) "</p>\n"))
                              (mentions-html (:name f))
                              (connected-html (:name f))
                              "</div>\n")))))))

;; ---------------------------------------------------------------- the pillars
(def by-id (into {} (map (juxt :id identity) events)))
(defn beside-counts [section ids]
  (->> ids (map by-id) (mapcat :said-beside) (remove #{section}) frequencies (sort-by (comp - val)) (take 3)))

(defn section-html [region thread sec]
  (let [name (:pillar sec) t (topic-of name) ids (:events sec)
        evs (keep by-id ids) dated (sort (keep :date evs))
        f (first-of name)]
    (str "<details class=\"more\" id=\"" (anchor name) "\"><summary><span>" (esc name)
         "<small class=\"meta\">" (if (:first-date sec) (str "first said " (:first-date sec)) "not yet said in a dated source")
         " · " (count ids) " moments · " (:quotes sec) " quotes</small></span></summary><div class=\"body\">\n"
         (if f
           (str "<p>First said on " (:date f) ", in " (esc (tidy (get-in f [:source :where]))) ".</p>\n"
                "<blockquote>" (esc (cut (first (s/split (str (first (:quotes f))) #"\s*—")) 320)) "</blockquote>\n")
           "<p>THE MAP has this section and no dated words of mine on it were found yet.</p>\n")
         (when (seq dated) (str "<p>Spoken of from " (first dated) " to " (last dated) ".</p>\n"))
         (let [bs (beside-counts name ids)]
           (when (seq bs)
             (str "<p>Most often spoken of beside "
                  (s/join ", " (for [[o n] bs] (str "<a href=\"#" (anchor o) "\">" (esc o) "</a> (" n ")")))
                  ".</p>\n")))
         (when t (str "<p class=\"order\">Its post is " (:order t) " of " (count topics) " in the order of writing"
                      (when (written? t) (str ", and <a href=\"" (:id t) "/index.html\">its post is written</a>")) ".</p>\n"))
         "</div></details>\n")))

(defn pillars-html []
  (apply str
         (for [[ri r] (map-indexed vector pillars)]
           (str "<h3 id=\"r-" ri "\" class=\"region r" ri "\">" (esc (:pillar r)) "</h3>\n"
                (apply str
                       (for [t (:threads r)]
                         (str "<p class=\"thread r" ri "\">" (esc (:pillar t)) "</p>\n"
                              (apply str (map #(section-html r t %) (sort-by #(or (:first-date %) "9999") (:sections t)))))))))))

(defn order-html []
  (str "<ol class=\"order-list\">\n"
       (apply str (for [t topics]
                    (str "<li>" (if (written? t) (str "<a href=\"" (:id t) "/index.html\">" (esc (:title t)) "</a>") (esc (:title t))) " <span class=\"meta\">"
                         (or (:first-date t) "undated") " · "
                         (case (:status t) :tested "written and tested" :drafted "drafted" "to be written") "</span></li>\n")))
       "</ol>\n"))

;; ---------------------------------------------------------------- data.js
(def thread-list (vec (for [[ri r] (map-indexed vector pillars) t (:threads r)] {:name (:pillar t) :region ri :sections (set (map :pillar (:sections t)))})))
(defn thread-of [section] (first (keep-indexed (fn [i t] (when ((:sections t) section) i)) thread-list)))

(def data
  {:threads (mapv #(select-keys % [:name :region]) thread-list)
   :events (vec (for [e said :let [ti (thread-of (:section e))] :when (and ti (:date e))]
                  {:d (:date e) :t ti :s (:section e) :q (count (:quotes e)) :f (boolean (:first-of-section e))
                   :w (tidy (get-in e [:source :where])) :x (cut (first (:quotes e)) 180) :a (anchor (:section e))}))
   :built (vec (for [b built] {:d (:date b) :n (count (:commits b)) :pub (public? b) :subj (cut (:subject (first (:commits b))) 120)}))
   :folders (vec (for [f folders] {:d (:date f) :name (s/replace (:title f) #"^Project begun, " "")}))
   :tree (vec (for [[ri r] (map-indexed vector pillars)]
                {:name (:pillar r) :ri ri
                 :children (vec (for [t (:threads r)]
                                  {:name (:pillar t)
                                   :children (vec (for [sec (:sections t)]
                                                    {:name (:pillar sec) :q (:quotes sec) :first (:first-date sec) :a (anchor (:pillar sec))}))}))}))})

;; ---------------------------------------------------------------- the page
(def title "The History of the Smile Prompt Language, a Timeline of Every Idea from 2023 to Now")
(def desc (str "Every idea in the Smile Prompt Language dated to the conversation, document or commit where it first appeared, from ChatGPT conversations of October 2023 to October 2026, nested as " (N "regions") " regions, " (N "threads") " threads and " (N "sections") " sections, each the subject of a post to come."))

(defn buddha-eyes []
  (-> (re-find #"(?s)<a class=\"buddha-eyes\".*?</a>" (slurp "C:/Users/hanjo/Claude/Projects/Blog Template/sample.html"))
      (s/replace "bottom:11px" "bottom:66px")))

(defn page []
  (reset! notes [])
  (let [era-html (features-html)
        faq [["When was the Smile Prompt Language created?"
              (str "My first words toward it are in two ChatGPT conversations of 3 October 2023, asking for a language a model reads and writes in, clearly labelled, and a prompt that describes itself. I shared the first version on Discord on 3 July 2025, and the public repository on GitHub began on 11 July 2025.")]
             ["What is Smile?"
              "Smile is a prompt language built from nested emoticons. The faces are the delimiters that open and close each section, and their features are the syntax."]
             ["How many ideas make up Smile?"
              (str (N "sections") " sections of THE MAP, gathered into " (N "threads") " threads inside " (N "regions") " regions. Each section will be the subject of its own post.")]
             ["Where do the dates come from?"
              (str "From " (N "quotes") " quotes of mine across " (N "said") " moments, each found character for character in its conversation, document or recording, and from " (N "public-commits") " commits to the public repository and " (N "pc-commits") " to the repository on my PC.")]]
        words (count (re-seq #"\w+" (-> (str era-html " " (s/join " " (map second faq))) (s/replace #"(?s)<details class=\"mentions\">.*?</details>" " ") (s/replace #"<[^>]+>" " "))))]
    (str "<!doctype html>
<html lang=\"en\">
<head>
<meta charset=\"utf-8\">
<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">
<title>" (esc title) "</title>
<meta name=\"description\" content=\"" (esc desc) "\">
<meta name=\"keywords\" content=\"history of the Smile prompt language, Smile prompt language timeline, when was Smile created, emoticon delimiters for prompts, prompt language development history, THE MAP of Smile, Dr Thomas Ager prompt engineering, modular prompt composition history\">
<meta name=\"author\" content=\"Dr Thomas Ager\">
<meta property=\"og:type\" content=\"article\">
<meta property=\"og:title\" content=\"" (esc title) "\">
<meta property=\"og:description\" content=\"" (esc desc) "\">
<link rel=\"preconnect\" href=\"https://fonts.googleapis.com\">
<link rel=\"preconnect\" href=\"https://fonts.gstatic.com\" crossorigin>
<link href=\"https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght,SOFT@0,9..144,300..700,0..100;1,9..144,300..700,0..100&family=Newsreader:ital,opsz,wght@0,6..72,300..600;1,6..72,300..600&family=Inter:wght@400;500;600;700&family=JetBrains+Mono&display=swap\" rel=\"stylesheet\">
<link rel=\"stylesheet\" href=\"../../../Blog Template/blog.css\">
<style>
  .r0{color:var(--hue-1)} .r1{color:var(--hue-2)} .r2{color:var(--hue-3)} .r3{color:var(--hue-4)} .r4{color:var(--ink-2)}
  h3.region{margin-top:var(--sp4)}
  p.thread{font:600 var(--s-1)/1.4 var(--sans);letter-spacing:.08em;text-transform:uppercase;margin:var(--sp3) 0 var(--sp1)}
  details.more summary small.meta{display:block;font:400 var(--s-1)/1.4 var(--sans);color:var(--ink-2);margin-top:4px}
  .meta{font:400 var(--s-1)/1.4 var(--sans);color:var(--ink-2)}
  details.more .body blockquote{font-style:italic;margin:var(--sp2) 0;padding-left:var(--sp2);border-left:2px solid var(--rule)}
  ol.order-list li{margin:6px 0}
  .feature .why{font:400 var(--s0)/1.55 var(--serif);color:var(--ink-2)} .feature details.mentions{margin:var(--sp1) 0;font:400 var(--s-1)/1.5 var(--sans)} .feature details.mentions summary{cursor:pointer;color:var(--ink-2)} .feature details.mentions ul{margin:6px 0 0;padding-left:18px} .feature details.mentions .where{color:var(--ink)} .feature p.connected{display:flex;flex-wrap:wrap;gap:8px 14px;margin:var(--sp1) 0 0;padding-top:8px;border-top:1px solid var(--rule);font:400 var(--s-1)/1.4 var(--sans)} .feature p.connected>span:first-child{color:var(--ink-2);text-transform:uppercase;letter-spacing:.06em} .feature p.connected small{color:var(--ink-2)}
  .feature{margin:0 0 var(--sp3)} .feature h4{margin:var(--sp3) 0 4px} .feature blockquote{font-style:italic;margin:var(--sp1) 0;padding-left:var(--sp2);border-left:2px solid var(--rule)}
  .authorship{font:italic 400 var(--s0)/1.4 var(--serif);color:var(--ink-2);margin:-8px 0 var(--sp2)}
  .h-tip{position:fixed;z-index:2147483647;max-width:340px;padding:10px 12px;background:var(--paper);color:var(--ink);border:1px solid var(--rule);border-radius:8px;box-shadow:0 6px 24px rgba(0,0,0,.12);font:400 13px/1.45 var(--sans);pointer-events:none}
  .h-tip b{display:block;font-weight:600;margin-bottom:2px}
  .h-tip span{display:block;color:var(--ink-2)}
  .h-tip q{display:block;margin-top:6px;font:italic 400 14px/1.45 var(--serif);color:var(--ink)}
  figure .slot svg{width:100%;height:auto;display:block}
</style>
<script type=\"application/ld+json\">
" (json/generate-string
   {"@context" "https://schema.org"
    "@graph" [{"@type" "BlogPosting" "headline" title "description" desc
               "author" {"@type" "Person" "name" "Dr Thomas Ager" "url" "https://github.com/DrThomasAger"}
               "datePublished" "2026-10-18" "inLanguage" "en"
               "about" ["Smile Prompt Language" "prompt engineering" "prompt languages" "history of software"]
               "isBasedOn" "https://github.com/DrThomasAger/smile"}
              {"@type" "FAQPage" "mainEntity" (for [[q a] faq] {"@type" "Question" "name" q "acceptedAnswer" {"@type" "Answer" "text" a}})}
              {"@type" "ItemList" "name" "The posts of the history of Smile, in the order of writing"
               "itemListElement" (for [t topics] {"@type" "ListItem" "position" (:order t) "name" (:title t)})}
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
<h1>" (esc title) "</h1>
<p class=\"lede\">Every idea in Smile, dated to the conversation, document or commit where it first appeared, and nested as the pillars the posts of this history will follow.</p>
<div class=\"byline\"><span class=\"who\">Dr Thomas Ager</span><span class=\"dot\"></span><span>18 October 2026</span><span class=\"dot\"></span><span>" (max 1 (Math/round (/ words 230.0))) " min read</span></div>
<p class=\"authorship\">(claude wrote this for me)</p>

<nav class=\"toc\" aria-label=\"Contents\"><div class=\"label\">Contents</div>
<ol><li><a href=\"#eras\">The features, asked for and built</a></li><li><a href=\"#chains\">What is built, and what each feature rests on</a></li><li><a href=\"#timeline\">Every moment, on one line</a></li><li><a href=\"#parts\">Every asking and every commit</a></li><li><a href=\"#pillars\">The pillars, one inside another</a></li><li><a href=\"#order\">The order of the posts</a></li><li><a href=\"#made\">How this timeline was made</a></li><li><a href=\"#faq\">Questions</a></li></ol></nav>

<p class=\"drop illuminated\" data-symbol=\"smile\" data-hue=\"3\" data-seed=\"the-history-of-smile\">This page is the map of a series. Smile, the prompt language whose sections open and close with faces, grew over three years across ChatGPT conversations, Discord messages, Google documents, Claude conversations, two repositories and many Claude Code sessions. Here each of its ideas is dated to the first place it was spoken of, and placed inside the pillar it belongs to. Every idea below will become its own post, written from every word I said about it, in the order the ideas first appeared. The features I asked for and the day each was built come first, era by era, then every moment on one line, and then every asking and commit part by part.</p>

<h2 id=\"eras\">The features, asked for and built</h2>
<p>Era by era, each feature of Smile with the first words in which I asked for it, kept exactly, where I said them, then what was built from it and on which day, and how its meaning moved. Each feature opens its own post. A few are not yet built, and say so.</p>
" era-html "
<h2 id=\"chains\">What is built, and what each feature rests on</h2>
<p>Figure 1 draws every feature of THE MAP that has a build state. A feature hangs below the features its own section in THE MAP names, so each chain runs from what a feature is made of down to what is made from it, and a link already implied by a longer chain is left out. Its bar counts its amendments, green for built, blue for part built and grey for not yet built, from the Map session's reading of every amendment against the code. No feature is complete yet. Hover or tap a feature for its counts and what is missing, and press it to open its post.</p>
<figure class=\"bleed chains\"><figcaption><b>Figure 1</b>Every feature with a build state, chained to the features it rests on, with its amendments built, part built and not yet built.</figcaption><div class=\"slot\">" (slurp (str here "/chains-figure.html")) "</div></figure>

<h2 id=\"timeline\">Every moment, on one line</h2>
<p>Each dot is one moment, one idea spoken of in one conversation, document or recording. The lanes are the threads of the pillars, coloured by their region. A ringed dot is the first time an idea was said. The lower lanes are the days of commits and the days new project folders began. Hover or tap a dot to read the words, and press it to open that idea below.</p>
<figure class=\"bleed reveal\" data-diagram=\"timeline\"><figcaption><b>Figure 2</b>" (N "said") " moments of " (N "sections") " ideas, " (N "public-commits") " public commits and " (N "pc-commits") " on my PC, from October 2023 to October 2026.</figcaption></figure>

<h2 id=\"parts\">Every asking and every commit, part by part</h2>
<p>From 22 July 2026, when Smile's work moved into Claude Code and every chat began to be harvested, each thing I asked for can be set beside the commits that built it. Figure 3 gives each part of Smile its own lane. A blue dot is something I asked for, a green square a commit that built it, and a rose cross something delivered otherwise than asked. Hover or tap a mark to read it.</p>
<figure class=\"bleed reveal\" data-diagram=\"f\"><figcaption><b>Figure 3</b>One lane for each part of Smile, July to October 2026, my askings beside the commits that built them.</figcaption></figure>
<h2 id=\"pillars\">The pillars, one inside another</h2>
<p>The pillars are THE MAP's own. " (N "regions") " regions contain " (N "threads") " threads, and the threads contain the " (N "sections") " sections of THE MAP, each a single idea of Smile. Figure 4 draws them packed inside one another, each section sized by how many times I spoke of it. Each section below opens to where it was first said, the ideas it was most often spoken of beside, and its place in the order of posts.</p>
<figure class=\"reveal\" data-diagram=\"pack\"><figcaption><b>Figure 4</b>The regions, threads and sections of Smile, each section's circle sized by my quotes on it. Press a section to open it below.</figcaption></figure>
" (pillars-html) "
<h2 id=\"order\">The order of the posts</h2>
<p>The posts follow the order in which each idea first appeared, so the series unfolds the way Smile did, from raw text in 2023 to the Sangha's energetic structure in 2026.</p>
" (order-html) "
<h2 id=\"made\">How this timeline was made</h2>
<p>Every quote here was found character for character in its source by the reading kept in Every word of his on Smile, " (N "quotes") " quotes in " (N "said") " moments, each placed under a section of THE MAP. The dates come from the source line itself, from the date Ekadanta keeps for the record, or, for " (N "undated") " moments, are not yet known. Commits come from the public repository on GitHub and from the Smile repository on my PC. A second Claude instance gathered and dated the events while this one wrote the page, and the page is rebuilt from that gathering by one Babashka script, so it grows as the gathering does.</p>

<h2 id=\"faq\" class=\"faq\">Questions</h2>
" (apply str (for [[q a] faq] (str "<h3>" (esc q) "</h3>\n<p>" (esc a) "</p>\n"))) "
<h3>Sources</h3>
<ol class=\"sources\">
<li>The Smile Development Timeline, C:\\Users\\hanjo\\Claude\\Projects\\Smile\\Smile Development Timeline, its events.edn, pillars.edn and topics.edn.</li>
<li>Every word of his on Smile, C:\\Users\\hanjo\\Claude\\Projects\\Smile\\Smile Prompt Language\\Every word of his on Smile.</li>
<li>THE MAP, C:\\Users\\hanjo\\Claude\\Projects\\Smile\\Smile Prompt Language\\THE MAP.md.</li>
<li>The public Smile repository, <a href=\"https://github.com/DrThomasAger/smile\">https://github.com/DrThomasAger/smile</a>.</li>
<li>Bostock, M. <a href=\"https://observablehq.com/@d3/pack\">Circle packing</a>, the method of Figure 4.</li>
</ol>
</article>
</div>
<div class=\"toolbar\"><button id=\"restore\" type=\"button\" hidden>Restore removed</button><button id=\"theme\" type=\"button\">☾ Night</button></div>
<script src=\"https://cdn.jsdelivr.net/npm/d3@7.9.0\"></script>
<script src=\"data.js\"></script>
<script src=\"timeline.js\"></script>
<script src=\"features-data.js\"></script>
<script src=\"features.js\"></script>
<script src=\"../../../Blog Template/blog.js\"></script>
<script src=\"../../../Blog Template/initial.js\"></script>
<script>
  const draw = el => { el.querySelectorAll('.slot').forEach(s => s.remove())
    const slot = document.createElement('div'); slot.className = 'slot'; el.prepend(slot)
    const fig = el.dataset.diagram === 'f' ? FD.draw : HD[el.dataset.diagram]; fig(slot) }
  const all = () => document.querySelectorAll('[data-diagram]').forEach(draw)
  all()
  document.addEventListener('blog:theme', all)
  let w = innerWidth; addEventListener('resize', () => { if ((w < 600) !== (innerWidth < 600)) all(); w = innerWidth })
</script>
" (buddha-eyes) "
</body>
</html>
")))

(defn -main []
  (let [html (page)]
    (spit (str here "/data.js") (str "window.H = " (json/generate-string data) "\n"))
    (spit (str here "/index.html") html)
    (println "index.html" (count html) "chars," (count @notes) "sidenotes," (count (:events data)) "dots")
    (println N)))

(when (= *file* (System/getProperty "babashka.file")) (-main))
