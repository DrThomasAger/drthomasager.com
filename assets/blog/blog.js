// The base template's behaviour for every blog. README.md beside it says how a
// post uses it. Each part works without the others, and a page reads whole
// with this file absent.
(function(){
  const $=s=>document.querySelector(s), $$=s=>[...document.querySelectorAll(s)];
  const root=document.documentElement;
  const wide=()=>matchMedia("(min-width:1150px)").matches;

  // theme: light paper unless the reader chose night, remembered for them
  const saved=(()=>{try{return localStorage.getItem("blog-theme")}catch(e){return null}})();
  const fromHash=(location.hash.match(/^#(light|night)$/)||[])[1];
  if(fromHash||saved==="night") root.dataset.theme=fromHash==="light"?"":(fromHash||saved);
  window.blogTheme=()=>root.dataset.theme==="night"?"night":"light";

  // sidenotes: each note beside its first reference, pushing the next one down
  function placeNotes(){
    const art=$(".page>article"); if(!art) return;
    const top0=art.getBoundingClientRect().top+scrollY; let floor=0;
    $$("p.sn,aside.sn").forEach(n=>{
      if(!wide()){ n.style.top=""; return; }
      const ref=document.querySelector(`sup.fn a[href="#${n.id}"]`);
      const y=ref?ref.getBoundingClientRect().top+scrollY-top0-6:floor;
      const t=Math.max(y,floor); n.style.top=t+"px"; floor=t+n.offsetHeight+16;
    });
  }
  window.blogPlaceNotes=placeNotes;
  $$("sup.fn a").forEach(a=>{
    const n=document.getElementById(a.getAttribute("href").slice(1)); if(!n) return;
    a.addEventListener("click",e=>{ e.preventDefault(); if(wide()){ n.classList.add("on"); setTimeout(()=>n.classList.remove("on"),1800);} else n.classList.toggle("open"); });
    a.addEventListener("mouseenter",()=>n.classList.add("on"));
    a.addEventListener("mouseleave",()=>n.classList.remove("on"));
  });
  addEventListener("load",placeNotes); addEventListener("resize",placeNotes);
  if(document.fonts) document.fonts.ready.then(placeNotes);

  // removable blocks, remembered per reader, with an undo where each was
  const key="blog-removed:"+location.pathname;
  const removed=new Set((()=>{try{return JSON.parse(localStorage.getItem(key)||"[]")}catch(e){return[]}})());
  const restore=$("#restore");
  function save(){ try{localStorage.setItem(key,JSON.stringify([...removed]))}catch(e){} if(restore) restore.hidden=!removed.size; placeNotes(); }
  function hide(b){ b.style.display="none";
    if(!(b.nextElementSibling&&b.nextElementSibling.classList.contains("gone"))){
      const label=(b.querySelector(".label")||{}).textContent||"Block";
      b.insertAdjacentHTML("afterend",`<div class="gone"><span>${label.trim()} · removed</span><button type="button">Undo</button></div>`);
      b.nextElementSibling.querySelector("button").onclick=()=>{ removed.delete(b.id); b.style.display=""; b.nextElementSibling.remove(); save(); };
    } }
  $$(".removable").forEach(b=>{ const x=b.querySelector("[data-remove]"); if(removed.has(b.id)) hide(b); if(x) x.onclick=()=>{ removed.add(b.id); hide(b); save(); }; });
  if(restore) restore.onclick=()=>{ $$(".removable").forEach(b=>{ b.style.display=""; const g=b.nextElementSibling; if(g&&g.classList.contains("gone")) g.remove(); }); removed.clear(); save(); };
  save();

  // theme toggle
  const tb=$("#theme");
  if(tb) tb.onclick=()=>{ const night=blogTheme()!=="night"; root.dataset.theme=night?"night":""; try{localStorage.setItem("blog-theme",night?"night":"light")}catch(e){} document.dispatchEvent(new CustomEvent("blog:theme")); };

  // reading progress
  const bar=$(".progress");
  if(bar) addEventListener("scroll",()=>{ const h=root; bar.style.width=(100*h.scrollTop/Math.max(1,h.scrollHeight-h.clientHeight))+"%"; },{passive:true});

  // a video chapter from the address, #t=52
  const m=location.hash.match(/^#t=(\d+)/), v=$("video[data-chapters]");
  if(m&&v) v.addEventListener("loadedmetadata",()=>{ v.currentTime=+m[1]; },{once:true});

  // sections rise in as they are reached, and drawings with .draw draw themselves
  const reveal=el=>{ el.classList.add("seen"); el.querySelectorAll(".draw").forEach(p=>p.style.strokeDashoffset=0); el.querySelectorAll(".pop").forEach(p=>p.style.opacity=1); };
  window.blogReveal=reveal;
  root.classList.add("anim");
  const io=new IntersectionObserver(es=>es.forEach(e=>{ if(e.isIntersecting){ reveal(e.target); io.unobserve(e.target);} }),{threshold:.15});
  $$(".reveal").forEach(el=>io.observe(el));
  setTimeout(()=>$$(".reveal").forEach(reveal),4000);
})();
