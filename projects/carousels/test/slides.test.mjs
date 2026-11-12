import { test } from "node:test";
import assert from "node:assert/strict";

import { accent, escapeHtml, expandSlides, slideHtml, validateSpec } from "../lib/slides.mjs";

const fonts = { fontsUrl: "file:///fonts" };

test("words between asterisks turn green", () => {
  assert.equal(accent("Every *hill* around here"), 'Every <span class="acc">hill</span> around here');
});

test("a new line in the text becomes a line break", () => {
  assert.equal(accent("30 KG.\n*EVERY* HILL."), '30 KG.<br><span class="acc">EVERY</span> HILL.');
});

test("text blocks can be moved, and fall back to the layout's default", () => {
  assert.match(slideHtml({ layout: "cover", image: "a", title: "x", position: "bottom" }, 0, 1, fonts), /block bottom/);
  assert.match(slideHtml({ layout: "cover", image: "a", title: "x", position: "sideways" }, 0, 1, fonts), /block centre/);
});

test("text is escaped so captions can't inject markup", () => {
  assert.equal(escapeHtml(`<b>"Mo" & co's</b>`), "&lt;b&gt;&quot;Mo&quot; &amp; co&#39;s&lt;/b&gt;");
  assert.ok(!slideHtml({ layout: "words", line: "<script>x</script>" }, 0, 1, fonts).includes("<script>x"));
});

test("a panorama spanning three slides becomes three slices", () => {
  const slides = expandSlides([{ layout: "cover", image: "a" }, { layout: "pano", image: "p", span: 3 }]);
  assert.equal(slides.length, 4);
  assert.deepEqual(slides.slice(1).map((s) => s.part), [0, 1, 2]);
  const last = slideHtml(slides[3], 3, 4, fonts);
  assert.match(last, /background-size:300% auto/);
  assert.match(last, /background-position:100%/);
});

test("validation catches the usual mistakes", () => {
  assert.deepEqual(validateSpec({ slides: [] }), ['The spec needs a non-empty "slides" list.']);
  const problems = validateSpec({
    slides: [
      { layout: "poster" },
      { layout: "pair", images: ["one"] },
      { layout: "pano", image: "p", span: 9 },
      { layout: "photo" },
    ],
  });
  assert.equal(problems.length, 4);
});

test("a valid spec has no problems", () => {
  const spec = { slides: [{ layout: "cover", image: "a", title: "HI" }, { layout: "words", line: "Hello" }] };
  assert.deepEqual(validateSpec(spec), []);
});

test("more than twenty slides after expanding panoramas is rejected", () => {
  const slides = Array.from({ length: 5 }, () => ({ layout: "pano", image: "p", span: 5 }));
  assert.match(validateSpec({ slides }).at(-1), /Instagram allows 20/);
});

test("slide counter shows position and can be turned off", () => {
  assert.match(slideHtml({ layout: "words", line: "x" }, 1, 7, fonts), /2 \/ 7/);
  assert.doesNotMatch(slideHtml({ layout: "words", line: "x" }, 1, 7, { ...fonts, showCounter: false }), /2 \/ 7/);
});
