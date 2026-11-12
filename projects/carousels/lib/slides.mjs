// Turns a carousel spec into one HTML page per slide, in the house style (brand/).
// Pure functions only: rendering to PNG happens in render.mjs.

export const WIDTH = 1080;
export const HEIGHT = 1350; // Instagram portrait, 4:5

const LAYOUTS = new Set(["cover", "photo", "stat", "pair", "pano", "words", "ask"]);

export function escapeHtml(text) {
  return String(text ?? "")
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#39;");
}

// "Every *hill* around here" -> Every <span class="acc">hill</span> around here
export function accent(text) {
  return escapeHtml(text)
    .replace(/\*([^*]+)\*/g, '<span class="acc">$1</span>')
    .replaceAll("\n", "<br>");
}

// Check a spec and return a list of problems (empty when it's fine).
export function validateSpec(spec) {
  const problems = [];
  if (!spec || !Array.isArray(spec.slides) || spec.slides.length === 0) {
    return ["The spec needs a non-empty \"slides\" list."];
  }
  spec.slides.forEach((slide, i) => {
    const where = `Slide ${i + 1}`;
    if (!LAYOUTS.has(slide.layout)) problems.push(`${where}: unknown layout "${slide.layout}".`);
    if (slide.layout === "pair" && (!Array.isArray(slide.images) || slide.images.length !== 2)) {
      problems.push(`${where}: "pair" needs exactly two images.`);
    }
    if (slide.layout === "pano" && !(Number.isInteger(slide.span) && slide.span >= 2 && slide.span <= 5)) {
      problems.push(`${where}: "pano" needs "span" between 2 and 5.`);
    }
    if (["cover", "photo", "stat", "pano"].includes(slide.layout) && !slide.image) {
      problems.push(`${where}: "${slide.layout}" needs an "image".`);
    }
  });
  const total = expandSlides(spec.slides).length;
  if (total > 20) problems.push(`That's ${total} slides; Instagram allows 20.`);
  return problems;
}

// A panorama spanning N slides becomes N slides, each showing its slice of the image.
export function expandSlides(slides) {
  return slides.flatMap((slide) => {
    if (slide.layout !== "pano") return [slide];
    return Array.from({ length: slide.span }, (_, part) => ({ ...slide, part }));
  });
}

function photo(src, focus = "50% 50%") {
  return `<div class="photo" style="background-image:url('${escapeHtml(src)}');background-position:${escapeHtml(focus)}"></div>`;
}

// Where the text block sits: "top", "centre" or "bottom" (each layout has a default).
function place(slide, fallback) {
  return ["top", "centre", "bottom"].includes(slide.position) ? slide.position : fallback;
}

function kicker(text) {
  return text ? `<div class="kick">${escapeHtml(text)}</div>` : "";
}

function counter(index, total, show) {
  return show ? `<div class="count">${index + 1} / ${total}</div>` : "";
}

const BODIES = {
  cover: (s) => `${photo(s.image, s.focus)}<div class="shade"></div>
    <div class="block ${place(s, "centre")}">${kicker(s.kicker)}<div class="t l">${accent(s.title)}</div>
    ${s.line ? `<div class="t s line">${accent(s.line)}</div>` : ""}</div>
    <div class="swipe">Swipe &rarr;</div>`,

  photo: (s) => `${photo(s.image, s.focus)}<div class="shade"></div>
    <div class="block ${place(s, "top")}">${kicker(s.kicker)}
    ${s.line ? `<div class="t m">${accent(s.line)}</div>` : ""}</div>`,

  stat: (s) => `${photo(s.image, s.focus)}<div class="shade heavy"></div>
    <div class="block ${place(s, "centre")}">${kicker(s.kicker)}<div class="t xl">${accent(s.value)}</div>
    <div class="bar"></div>${s.line ? `<div class="t s line">${accent(s.line)}</div>` : ""}</div>`,

  pair: (s) => `<div class="pair">${photo(s.images[0], s.focus?.[0])}${photo(s.images[1], s.focus?.[1])}</div>
    <div class="shade"></div><div class="block top">${kicker(s.kicker)}
    ${s.line ? `<div class="t m">${accent(s.line)}</div>` : ""}</div>`,

  pano: (s) => `<div class="photo" style="background-image:url('${escapeHtml(s.image)}');
    background-size:${s.span * 100}% auto;background-position:${s.span === 1 ? 0 : (s.part / (s.span - 1)) * 100}% ${escapeHtml(s.focusY ?? "50%")}"></div>
    ${s.part === 0 && (s.line || s.kicker) ? `<div class="shade"></div><div class="block top">${kicker(s.kicker)}
    ${s.line ? `<div class="t m">${accent(s.line)}</div>` : ""}</div>` : ""}`,

  words: (s) => `${s.image ? `${photo(s.image, s.focus)}<div class="blur"></div>` : ""}
    <div class="block centre words">${kicker(s.kicker)}<div class="t m">${accent(s.line)}</div>
    ${s.small ? `<div class="small">${accent(s.small)}</div>` : ""}</div>`,

  ask: (s) => `${s.image ? `${photo(s.image, s.focus)}<div class="blur"></div>` : ""}
    <div class="block centre">${kicker(s.kicker)}<div class="t l">${accent(s.title)}</div><div class="bar"></div>
    ${s.line ? `<div class="t s line">${accent(s.line)}</div>` : ""}
    ${s.link ? `<div class="link">${escapeHtml(s.link)}</div>` : ""}</div>`,
};

export function slideHtml(slide, index, total, { fontsUrl, showCounter = true }) {
  return `<!doctype html><html><head><meta charset="utf-8"><style>${css(fontsUrl)}</style></head>
<body><div class="slide">${BODIES[slide.layout](slide)}${counter(index, total, showCounter)}</div></body></html>`;
}

export function css(fontsUrl) {
  return `
@font-face { font-family: "Merienda"; src: url("${fontsUrl}/Merienda-var.woff2") format("woff2"); font-weight: 300 900; }
@font-face { font-family: "Outfit"; src: url("${fontsUrl}/Outfit-var.woff2") format("woff2"); font-weight: 100 900; }
:root { --accent:#75ff78; --ink:#fff; --shadow:4px 6px 0 rgba(0,0,0,.28), 6px 8px 12px rgba(0,0,0,.35); }
* { margin:0; padding:0; box-sizing:border-box; }
body { width:${WIDTH}px; height:${HEIGHT}px; background:#111; overflow:hidden; }
.slide { position:relative; width:${WIDTH}px; height:${HEIGHT}px; overflow:hidden; background:#151515; }
.photo { position:absolute; inset:0; background-size:cover; background-repeat:no-repeat; }
.pair { position:absolute; inset:0; display:grid; grid-template-rows:1fr 1fr; gap:10px; background:#111; }
.pair .photo { position:relative; inset:auto; }
.shade { position:absolute; inset:0; background:linear-gradient(180deg, rgba(0,0,0,.55) 0%, rgba(0,0,0,0) 32%, rgba(0,0,0,0) 60%, rgba(0,0,0,.6) 100%); }
.shade.heavy { background:rgba(0,0,0,.42); }
.blur { position:absolute; inset:-40px; backdrop-filter:blur(28px) brightness(.55); }
.block { position:absolute; left:90px; right:90px; display:flex; flex-direction:column; gap:26px; align-items:center; text-align:center; }
.block.top { top:110px; } .block.bottom { bottom:130px; }
.block.centre { top:50%; transform:translateY(-50%); }
.t { font-family:"Merienda",cursive; font-weight:900; line-height:1.08; color:var(--ink); text-shadow:var(--shadow); }
.xl { font-size:190px; } .l { font-size:112px; } .m { font-size:76px; } .s { font-size:54px; }
.line { font-weight:800; }
.acc { color:var(--accent); }
.kick { font-family:"Outfit"; font-weight:500; font-size:32px; letter-spacing:11px; text-transform:uppercase; color:var(--ink); text-shadow:var(--shadow); }
.bar { height:6px; width:320px; background:var(--accent); box-shadow:4px 6px 10px rgba(0,0,0,.35); }
.small, .link { font-family:"Outfit"; font-weight:500; font-size:38px; color:#ffffffd9; text-shadow:var(--shadow); line-height:1.35; }
.link { color:var(--accent); letter-spacing:1px; }
.swipe, .count { position:absolute; font-family:"Outfit"; font-weight:500; font-size:28px; letter-spacing:6px; text-transform:uppercase; color:#ffffffd9; text-shadow:var(--shadow); }
.swipe { right:70px; bottom:70px; } .count { right:60px; top:56px; }
`;
}
