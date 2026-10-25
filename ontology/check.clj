(ns check
  "The DrThomasAger ontology checked, and its files for readers and MCPs written.
  bb ontology/check.clj            checks the tree and every placement, writes index.json and ontology.json
  bb ontology/check.clj <slug>     prints that post's kicker, its breadcrumb JSON-LD and its tags"
  (:require [clojure.edn :as edn]
            [clojure.string :as str]
            [cheshire.core :as json]
            [babashka.fs :as fs]))

(def dir (str (fs/parent (fs/absolutize *file*))))
(def onto (edn/read-string (slurp (str dir "/ontology.edn"))))
(def placements (edn/read-string (slurp (str dir "/placements.edn"))))

(defn nodes
  "Every node with its route from the root, e.g. [ai agents ai-companions]."
  ([] (mapcat #(nodes % []) (:tree onto)))
  ([n route] (let [r (conj route n)] (cons (assoc n :route r) (mapcat #(nodes % r) (:children n))))))

(def by-id (into {} (map (juxt :id identity) (nodes))))

(defn kicker [id] (str/join " › " (map :label (:route (by-id id)))))

(defn tree-problems []
  (let [ns (nodes) ids (map :id ns) tiers (count (:tiers onto))]
    (concat
     (for [[id n] (frequencies ids) :when (> n 1)] (str "id used twice " id))
     (for [n ns :when (str/blank? (:definition n))] (str "no definition " (:id n)))
     (for [n ns :when (> (count (:route n)) tiers)] (str "deeper than " tiers " tiers " (:id n)))
     (for [n ns :when (and (> (count (:route n)) 1) (not= (namespace (:id n)) (name (:id (first (:route n))))))]
       (str "id not under its root's namespace " (:id n)))
     (for [n ns, [label k] (frequencies (map :label (:children n))) :when (> k 1)] (str "two siblings named " label " under " (:id n))))))

(defn placement-problems [[slug {:keys [place facets]}]]
  (concat
   (when-not (by-id place) [(str slug " is placed at " place ", which is not in the tree")])
   (when (and (by-id place) (< (count (:route (by-id place))) 3))
     [(str slug " is placed at " place ", above the subject tier")])
   (for [[facet vs] facets, v vs :when (not (get-in onto [:facets facet :values v]))]
     (str slug " has " facet " " v ", which is not in the vocabulary"))))

(defn breadcrumb [slug]
  (let [{:keys [place title]} (placements slug)]
    {"@context" "https://schema.org" "@type" "BreadcrumbList"
     "itemListElement" (vec (map-indexed (fn [i n] {"@type" "ListItem" "position" (inc i) "name" (:label n)
                                                     "item" (str "https://drthomasager.com/" (str/join "/" (map (comp name :id) (take (inc i) (:route (by-id place))))))})
                                         (:route (by-id place))))}))

(defn front-matter
  "The date, read time and link of a post that lives in posts/."
  [slug]
  (let [f (fs/file (fs/parent dir) "posts" (str slug ".md"))]
    (when (fs/exists? f)
      (let [s (slurp f)]
        {:date (second (re-find #"(?m)^date: *(\S+)" s))
         :readtime (some-> (re-find #"(?m)^readtime: *(\d+)" s) second parse-long)
         :site-project (some-> (re-find #"(?m)^project: *(.+)$" s) second str/trim)
         :glyph (some-> (re-find #"(?m)^glyph: *(.+)$" s) second str/trim)
         :description (some-> (re-find #"(?m)^description: *(.+)$" s) second str/trim)
         :url (str slug ".html")}))))

(defn index []
  (vec (for [[slug {:keys [place title facets file url date readtime site-project glyph description]}] (sort-by key placements)
             :let [fm (front-matter slug)]]
         {:slug slug :title title :kicker (kicker place) :place (str place)
          :date (or date (:date fm)) :readtime (or readtime (:readtime fm))
          :site-project (or site-project (:site-project fm)) :glyph (or glyph (:glyph fm))
          :description (or description (:description fm))
          :url (or (:url fm) url (str "file:///" file))
          :depth (count (:route (by-id place)))
          :route (mapv (comp str :id) (:route (by-id place)))
          :root (name (:id (first (:route (by-id place)))))
          :facets (into {} (for [[k vs] facets] [k (mapv name vs)]))
          :file file})))

(defn -main [& [slug]]
  (if slug
    (let [{:keys [place facets]} (placements slug)]
      (println (kicker place))
      (println (json/generate-string (breadcrumb slug)))
      (println (str/join ", " (for [[k vs] facets v vs] (str (name k) ":" (name v))))))
    (let [problems (concat (tree-problems) (mapcat placement-problems placements))]
      (spit (str dir "/ontology.json") (json/generate-string onto {:pretty true}))
      (spit (str dir "/index.json") (json/generate-string (index) {:pretty true}))
      (doseq [p problems] (println "problem" p))
      (println (count (nodes)) "nodes," (count placements) "posts placed,"
               (if (empty? problems) "every placement is valid" (str (count problems) " problems")))
      (System/exit (if (empty? problems) 0 1)))))

(when (= *file* (System/getProperty "babashka.file")) (apply -main *command-line-args*))
