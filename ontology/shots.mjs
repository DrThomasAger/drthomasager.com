// Screenshots of site/explore.html and the Blog Template sample, side by side
// in width and theme. node ontology/shots.mjs from the DrThomasAger folder.
import { chromium } from "file:///C:/Users/hanjo/AppData/Roaming/npm/node_modules/playwright/index.mjs"
import { pathToFileURL } from "node:url"

const explore = pathToFileURL("site/explore.html").href
const sample = pathToFileURL("C:/Users/hanjo/Claude/Projects/Blog Template/sample.html").href
const views = [["explore", explore + "#"], ["explore-ai-measured", explore + "#place=ai&evidence=measured"], ["sample", sample + "#"]]
const b = await chromium.launch()
for (const w of [1440, 390]) for (const theme of ["light", "night"]) for (const [name, url] of views) {
  const p = await b.newPage({ viewport: { width: w, height: 1100 }, reducedMotion: "reduce" })
  const errors = []; p.on("pageerror", e => errors.push(e.message))
  await p.addInitScript(t => { try { localStorage.setItem("blog-theme", t) } catch (e) {} }, theme)
  await p.goto(url); await p.waitForTimeout(700)
  const sideways = await p.evaluate(() => document.documentElement.scrollWidth > innerWidth)
  await p.screenshot({ path: `ontology/shots/b-${name}-${w}-${theme}.png` })
  console.log(name, w, theme, "sideways", sideways, "errors", errors.length ? errors : 0)
  await p.close()
}
await b.close()
