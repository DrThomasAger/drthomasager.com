;; bb first-person.clj [--dry], from this folder. Moves the prose of every post
;; from he and his to I and my, since every post carries Dr Thomas Ager's byline.
;; His quoted words (inside “ ”), citation tokens ([[...]]) and {{counts}} are
;; left exactly as they are. --dry prints each changed sentence instead of writing.
(require '[clojure.string :as s] '[clojure.edn :as edn] '[babashka.fs :as fs] '[clojure.pprint :as pp])

(def verbs {"prompts" "prompt" "owns" "own" "works" "work" "names" "name" "asks" "ask" "uses" "use"
            "types" "type" "tells" "tell" "has" "have" "is" "am" "was" "was" "says" "say" "wants" "want"
            "writes" "write" "keeps" "keep" "calls" "call" "does" "do" "sees" "see" "gives" "give"})

(defn swap-words [t]
  (-> t
      ;; "of his own words" and "one of his instructions" take my, a bare "of his" takes mine
      (s/replace #"\bof his (?=[a-z])(?!on\b|in\b|that\b|about\b|from\b|across\b|since\b|before\b)" "of my ")
      (s/replace #"\bof his\b" "of mine")
      (s/replace #"\b([Hh]e) ([a-z]+)\b"
                 (fn [[_ h v]] (str "I " (get verbs v v))))
      (s/replace #"\bHe\b" "I") (s/replace #"\bhe\b" "I")
      (s/replace #"\bHis\b" "My") (s/replace #"\bhis\b" "my")
      (s/replace #"\bhimself\b" "myself") (s/replace #"\bhim\b" "me")
      (s/replace #"\bI am\b(?= (?:asked|named|described))" "I was")))

(defn convert
  "Converts only the text outside his quotes and outside tokens."
  [t]
  (let [parts (re-seq #"“[^”]*”|\[\[[^\]]*\]\]|\{\{[^}]*\}\}|[^“\[{]+|[\[{]" t)]
    (apply str (for [p parts] (if (re-find #"^(“|\[\[|\{\{)" p) p (swap-words p))))))

(defn convert-post [p]
  (-> p
      (update :title convert) (update :description convert) (update :lede convert)
      (update :paras #(mapv convert %))
      (update :faq #(mapv (fn [[q a]] [(convert q) (convert a)]) %))))

(def dry? (= "--dry" (first *command-line-args*)))
(doseq [f (concat (fs/glob "prose" "*.edn") (fs/glob "prose-built" "*.edn"))
        :let [p (edn/read-string (slurp (str f))) q (convert-post p)]
        :when (not= p q)]
  (if dry?
    (doseq [[a b] (map vector (concat [(:lede p)] (:paras p)) (concat [(:lede q)] (:paras q)))
            :when (not= a b)
            [x y] (map vector (s/split a #"(?<=\.) ") (s/split b #"(?<=\.) ")) :when (not= x y)]
      (println (fs/file-name f) "|" y))
    (do (spit (str f) (with-out-str (binding [*print-namespace-maps* false] (pp/pprint q))))
        (println "converted" (fs/file-name f)))))
