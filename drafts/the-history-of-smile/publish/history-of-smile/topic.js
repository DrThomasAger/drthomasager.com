// The figure of one idea of Smile, drawn from window.T (written by topic.clj).
// The top lane is every moment of this idea. The lanes below are the ideas said
// most often beside it, a dot wherever both were spoken of in the same place.
(function () {
  const T = window.T
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim()
  const parse = d3.utcParse("%Y-%m-%d")
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c])
  const tip = document.createElement("div")
  tip.className = "h-tip"; tip.hidden = true; document.body.appendChild(tip)
  const show = (ev, html) => {
    tip.innerHTML = html; tip.hidden = false
    const r = tip.getBoundingClientRect()
    let x = ev.clientX + 14, y = ev.clientY + 14
    if (x + r.width > innerWidth - 8) x = Math.max(8, ev.clientX - r.width - 14)
    if (y + r.height > innerHeight - 8) y = Math.max(8, ev.clientY - r.height - 14)
    tip.style.left = x + "px"; tip.style.top = y + "px"
  }
  const hide = () => (tip.hidden = true)

  function figure(slot) {
    const narrow = slot.clientWidth < 600
    const W = narrow ? 420 : 1000, L = narrow ? 6 : 190, R = W - 14, top = 34
    const laneH = narrow ? 34 : 26
    const lanes = [{ name: T.title, dates: T.moments.map(m => m.d), main: true }].concat(T.beside)
    const Hh = top + lanes.length * laneH + 24
    const x = d3.scaleUtc()
      .domain([parse("2023-07-20"), parse("2023-11-25"), parse("2025-06-15"), parse("2026-10-31")])
      .range([L, L + (R - L) * 0.17, L + (R - L) * 0.22, R])
    const svg = d3.select(slot).append("svg").attr("viewBox", `0 0 ${W} ${Hh}`)
      .attr("role", "img").attr("aria-label", `Every moment of ${T.title} on a time axis, with the ideas said beside it`)
    const y = i => top + i * laneH + laneH / 2
    const q0 = x(parse("2023-11-25")), q1 = x(parse("2025-06-15"))
    svg.append("rect").attr("x", q0).attr("y", top - 6).attr("width", q1 - q0).attr("height", lanes.length * laneH + 6).attr("fill", css("--surface"))
    const g = svg.append("g").attr("font-family", css("--sans")).attr("font-size", 11).attr("fill", css("--ink-2"))
    ;["2023-08-01", "2023-10-01", "2025-07-01", "2025-10-01", "2026-01-01", "2026-04-01", "2026-07-01", "2026-10-01"].map(parse).forEach((t, k) => {
      if (narrow && k % 2) return
      g.append("line").attr("x1", x(t)).attr("x2", x(t)).attr("y1", top - 6).attr("y2", top + lanes.length * laneH).attr("stroke", css("--rule"))
      g.append("text").attr("x", x(t)).attr("y", top - 12).attr("text-anchor", narrow && k === 0 ? "start" : "middle").text(d3.utcFormat("%b %Y")(t))
    })
    const r = d3.scaleSqrt().domain([1, 20]).range([narrow ? 3 : 3, narrow ? 9 : 10]).clamp(true)
    lanes.forEach((ln, i) => {
      svg.append("line").attr("x1", L).attr("x2", R).attr("y1", y(i)).attr("y2", y(i)).attr("stroke", css("--rule")).attr("stroke-dasharray", "1 4")
      const label = (ln.main ? svg : svg.append("a").attr("href", ln.href))
        .append("text").attr("font-family", css("--sans")).attr("font-weight", ln.main ? 600 : 400)
        .attr("fill", ln.main ? css("--accent") : css("--ink-2"))
      if (narrow) label.attr("x", L + 2).attr("y", y(i) - 9).attr("font-size", 11.5).text(ln.main ? ln.name : `${ln.name} (${ln.dates.length})`)
      else label.attr("x", L - 10).attr("y", y(i) + 4).attr("text-anchor", "end").attr("font-size", 12).text(ln.main ? ln.name : `${ln.name} (${ln.dates.length})`)
    })
    T.moments.forEach(m => {
      if (!m.d) return
      svg.append("circle").attr("cx", x(parse(m.d))).attr("cy", y(0)).attr("r", r(m.q))
        .attr("fill", css("--accent")).attr("fill-opacity", 0.75).style("cursor", "pointer")
        .on("mousemove", ev => show(ev, `<b>${esc(m.d)}</b><span>${esc(m.w)} · ${m.q} quote${m.q === 1 ? "" : "s"}</span>${m.x ? `<q>${esc(m.x)}</q>` : ""}`))
        .on("mouseleave", hide)
        .on("click", () => { const a = document.getElementById(m.a); if (a) { a.open = true; a.scrollIntoView({ behavior: "smooth", block: "center" }) } })
    })
    lanes.slice(1).forEach((ln, i) => ln.dates.forEach(d => {
      if (!d) return
      svg.append("circle").attr("cx", x(parse(d))).attr("cy", y(i + 1)).attr("r", narrow ? 3.4 : 3.6)
        .attr("fill", css("--hue-2")).attr("fill-opacity", 0.6)
        .on("mousemove", ev => show(ev, `<b>${esc(ln.name)}</b><span>said beside ${esc(T.title)} on ${esc(d)}</span>`))
        .on("mouseleave", hide)
    }))
  }
  window.TD = { figure }
})()
