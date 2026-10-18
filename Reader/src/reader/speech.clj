(ns reader.speech
  "Speech for the reader, in Clojure, with the time of every spoken word.

  This speaks to the same Microsoft Edge read-aloud service that the
  edge-tts package uses (installed globally on this machine, version
  7.2.8, whose constants this namespace follows). The edge-tts command
  line only writes sentence times, so the conversation is held here
  directly over java.net.http's WebSocket, with word boundaries turned
  on.

  From a REPL
    (require '[reader.speech :as s] :reload)
    (s/speak-paragraphs [\"A language model keeps nothing between calls.\"])
  returns {:audio <bytes> :pieces [[{:text .. :start s :end s} ..]]}."
  (:require [clojure.string :as str]
            [jsonista.core :as j])
  (:import (java.net URI)
           (java.net.http HttpClient WebSocket WebSocket$Listener)
           (java.nio ByteBuffer)
           (java.security MessageDigest SecureRandom)
           (java.io ByteArrayOutputStream)
           (java.time ZonedDateTime ZoneOffset)
           (java.time.format DateTimeFormatter)
           (java.util Locale UUID)
           (java.util.concurrent CompletableFuture TimeUnit)))

(def speaker "en-GB-RyanNeural")

(def ^:private trusted-token "6A5AA1D4EAFF4E9FB37E23D68491D6F4")
(def ^:private chromium "143.0.3650.75")
(def ^:private chromium-major (first (str/split chromium #"\.")))
(def ^:private ticks-per-second 10000000)
(def ^:private mp3-bits-per-second 48000)

(defn- sha256-hex [^String s]
  (let [d (.digest (MessageDigest/getInstance "SHA-256") (.getBytes s "US-ASCII"))]
    (str/upper-case (apply str (map #(format "%02x" (bit-and % 0xff)) d)))))

(defn sec-ms-gec-v1
  "The first form of the token, the Windows file time rounded down to
  five minutes, joined to the trusted client token and hashed. The service
  refused it with 403 from 2026-10-18."
  []
  (let [unix (quot (System/currentTimeMillis) 1000)
        win  (+ unix 11644473600)
        win  (- win (mod win 300))]
    (sha256-hex (str (* win 10000000) trusted-token))))

(defn sec-ms-gec
  "The token the service asks for since October 2026, version 2, a CS64
  digest and a SHA-256 digest joined by a dash. edge-tts 7.3.1 carries the
  hash, about 300 lines, so it is asked of the installed package rather
  than written again here. It changes every five minutes."
  []
  (let [p (.start (ProcessBuilder. ["python" "-c" "from edge_tts.drm import DRM; print(DRM.generate_sec_ms_gec())"]))
        out (str/trim (slurp (.getInputStream p)))]
    (.waitFor p)
    (if (re-matches #"[0-9A-F]{16}-[0-9A-F]{64}" out) out (sec-ms-gec-v1))))

(defn- hex-id []
  (str/replace (str (UUID/randomUUID)) "-" ""))

(defn- muid []
  (let [b (byte-array 16)]
    (.nextBytes (SecureRandom.) b)
    (str/upper-case (apply str (map #(format "%02x" (bit-and % 0xff)) b)))))

(defn- js-date []
  (.format (ZonedDateTime/now ZoneOffset/UTC)
           (DateTimeFormatter/ofPattern
            "EEE MMM dd yyyy HH:mm:ss 'GMT+0000 (Coordinated Universal Time)'"
            Locale/US)))

(defn- xml-escape [s]
  (-> s (str/replace "&" "&amp;") (str/replace "<" "&lt;") (str/replace ">" "&gt;")))

(defn- ssml [text]
  (str "<speak version='1.0' xmlns='http://www.w3.org/2001/10/synthesis' xml:lang='en-US'>"
       "<voice name='" speaker "'><prosody pitch='+0Hz' rate='+0%' volume='+0%'>"
       (xml-escape text)
       "</prosody></voice></speak>"))

(defn- headers-of
  "Splits a text frame or the header part of a binary frame into a map."
  [^String head]
  (into {} (for [line (str/split-lines head)
                 :let [i (.indexOf line ":")]
                 :when (pos? i)]
             [(subs line 0 i) (subs line (inc i))])))

(defn- speak-one
  "Speaks one piece of text on its own connection. Returns
  {:audio bytes :marks [{:text :offset :duration}]} with offsets in ticks
  counted from the start of this piece."
  [text]
  (let [done   (CompletableFuture.)
        audio  (ByteArrayOutputStream.)
        marks  (atom [])
        tbuf   (StringBuilder.)
        bbuf   (ByteArrayOutputStream.)
        on-text (fn [^String msg]
                  (let [i    (.indexOf msg "\r\n\r\n")
                        hs   (headers-of (subs msg 0 i))
                        body (subs msg (+ i 4))]
                    (case (get hs "Path")
                      "audio.metadata"
                      (doseq [m (get (j/read-value body) "Metadata")
                              :when (= "WordBoundary" (get m "Type"))]
                        (swap! marks conj
                               {:text     (get-in m ["Data" "text" "Text"])
                                :offset   (get-in m ["Data" "Offset"])
                                :duration (get-in m ["Data" "Duration"])}))
                      "turn.end" (.complete done true)
                      nil)))
        on-binary (fn [^bytes b]
                    (let [hl (bit-or (bit-shift-left (bit-and (aget b 0) 0xff) 8)
                                     (bit-and (aget b 1) 0xff))
                          hs (headers-of (String. b 2 (int hl) "UTF-8"))
                          n  (- (alength b) 2 hl)]
                      (when (and (= "audio" (get hs "Path")) (pos? n))
                        (.write audio b (int (+ 2 hl)) (int n)))))
        listener
        (reify WebSocket$Listener
          (onOpen [_ ws] (.request ws 1))
          (onText [_ ws data last?]
            (.append tbuf data)
            (when last?
              (let [s (str tbuf)] (.setLength tbuf 0) (on-text s)))
            (.request ws 1) nil)
          (onBinary [_ ws data last?]
            (let [arr (byte-array (.remaining ^ByteBuffer data))]
              (.get ^ByteBuffer data arr)
              (.write bbuf arr 0 (alength arr)))
            (when last?
              (let [b (.toByteArray bbuf)] (.reset bbuf) (on-binary b)))
            (.request ws 1) nil)
          (onClose [_ ws code reason] (.complete done false) nil)
          (onError [_ ws err] (.completeExceptionally done err)))
        url (str "wss://speech.platform.bing.com/consumer/speech/synthesize/readaloud/edge/v1"
                 "?TrustedClientToken=" trusted-token
                 "&ConnectionId=" (hex-id)
                 "&Sec-MS-GEC=" (sec-ms-gec)
                 "&Sec-MS-GEC-Version=2-" chromium)
        ws (-> (HttpClient/newHttpClient)
               (.newWebSocketBuilder)
               (.header "Pragma" "no-cache")
               (.header "Cache-Control" "no-cache")
               (.header "Origin" "chrome-extension://jdiccldimpdaibmpdkjnbmckianbfold")
               (.header "User-Agent"
                        (str "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                             " (KHTML, like Gecko) Chrome/" chromium-major ".0.0.0 Safari/537.36"
                             " Edg/" chromium-major ".0.0.0"))
               (.header "Accept-Language" "en-US,en;q=0.9")
               (.header "Cookie" (str "muid=" (muid) ";"))
               (.buildAsync (URI. url) listener)
               (.get 30 TimeUnit/SECONDS))]
    (.get (.sendText ws (str "X-Timestamp:" (js-date) "\r\n"
                             "Content-Type:application/json; charset=utf-8\r\n"
                             "Path:speech.config\r\n\r\n"
                             "{\"context\":{\"synthesis\":{\"audio\":{\"metadataoptions\":{"
                             "\"sentenceBoundaryEnabled\":\"false\",\"wordBoundaryEnabled\":\"true\"},"
                             "\"outputFormat\":\"audio-24khz-48kbitrate-mono-mp3\"}}}}\r\n")
                     true))
    (.get (.sendText ws (str "X-RequestId:" (hex-id) "\r\n"
                             "Content-Type:application/ssml+xml\r\n"
                             "X-Timestamp:" (js-date) "Z\r\n"
                             "Path:ssml\r\n\r\n"
                             (ssml text))
                     true))
    (.get done 120 TimeUnit/SECONDS)
    (try (.get (.sendClose ws WebSocket/NORMAL_CLOSURE "") 5 TimeUnit/SECONDS)
         (catch Exception _))
    {:audio (.toByteArray audio) :marks @marks}))

(defn- speak-with-retries [text]
  (loop [n 1]
    (let [r (try (let [r (speak-one text)]
                   (if (pos? (alength ^bytes (:audio r))) r (throw (ex-info "no audio" {}))))
                 (catch Exception e (if (< n 4) ::again (throw e))))]
      (if (= r ::again)
        (do (Thread/sleep (* 1500 n)) (recur (inc n)))
        r))))

(defn speak-paragraphs
  "Speaks each piece of text and joins the audio into one mp3. Six
  pieces are asked for at a time. Word times are carried across pieces
  by the exact byte count of the constant 48 kbps stream before each
  piece, as edge-tts does. Returns {:audio bytes :pieces [[{:text :start
  :end} ..] ..]}, one vector of spoken words per piece, times in seconds."
  [texts]
  (let [spoken (vec (mapcat #(doall (pmap speak-with-retries %))
                            (partition-all 6 texts)))
        out    (ByteArrayOutputStream.)]
    (loop [[s & more] spoken, pieces []]
      (if (nil? s)
        {:audio (.toByteArray out) :pieces pieces}
        (let [shift (quot (* (.size out) 8 ticks-per-second) mp3-bits-per-second)
              ^bytes audio (:audio s)]
          (.write out audio 0 (alength audio))
          (recur more
                 (conj pieces
                       (vec (for [{:keys [text offset duration]} (:marks s)]
                              {:text  text
                               :start (/ (double (+ shift offset)) ticks-per-second)
                               :end   (/ (double (+ shift offset duration)) ticks-per-second)})))))))))

(comment
  (def r (speak-paragraphs ["A language model keeps nothing between calls."
                            "An agent remembers through its context."]))
  (count (:audio r))
  (:pieces r))
