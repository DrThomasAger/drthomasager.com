// Figure 1 of the features timeline, from window.F (written by features.clj).
// One lane per part of Smile, July to October 2026. Blue dots are askings in his
// words, green squares commits, rose crosses things delivered otherwise.
(function () {
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim()
  const parse = d3.utcParse("%Y-%m-%d")
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c])
  const tip = document.createElement("div"); tip.className = "h-tip"; tip.hidden = true; document.body.appendChild(tip)
  const show = (ev, html) => {
    tip.innerHTML = html; tip.hidden = false
    const r = tip.getBoundingClientRect()
    let x = ev.clientX + 14, y = ev.clientY + 14
    if (x + r.width > innerWidth - 8) x = Math.max(8, ev.clientX - r.width - 14)
    if (y + r.height > innerHeight - 8) y = Math.max(8, ev.clientY - r.height - 14)
    tip.style.left = x + "px"; tip.style.top = y + "px"
  }
  const hide = () => (tip.hidden = true)
  function draw(slot) {
    const narrow = slot.clientWidth < 600
    const W = narrow ? 420 : 1000, L = narrow ? 6 : 220, R = W - 14, top = 34, laneH = narrow ? 30 : 22
    const lanes = F.lanes
    const H = top + lanes.length * laneH + 10
    const x = d3.scaleUtc().domain([parse("2026-07-20"), parse("2026-10-19")]).range([L, R])
    const svg = d3.select(slot).append("svg").attr("viewBox", `0 0 ${W} ${H}`).attr("role", "img")
      .attr("aria-label", "What I asked of each part of Smile and the commits that built it, July to October 2026")
    const y = i => top + i * laneH + laneH / 2
    x.ticks(d3.utcMonth.every(1)).forEach(t => {
      svg.append("line").attr("x1", x(t)).attr("x2", x(t)).attr("y1", top - 6).attr("y2", H - 10).attr("stroke", css("--rule"))
      svg.append("text").attr("x", x(t)).attr("y", top - 12).attr("text-anchor", "middle").attr("font-family", css("--sans")).attr("font-size", 11).attr("fill", css("--ink-2")).text(d3.utcFormat("%b %Y")(t))
    })
    lanes.forEach((ln, i) => {
      const g = svg.append("g").style("cursor", "pointer").on("click", () => { const a = document.getElementById(ln.a); if (a) { a.open = true; a.scrollIntoView({ behavior: "smooth", block: "start" }) } })
      g.append("line").attr("x1", L).attr("x2", R).attr("y1", y(i)).attr("y2", y(i)).attr("stroke", css("--rule")).attr("stroke-dasharray", "1 4")
      const t = g.append("text").attr("font-family", css("--sans")).attr("font-size", narrow ? 11 : 12).attr("fill", css("--ink-2")).text(ln.name.length > 30 ? ln.name.slice(0, 28) + "…" : ln.name)
      if (narrow) t.attr("x", L + 2).attr("y", y(i) - 8); else t.attr("x", L - 10).attr("y", y(i) + 4).attr("text-anchor", "end")
      ln.built.forEach(c => g.append("rect").attr("x", x(parse(c.d)) - 3.5).attr("y", y(i) - 3.5).attr("width", 7).attr("height", 7).attr("fill", css("--hue-4")).attr("fill-opacity", .7)
        .on("mousemove", ev => show(ev, `<b>${esc(ln.name)}, built</b><span>${esc(c.d)}</span><q>${esc(c.x)}</q>`)).on("mouseleave", hide))
      ln.asks.forEach(a => g.append("circle").attr("cx", x(parse(a.d))).attr("cy", y(i)).attr("r", narrow ? 3.4 : 3.8).attr("fill", css("--hue-1")).attr("fill-opacity", .8)
        .on("mousemove", ev => show(ev, `<b>${esc(ln.name)}, asked</b><span>${esc(a.d)}</span><q>${esc(a.x)}</q>`)).on("mouseleave", hide))
      ln.otherwise.forEach(o => g.append("text").attr("x", x(parse(o.d))).attr("y", y(i) + 4).attr("text-anchor", "middle").attr("font-size", 12).attr("fill", css("--hue-2")).text("×")
        .on("mousemove", ev => show(ev, `<b>${esc(ln.name)}, delivered otherwise</b><span>${esc(o.d)}</span><q>${esc(o.x)}</q>`)).on("mouseleave", hide))
    })
  }
  window.FD = { draw }
})()
