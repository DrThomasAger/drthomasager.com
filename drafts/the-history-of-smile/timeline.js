// The two figures of the history of Smile, drawn from window.H (data.js, written by build.clj).
// Figure 1, every moment on a time axis, one lane per thread, the quiet of 2023-11 to 2025-06 drawn narrow.
// Figure 2, the regions, threads and sections packed inside one another, sized by my quotes.
(function () {
  const H = window.H
  const css = n => getComputedStyle(document.documentElement).getPropertyValue(n).trim()
  const regionHue = i => css(["--hue-1", "--hue-2", "--hue-3", "--hue-4", "--ink-2"][i % 5])
  const tip = (() => {
    const t = document.createElement("div")
    t.className = "h-tip"
    t.hidden = true
    document.body.appendChild(t)
    return t
  })()
  const show = (ev, html) => {
    tip.innerHTML = html
    tip.hidden = false
    const r = tip.getBoundingClientRect()
    let x = ev.clientX + 14, y = ev.clientY + 14
    if (x + r.width > innerWidth - 8) x = Math.max(8, ev.clientX - r.width - 14)
    if (y + r.height > innerHeight - 8) y = Math.max(8, ev.clientY - r.height - 14)
    tip.style.left = x + "px"
    tip.style.top = y + "px"
  }
  const hide = () => (tip.hidden = true)
  const esc = s => String(s ?? "").replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" })[c])
  const parse = d3.utcParse("%Y-%m-%d")

  function timeline(slot) {
    const narrow = slot.clientWidth < 600
    const W = narrow ? 420 : 1000, L = narrow ? 6 : 190, R = W - 14, laneH = narrow ? 32 : 24, top = 34
    const lanes = H.threads.map((t, i) => ({ ...t, i }))
    const extra = [{ name: "Commits", key: "built" }, { name: "Project folders", key: "folder" }]
    const rows = lanes.length + extra.length
    const Hh = top + rows * laneH + 30
    const x = d3.scaleUtc()
      .domain([parse("2023-09-20"), parse("2023-11-25"), parse("2025-06-15"), parse("2026-10-31")])
      .range([L, L + (R - L) * 0.17, L + (R - L) * 0.22, R])
    const svg = d3.select(slot).append("svg").attr("viewBox", `0 0 ${W} ${Hh}`)
      .attr("role", "img").attr("aria-label", "Every moment in the history of Smile on a time axis, one lane for each thread of the pillars")
    const y = i => top + i * laneH + laneH / 2
    // the quiet stretch
    const q0 = x(parse("2023-11-25")), q1 = x(parse("2025-06-15"))
    svg.append("rect").attr("x", q0).attr("y", top - 6).attr("width", q1 - q0).attr("height", rows * laneH + 6)
      .attr("fill", css("--surface"))
    svg.append("text").attr("x", (q0 + q1) / 2).attr("y", top + rows * laneH + 22).attr("text-anchor", "middle")
      .attr("font-family", css("--sans")).attr("font-size", 11).attr("fill", css("--ink-2")).text("quiet")
    // axis ticks
    const ticks = ["2023-10-01", "2025-07-01", "2025-10-01", "2026-01-01", "2026-04-01", "2026-07-01", "2026-10-01"].map(parse)
    const g = svg.append("g").attr("font-family", css("--sans")).attr("font-size", narrow ? 11 : 11).attr("fill", css("--ink-2"))
    ticks.forEach((t, k) => {
      if (narrow && k % 2) return
      g.append("line").attr("x1", x(t)).attr("x2", x(t)).attr("y1", top - 6).attr("y2", top + rows * laneH).attr("stroke", css("--rule"))
      g.append("text").attr("x", x(t)).attr("y", top - 12).attr("text-anchor", narrow && k === 0 ? "start" : "middle").text(d3.utcFormat("%b %Y")(t))
    })
    // lanes
    const all = lanes.map(t => t.name).concat(extra.map(e => e.name))
    all.forEach((n, i) => {
      svg.append("line").attr("x1", L).attr("x2", R).attr("y1", y(i)).attr("y2", y(i)).attr("stroke", css("--rule")).attr("stroke-dasharray", "1 4")
      const label = svg.append("text").attr("font-family", css("--sans")).attr("fill", i < lanes.length ? regionHue(lanes[i].region) : css("--ink-2"))
      if (narrow) label.attr("x", L + 2).attr("y", y(i) - 8).attr("font-size", 11.5).text(n)
      else label.attr("x", L - 10).attr("y", y(i) + 4).attr("text-anchor", "end").attr("font-size", 12).text(n)
    })
    const r = d3.scaleSqrt().domain([1, 40]).range([narrow ? 2.4 : 2.6, narrow ? 7 : 9]).clamp(true)
    const dots = svg.append("g")
    H.events.forEach(e => {
      if (!e.d) return
      dots.append("circle").attr("cx", x(parse(e.d))).attr("cy", y(e.t)).attr("r", r(e.q || 1))
        .attr("fill", regionHue(H.threads[e.t].region)).attr("fill-opacity", e.f ? 0.95 : 0.45)
        .attr("stroke", e.f ? css("--ink") : "none").attr("stroke-width", 1.2).style("cursor", "pointer")
        .on("mousemove", ev => show(ev, `<b>${esc(e.s)}</b><span>${esc(e.d)}${e.f ? ", first said" : ""} · ${e.q} quote${e.q === 1 ? "" : "s"}</span><span>${esc(e.w)}</span>${e.x ? `<q>${esc(e.x)}</q>` : ""}`))
        .on("mouseleave", hide)
        .on("click", () => { const a = document.getElementById(e.a); if (a) { a.open = true; a.scrollIntoView({ behavior: "smooth", block: "center" }) } })
    })
    const by = lanes.length, fy = lanes.length + 1
    const rc = d3.scaleSqrt().domain([1, 206]).range([narrow ? 1.6 : 2, narrow ? 7 : 10])
    H.built.forEach(b => {
      dots.append("circle").attr("cx", x(parse(b.d))).attr("cy", y(by)).attr("r", rc(b.n))
        .attr("fill", "none").attr("stroke", b.pub ? css("--hue-1") : css("--hue-3")).attr("stroke-width", 1.3)
        .on("mousemove", ev => show(ev, `<b>${b.n} commit${b.n === 1 ? "" : "s"}</b><span>${esc(b.d)}, ${b.pub ? "the public repository on GitHub" : "the repository on my PC"}</span><q>${esc(b.subj)}</q>`))
        .on("mouseleave", hide)
    })
    H.folders.forEach(f => {
      dots.append("rect").attr("x", x(parse(f.d)) - 3.5).attr("y", y(fy) - 3.5).attr("width", 7).attr("height", 7)
        .attr("transform", `rotate(45 ${x(parse(f.d))} ${y(fy)})`).attr("fill", css("--ink-2"))
        .on("mousemove", ev => show(ev, `<b>${esc(f.name)}</b><span>${esc(f.d)}, a project folder begun</span>`))
        .on("mouseleave", hide)
    })
  }

  function pack(slot) {
    const narrow = slot.clientWidth < 600
    const S = 1000
    const root = d3.hierarchy({ name: "Smile", children: H.tree }).sum(d => d.q ? Math.max(d.q, 2) : 0)
      .sort((a, b) => b.value - a.value)
    d3.pack().size([S, S]).padding(d => d.depth === 0 ? 14 : d.depth === 1 ? 8 : 3)(root)
    const svg = d3.select(slot).append("svg").attr("viewBox", `0 -34 ${S} ${S + 34}`)
      .attr("role", "img").attr("aria-label", "The five regions of Smile, the threads inside them and THE MAP's sections inside those, each circle sized by my quotes")
    const node = svg.selectAll("g").data(root.descendants().slice(1)).join("g")
      .attr("transform", d => `translate(${d.x},${d.y})`)
    const hueOf = d => regionHue(d.ancestors().find(a => a.depth === 1).data.ri)
    node.append("circle").attr("r", d => d.r)
      .attr("fill", d => d.depth === 3 ? hueOf(d) : "none")
      .attr("fill-opacity", d => d.depth === 3 ? 0.55 : 0)
      .attr("stroke", d => d.depth === 3 ? "none" : hueOf(d))
      .attr("stroke-width", d => d.depth === 1 ? 2 : 1).attr("stroke-dasharray", d => d.depth === 2 ? "3 3" : null)
      .style("cursor", d => d.depth === 3 ? "pointer" : null)
      .on("mousemove", (ev, d) => show(ev, d.depth === 3
        ? `<b>${esc(d.data.name)}</b><span>${esc(d.parent.parent.data.name)} › ${esc(d.parent.data.name)}</span><span>first said ${esc(d.data.first || "undated")} · ${d.data.q} quotes</span>`
        : `<b>${esc(d.data.name)}</b><span>${d.depth === 1 ? "a region" : "a thread"}, ${d.leaves().length} sections</span>`))
      .on("mouseleave", hide)
      .on("click", (ev, d) => { if (d.depth !== 3) return; const a = document.getElementById(d.data.a); if (a) { a.open = true; a.scrollIntoView({ behavior: "smooth", block: "center" }) } })
    node.filter(d => d.depth === 3 && d.r > (narrow ? 34 : 24)).append("text")
      .attr("text-anchor", "middle").attr("dy", "0.35em").attr("pointer-events", "none")
      .attr("font-family", css("--sans")).attr("font-size", d => Math.min(narrow ? 22 : 14, d.r / 3.2)).attr("fill", css("--ink"))
      .text(d => d.data.name.length > 18 ? d.data.name.slice(0, 16) + "…" : d.data.name)
    node.filter(d => d.depth === 1).append("text").attr("text-anchor", "middle").attr("y", d => -d.r - 8)
      .attr("font-family", css("--display")).attr("font-size", narrow ? 24 : 17).attr("font-weight", 600)
      .attr("fill", hueOf).attr("pointer-events", "none").text(d => d.data.name)
  }

  window.HD = { timeline, pack }
})()
