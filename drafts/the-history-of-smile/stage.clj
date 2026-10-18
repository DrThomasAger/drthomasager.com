;; bb stage.clj, from this folder. Writes publish\history-of-smile\, the whole
;; series as the site will serve it, with the Blog Template's blog.css and blog.js
;; copied into it and every relative link to them rewritten, so the folder can be
;; copied whole into C:\Users\hanjo\Claude\Projects\DrThomasAger\site\ and pushed.
;; It also writes publish\sitemap-rows.xml, the <url> rows for the series.
;; Nothing here touches posts\ or atom.xml, so the Mailing Steward never sees it.
(require '[babashka.fs :as fs] '[clojure.string :as str] '[clojure.edn :as edn])
(def here (str (fs/parent (fs/absolutize *file*))))
(def out (str here "/publish/history-of-smile"))
(def template "C:/Users/hanjo/Claude/Projects/Blog Template")
(def site-url "https://drthomasager.github.io/drthomasager.com/history-of-smile/")
(def topics (sort-by :order (edn/read-string (slurp "C:/Users/hanjo/Claude/Projects/Smile/Smile Development Timeline/topics.edn"))))

;; bb stage.clj YYYY-MM-DD stages only what smile-96's release-schedule.edn
;; releases by that day, one post a day, and points every link to a post not
;; yet released at its place in the timeline instead. With no date, all of it.
(def schedule (edn/read-string (slurp "C:/Users/hanjo/Claude/Projects/Smile/Smile Development Timeline/release-schedule.edn")))
(def cutoff (first *command-line-args*))
(def released (set (keep #(when (and (:topic %) (or (nil? cutoff) (<= (compare (:day %) cutoff) 0))) (:topic %)) schedule)))
(def unreleased (remove released (map :id topics)))
(defn unlink [html prefix anchor-prefix]
  (reduce (fn [h id] (str/replace h (str "href=\"" prefix id "/index.html\"") (str "href=\"" anchor-prefix id "\""))) html unreleased))
(when (fs/exists? out) (fs/delete-tree out))
(fs/create-dirs (str out "/blog"))
(doseq [f ["blog.css" "blog.js"]] (fs/copy (str template "/" f) (str out "/blog/" f)))
(doseq [f ["timeline.js" "topic.js" "history.css" "data.js"]] (fs/copy (str here "/" f) (str out "/" f)))
(spit (str out "/index.html")
      (-> (slurp (str here "/index.html")) (str/replace "../../../Blog Template/" "blog/") (unlink "" "#s-")))
(def ids (keep #(when (and (released (:id %)) (fs/exists? (str here "/" (:id %) "/index.html"))) (:id %)) topics))
(doseq [id ids]
  (fs/create-dirs (str out "/" id))
  (fs/copy (str here "/" id "/data.js") (str out "/" id "/data.js"))
  (spit (str out "/" id "/index.html")
        (-> (slurp (str here "/" id "/index.html")) (str/replace "../../../../Blog Template/" "../blog/") (unlink "../" "../index.html#s-"))))
(spit (str here "/publish/sitemap-rows.xml")
      (apply str (for [p (cons "" (map #(str % "/") ids))]
                   (str "<url><loc>" site-url p "</loc><lastmod>2026-10-18</lastmod></url>\n"))))
(let [left (for [f (fs/glob out "**.html") :let [t (slurp (str f))] :when (str/includes? t "Blog Template")] (str f))]
  (println "staged" (inc (count ids)) "pages into" out)
  (println "pages still linking outside the folder" (count left)))
