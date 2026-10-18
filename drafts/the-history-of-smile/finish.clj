;; bb finish.clj <topic-id>, from this folder. Builds the post and the one
;; before it (so its next link is live), runs smile-96's post_check on it, takes
;; the shots at 390 and 1440, and when every quote is found, every id held,
;; every moment cited and nothing is wider than the page, marks the topic
;; :tested in topics.edn and rebuilds the timeline post.
(require '[babashka.process :as p] '[clojure.edn :as edn] '[clojure.string :as str])
(def id (first *command-line-args*))
;; bb finish.clj <id> quick, builds and checks the post alone, no shots, no timeline rebuild
(def quick? (= "quick" (second *command-line-args*)))
(def tl "C:/Users/hanjo/Claude/Projects/Smile/Smile Development Timeline")
(def built? (str/starts-with? id "built-"))
(def tool (if built? "project.clj" "topic.clj"))
(def order (mapv :id (sort-by :order (edn/read-string (slurp (str tl (if built? "/built-topics.edn" "/topics.edn")))))))
(def prev (let [i (.indexOf order id)] (when (pos? i) (order (dec i)))))
(defn sh [opts & args] (let [r @(p/process (vec args) (merge {:out :string :err :string} opts))] (when (pos? (:exit r)) (println (:err r))) (:out r)))
(print (sh {} "bb" tool id))
(when (and (not quick?) prev (babashka.fs/exists? (str (if built? "prose-built/" "prose/") prev ".edn"))) (sh {} "bb" tool prev))
(def check (edn/read-string (sh {:dir tl} "bb" "post_check.clj" (str (babashka.fs/absolutize (str id "/index.html"))) id)))
(prn (select-keys check [:passages :not-found :ids-named :ids-unknown :uncited]))
(def shots (if quick? "\"wide\":[] \"wide\":[]" (sh {} "bb" "shots.clj" (str id "/index.html"))))
(print shots)
(if (and (empty? (:not-found check)) (empty? (:ids-unknown check)) (empty? (:uncited check))
         (= 2 (count (re-seq #"\"wide\":\[\]" shots))))
  (do (print (sh {} "bb" tool "mark" id "tested")) (when-not quick? (print (sh {} "bb" "build.clj"))) (println "PASSES"))
  (do (print (sh {} "bb" tool "mark" id "drafted")) (println "DIFFERS")))
