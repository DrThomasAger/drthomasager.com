;; bb chains.clj, from this folder. Writes chains-figure.html, the figure of every
;; feature of THE MAP that has a build state, coloured by how much of it is built,
;; and chained to the features it depends on.
;; A feature depends on an earlier feature of THE MAP when its section names it.
;; The chains are the transitive reduction of that, so A to B to C is drawn without A to C.
;; Built, part built and not built counts are the Map session's reading of every
;; amendment against the code, in build state by section.json.
(require '[clojure.string :as s] '[cheshire.core :as j] '[clojure.edn :as edn] '[babashka.fs :as fs])
(def map-file "C:/Users/hanjo/Claude/Projects/Smile/Smile Prompt Language/THE MAP.md")
(def state-file "C:/Users/hanjo/Claude/Projects/Smile/Smile Prompt Language/THE MAP with his amendments/build state by section.json")
(def here (str (fs/parent (fs/absolutize *file*))))
(def topics (edn/read-string (slurp "C:/Users/hanjo/Claude/Projects/Smile/Smile Development Timeline/topics.edn")))
(def written (set (for [t topics :when (and (= :tested (:status t)) (fs/exists? (str here "/" (:id t) "/index.html")))] (:id t))))
(def title-of (into {} (map (juxt :id :title) topics)))

(def mp (s/replace (slurp map-file) "\r" ""))
(def bs (j/parse-string (slurp state-file)))
(def slug-of (into {} (for [[k v] bs] [(get v "section") k])))
(def nodes
  (vec (keep (fn [p] (let [[h & body] (s/split-lines p)
                           nm (s/trim (s/replace h #"\s*\(.*$" ""))
                           k (or (slug-of nm) (slug-of (s/trim h)))]
                       (when k {:slug k :name nm :body (s/join "\n" body)})))
             (rest (s/split mp #"(?m)^# ")))))
(defn names? [body nm] (re-find (re-pattern (str "(?i)\\b" (java.util.regex.Pattern/quote (s/lower-case nm)) "(e?s)?\\b")) body))
;; deps: slug -> set of earlier slugs its section names
(def deps (into {} (for [[i a] (map-indexed vector nodes)]
                     [(:slug a) (set (for [b (take i nodes) :when (names? (:body a) (:name b))] (:slug b)))])))
(defn reach [x] (loop [seen #{} todo (vec (deps x))]
                  (if-let [y (peek todo)] (if (seen y) (recur seen (pop todo)) (recur (conj seen y) (into (pop todo) (deps y)))) seen)))
;; transitive reduction, keep b in deps a only when no other dep of a reaches b
(def chain (into {} (for [[a ds] deps] [a (set (remove (fn [b] (some #(contains? (reach %) b) (disj ds b))) ds))])))
(def depth (memoize (fn d [x] (if (empty? (chain x)) 0 (inc (apply max (map d (chain x))))))))
(def kids (reduce (fn [m [a ds]] (reduce #(update %1 %2 (fnil conj #{}) a) m ds)) {} chain))
(def alone (set (for [n nodes :let [k (:slug n)] :when (and (empty? (chain k)) (empty? (kids k)))] k)))

(def cols (group-by depth (remove alone (map :slug nodes))))
(def ncol (inc (apply max (keys cols))))
;; order each column by the mean row of its parents, so chains run straight
(def rows
  (loop [c 0 pos {}]
    (if (= c ncol) pos
        (let [col (cols c)
              key (fn [k] (if-let [ps (seq (keep pos (chain k)))] (/ (reduce + ps) (count ps)) (* 1000 (- (count (kids k))))))
              sorted (sort-by key col)]
          (recur (inc c) (merge pos (zipmap sorted (range))))))))
(def W 182) (def H 96) (def bw 168) (def bh 52) (def pad 12)
(def maxrows (apply max (map count (vals cols))))
(defn xy [k] [(+ pad (* W (rows k))) (+ pad (* H (depth k)))])
(defn esc [t] (-> (str t) (s/replace "&" "&amp;") (s/replace "<" "&lt;") (s/replace ">" "&gt;") (s/replace "\"" "&quot;")))
(defn counts [k] (let [v (bs k)] (mapv #(or (get v %) 0) ["built" "part built" "not built"])))
(defn node [k [x y]]
  (let [[b p n] (counts k) tot (max 1 (+ b p n)) iw (- bw 20)
        wb (* iw (/ b tot)) wp (* iw (/ p tot))
        nm (get-in bs [k "section"])
        tip (str nm ", " b " built, " p " part built, " n " not yet built" (when-let [su (get-in bs [k "summary"])] (str ". " su)))
        body (str "<rect class=\"ch-box\" x=\"" x "\" y=\"" y "\" width=\"" bw "\" height=\"" bh "\" rx=\"7\"/>"
                  "<text class=\"ch-name\" x=\"" (+ x 10) "\" y=\"" (+ y 23) "\"" (when (> (count nm) 17) (str " textLength=\"" (- bw 20) "\" lengthAdjust=\"spacingAndGlyphs\"")) ">" (esc nm) "</text>"
                  "<rect class=\"ch-not\" x=\"" (+ x 10) "\" y=\"" (+ y 34) "\" width=\"" iw "\" height=\"9\" rx=\"4.5\"/>"
                  (when (pos? p) (str "<rect class=\"ch-part\" x=\"" (format "%.1f" (double (+ x 10 wb))) "\" y=\"" (+ y 34) "\" width=\"" (format "%.1f" (double wp)) "\" height=\"9\"/>"))
                  (when (pos? b) (str "<rect class=\"ch-built\" x=\"" (+ x 10) "\" y=\"" (+ y 34) "\" width=\"" (format "%.1f" (double wb)) "\" height=\"9\" rx=\"4.5\"/>")))]
    (str "<g class=\"ch-node\" tabindex=\"0\" data-tip=\"" (esc tip) "\">"
         (if (written k) (str "<a href=\"" k "/index.html\">" body "</a>") body) "</g>\n")))
(defn edge [a b]
  (let [[x1 y1] (xy b) [x2 y2] (xy a) x1 (+ x1 (/ bw 2)) y1 (+ y1 bh) x2 (+ x2 (/ bw 2)) m (/ (+ y1 y2) 2)]
    (str "<path class=\"ch-edge\" d=\"M" x1 " " y1 " C" x1 " " m " " x2 " " m " " x2 " " y2 "\"/>\n")))
(def alone-y (+ pad (* H ncol) 34))
(def alone-list (sort-by #(get-in bs [% "section"]) alone))
(def per-row (max 1 maxrows))
(def alone-xy (into {} (map-indexed (fn [i k] [k [(+ pad (* W (mod i per-row))) (+ alone-y (* H (quot i per-row)))]]) alone-list)))
(def height (+ (if (seq alone) (+ alone-y (* H (inc (quot (dec (count alone)) per-row)))) (+ pad (* H ncol))) pad))
(def width (+ pad (* W maxrows)))
(def built-total (reduce + (map #(first (counts %)) (keys bs))))
(def style
  (str "<style>"
       "figure.chains .slot{overflow-x:auto;-webkit-overflow-scrolling:touch}"
       "figure.chains .slot svg{min-width:760px}"
       ".ch-edge{fill:none;stroke:var(--ink-2);stroke-opacity:.38;stroke-width:1.3}"
       ".ch-box{fill:var(--paper);stroke:var(--rule);stroke-width:1.2}"
       ".ch-node a:hover .ch-box,.ch-node a:focus .ch-box{stroke:var(--accent);stroke-width:1.8}"
       ".ch-node a{text-decoration:none}.ch-name{font:500 17px var(--sans);fill:var(--ink)}"
       ".ch-head{font:500 17px var(--sans);fill:var(--ink-2)}"
       ".ch-not{fill:var(--rule)}"
       ".ch-part{fill:var(--hue-1);fill-opacity:.45}"
       ".ch-built{fill:var(--hue-4)}"
       "</style>\n"))
(def svg
  (str style "<svg viewBox=\"0 0 " width " " height "\" role=\"img\" aria-label=\"Every feature of THE MAP with a build state, chained to the features it depends on, each with a bar of its amendments built, part built and not yet built\">\n"
       (apply str (for [[a ds] chain :when (not (alone a)) b ds] (edge a b)))
       (apply str (for [k (remove alone (map :slug nodes))] (node k (xy k))))
       (when (seq alone)
         (str "<text class=\"ch-head\" x=\"" pad "\" y=\"" (- alone-y 12) "\">Features that name no other and are named by none</text>\n"
              (apply str (for [k alone-list] (node k (alone-xy k))))))
       "</svg>\n"
       ;; the hover text lives in data-tip, shown in the page's own .h-tip, so it is read on hover and not counted as prose
       "<script>(()=>{const t=document.createElement('div');t.className='h-tip';t.hidden=true;document.body.appendChild(t);"
       "const show=(g,x,y)=>{t.textContent=g.dataset.tip;t.hidden=false;const r=t.getBoundingClientRect();"
       "t.style.left=Math.min(x+14,innerWidth-r.width-8)+'px';t.style.top=Math.min(y+14,innerHeight-r.height-8)+'px'};"
       "document.querySelectorAll('.ch-node').forEach(g=>{g.addEventListener('pointerenter',e=>show(g,e.clientX,e.clientY));"
       "g.addEventListener('pointermove',e=>show(g,e.clientX,e.clientY));g.addEventListener('pointerleave',()=>t.hidden=true);"
       "g.addEventListener('focus',()=>{const r=g.getBoundingClientRect();show(g,r.left,r.bottom)});g.addEventListener('blur',()=>t.hidden=true)})})()</script>"))
(spit (str here "/chains-figure.html") svg)
(prn {:features (count nodes) :chained (- (count nodes) (count alone)) :alone (count alone) :links (reduce + (map count (vals chain))) :columns ncol :rows maxrows})
