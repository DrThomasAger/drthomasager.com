;; bb release.clj [YYYY-MM-DD], from this folder. The day's release of the
;; history of Smile. Stages what smile-96's release-schedule.edn releases by that
;; day (today when no date is given), copies it into site\history-of-smile\,
;; commits only that folder and build.py, and pushes, which publishes it about 33
;; seconds later. Nothing here touches posts\ or atom.xml, so nothing is mailed.
;; It is run by hand each day, as nothing that reaches the internet starts itself.
(require '[babashka.process :as p] '[babashka.fs :as fs] '[clojure.edn :as edn])
(def day (or (first *command-line-args*) (str (java.time.LocalDate/now))))
(def repo "C:/Users/hanjo/Claude/Projects/DrThomasAger")
(def schedule (edn/read-string (slurp "C:/Users/hanjo/Claude/Projects/Smile/Smile Development Timeline/release-schedule.edn")))
(def todays (first (filter #(= day (:day %)) schedule)))
(defn sh [& args] (let [r @(p/process (vec args) {:dir repo :out :string :err :string})] (print (:out r) (:err r)) r))
(when-not todays (println "nothing is scheduled for" day) (System/exit 0))
(when (fs/exists? (str (fs/parent (fs/absolutize *file*)) "/HOLD.txt")) (println (slurp (str (fs/parent (fs/absolutize *file*)) "/HOLD.txt"))) (System/exit 0))
@(p/process ["bb" "stage.clj" day] {:inherit true})
(fs/delete-tree (str repo "/site/history-of-smile"))
(fs/copy-tree (str (fs/parent (fs/absolutize *file*)) "/publish/history-of-smile") (str repo "/site/history-of-smile"))
(sh "git" "add" "site/history-of-smile" "build.py")
(sh "git" "commit" "-m" (str "The history of Smile, " (:title todays) ", released " day "\n\nCo-Authored-By: Claude Opus 5.5 (1M context) <noreply@anthropic.com>"))
(sh "git" "push" "origin" "main")
(println "released" (:title todays) "for" day)
