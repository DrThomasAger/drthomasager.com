// The article widgets that move. A checklist remembers its ticks in the
// reader's own browser, per page. Each part works without the others.
(function(){
  const boxes=[...document.querySelectorAll("li.check input[type=checkbox]")];
  if(!boxes.length) return;
  const key="checks:"+location.pathname;
  let saved={};
  try{ saved=JSON.parse(localStorage.getItem(key)||"{}"); }catch(e){}
  boxes.forEach((b,i)=>{
    if(i in saved) b.checked=saved[i];
    b.addEventListener("change",()=>{ saved[i]=b.checked; try{localStorage.setItem(key,JSON.stringify(saved))}catch(e){} });
  });
})();
