;; bb shots.clj, from this folder. The page through frame.html at 1440 and at
;; 390 wide (a headless Edge window is never narrower than about 500), at the
;; top, at the pillars with one section opened, and at the order of posts,
;; into shots\, and the phone check printed, its scroll width against 390.
(require '[babashka.process :as p] '[babashka.fs :as fs] '[clojure.string :as str])
(def edge "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe")
(def frame (str "file:///" (str/replace (str (fs/absolutize "frame.html")) "\\" "/")))
(def src (or (first *command-line-args*) "index.html"))
(def tag (if (= src "index.html") "" (str (first (str/split src #"/")) "-")))
(fs/create-dirs "shots")
(defn edge! [& args] (:out @(p/process (into [edge "--headless=new" "--disable-gpu" "--hide-scrollbars" "--force-device-scale-factor=1" "--allow-file-access-from-files" "--virtual-time-budget=9000"] args) {:out :string :err :string})))
(doseq [[w h] [[1440 2000] [390 2000]] [nm q] (remove nil? [["top" ""] ["pillars" "&at=pillars"] ["lower" (if (= src "index.html") "&at=order" "&at=moments")] (when (= src "index.html") ["eras" "&at=era-1"])])]
  (edge! (str "--window-size=" (max w 600) "," h) (str "--screenshot=" (fs/absolutize (str "shots/" tag nm "-" w ".png"))) (str frame "?src=" src "&w=" w "&h=" h q)))
(doseq [w [390 1440]]
  (println w (second (re-find #"<pre id=\"out\">(.*?)</pre>" (edge! "--window-size=1440,3000" "--dump-dom" (str frame "?src=" src "&w=" w))))))
