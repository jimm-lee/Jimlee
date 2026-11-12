// Render a carousel spec to Instagram-ready PNGs.
//   node render.mjs specs/my-carousel.json [--out out/my-carousel] [--no-counter]
// Image paths in the spec are relative to the spec file.

import { mkdir, readFile, rm, writeFile } from "node:fs/promises";
import path from "node:path";
import { createRequire } from "node:module";
import { fileURLToPath, pathToFileURL } from "node:url";

import { HEIGHT, WIDTH, expandSlides, slideHtml, validateSpec } from "./lib/slides.mjs";

// require() also finds a globally installed Playwright (NODE_PATH); ESM import doesn't.
const { chromium } = createRequire(import.meta.url)("playwright");

const HERE = path.dirname(fileURLToPath(import.meta.url));
const FONTS = path.resolve(HERE, "../../brand/fonts");
const RAW_EXTENSIONS = /\.(cr2|cr3|nef|arw|raf|orf|rw2|dng)$/i;
const STRIP_SCALE = 0.25;

function parseArgs(argv) {
  const [specPath, ...rest] = argv;
  if (!specPath) throw new Error("Usage: node render.mjs <spec.json> [--out dir] [--no-counter]");
  const outIndex = rest.indexOf("--out");
  const name = path.basename(specPath, ".json");
  return {
    specPath: path.resolve(specPath),
    out: path.resolve(outIndex >= 0 ? rest[outIndex + 1] : path.join(HERE, "out", name)),
    showCounter: !rest.includes("--no-counter"),
  };
}

// Point every image at an absolute file:// URL so the browser can load it.
function resolveImages(slide, base) {
  const fix = (src) => {
    if (!src) return src;
    if (RAW_EXTENSIONS.test(src)) throw new Error(`${src} is a RAW file; export it as JPEG first.`);
    return pathToFileURL(path.resolve(base, src)).href;
  };
  return { ...slide, image: fix(slide.image), images: slide.images?.map(fix) };
}

async function renderStrip(page, files, out) {
  const w = Math.round(WIDTH * STRIP_SCALE);
  const h = Math.round(HEIGHT * STRIP_SCALE);
  const imgs = files.map((f) => `<img src="${pathToFileURL(f).href}" width="${w}" height="${h}">`).join("");
  const html = `<!doctype html><body style="margin:0;background:#000;display:flex;gap:6px;padding:6px;width:max-content">${imgs}</body>`;
  const stripHtml = path.join(out, "_strip.html");
  await writeFile(stripHtml, html);
  await page.setViewportSize({ width: files.length * (w + 6) + 6, height: h + 12 });
  await page.goto(pathToFileURL(stripHtml).href, { waitUntil: "load" });
  await page.screenshot({ path: path.join(out, "preview-strip.png") });
  await rm(stripHtml);
}

async function main() {
  const { specPath, out, showCounter } = parseArgs(process.argv.slice(2));
  const spec = JSON.parse(await readFile(specPath, "utf8"));
  const problems = validateSpec(spec);
  if (problems.length) throw new Error(`Spec problems:\n- ${problems.join("\n- ")}`);

  const base = path.dirname(specPath);
  const slides = expandSlides(spec.slides).map((s) => resolveImages(s, base));
  await mkdir(out, { recursive: true });

  const browser = await chromium.launch();
  try {
    const page = await browser.newPage({ viewport: { width: WIDTH, height: HEIGHT }, deviceScaleFactor: 1 });
    const files = [];
    for (const [i, slide] of slides.entries()) {
      const html = slideHtml(slide, i, slides.length, {
        fontsUrl: pathToFileURL(FONTS).href,
        showCounter: showCounter && spec.counter !== false,
      });
      const htmlPath = path.join(out, `_slide.html`);
      await writeFile(htmlPath, html);
      await page.goto(pathToFileURL(htmlPath).href, { waitUntil: "load" });
      await page.evaluate(() => document.fonts.ready);
      const file = path.join(out, `${String(i + 1).padStart(2, "0")}.png`);
      await page.screenshot({ path: file });
      files.push(file);
      await rm(htmlPath);
    }
    await renderStrip(page, files, out);
    console.log(`${files.length} slides -> ${out}`);
  } finally {
    await browser.close();
  }
}

main().catch((error) => {
  console.error(error.message);
  process.exit(1);
});
