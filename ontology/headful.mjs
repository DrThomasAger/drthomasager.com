// A visible browser on site/explore.html that reloads each time the page is
// rebuilt, and writes what it shows to shots/live-<width>.png.
// node ontology/headful.mjs from the DrThomasAger folder.
import { chromium } from "file:///C:/Users/hanjo/AppData/Roaming/npm/node_modules/playwright/index.mjs"
import { pathToFileURL } from "node:url"
import { watch } from "node:fs"

const file = "site/explore.html", url = pathToFileURL(file).href
const b = await chromium.launch({ headless: false })
const wide = await b.newPage({ viewport: { width: 1440, height: 1000 } })
const phone = await b.newPage({ viewport: { width: 390, height: 900 } })
const shoot = async () => {
  for (const [p, w] of [[wide, 1440], [phone, 390]]) {
    await p.goto(url + "#"); await p.waitForTimeout(900)
    await p.screenshot({ path: `ontology/shots/live-${w}.png`, fullPage: w === 1440 })
  }
  await wide.bringToFront(); console.log("shown", new Date().toLocaleTimeString())
}
await shoot()
let t; watch(file, () => { clearTimeout(t); t = setTimeout(shoot, 400) })
