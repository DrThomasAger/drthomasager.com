// Letterhead II, solid gold. Splits the title of .letterhead into words and
// letters so each letter can rise in turn (letterhead-gold.css). Spaces stay
// as text between the words, so the title still wraps between words, and a
// word never breaks across lines. Without this file the title is gold and still.
(function(){
  const h1=document.querySelector(".letterhead h1"); if(!h1) return;
  const text=h1.textContent; const words=text.split(/(\s+)/); let i=0;
  h1.setAttribute("aria-label",text.replace(/\s+/g," ").trim());
  h1.textContent="";
  for(const w of words){
    if(!w) continue;
    if(/^\s+$/.test(w)){ h1.appendChild(document.createTextNode(" ")); continue; }
    const span=document.createElement("span"); span.className="w"; span.setAttribute("aria-hidden","true");
    for(const ch of [...w]){ const c=document.createElement("span"); c.className="ch"; c.style.setProperty("--i",i++); c.textContent=ch; span.appendChild(c); }
    h1.appendChild(span);
  }
})();
