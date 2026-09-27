const NS = "http://www.w3.org/2000/svg";
const CYAN = "rgb(103 232 249)";
const TEXT = "rgb(230 233 239)";
const BG = "rgb(10 12 16)";
const root = document.getElementById("root");
const DOT = String.fromCharCode(183);

function el(name, attrs, parent) {
  const node = document.createElementNS(NS, name);
  for (const k in attrs) node.setAttribute(k, attrs[k]);
  if (parent) parent.appendChild(node);
  return node;
}

function html(tag, cls, text, parent) {
  const node = document.createElement(tag);
  if (cls) node.className = cls;
  if (text) node.textContent = text;
  if (parent) parent.appendChild(node);
  return node;
}

// logo: the word "90" plus a cyan x made of two strokes
function drawLogo(px, withTile, animate) {
  const svg = el("svg", { width: px, height: px, viewBox: "0 0 100 100", class: "logo" });
  if (withTile) el("rect", { width: 100, height: 100, rx: 22, fill: BG }, svg);
  const word = el("text", { x: 16, y: 62, "text-anchor": "start", "font-family": "Sora, sans-serif", "font-weight": 700, "font-size": 38, fill: TEXT }, svg);
  word.textContent = "90";
  addStroke(svg, 0, 0, 0, 0, animate ? "s s1" : "");
  addStroke(svg, 0, 0, 0, 0, animate ? "s s2" : "");
  return svg;
}

// Place "90" and the x from measured Sora glyphs (see layoutLogos below).
const FONT_SIZE = 38;
const BASELINE = 62;
const STROKE = 6;

function measureMark() {
  const ctx = document.createElement("canvas").getContext("2d");
  ctx.font = `700 ${FONT_SIZE}px Sora`;
  const nine = ctx.measureText("90");
  const ex = ctx.measureText("x");
  return {
    inkLeft: nine.actualBoundingBoxLeft,
    inkWidth: nine.actualBoundingBoxLeft + nine.actualBoundingBoxRight,
    capHeight: nine.actualBoundingBoxAscent,
    xHeight: ex.actualBoundingBoxAscent,
  };
}
// The x is as tall as Sora's own x-height, sits on the same baseline, and
// starts a fixed gap after the ink of the "0". The whole mark is centred.
function layoutLogos() {
  const m = measureMark();
  const gap = FONT_SIZE * 0.14;
  const xSize = m.xHeight;
  const total = m.inkWidth + gap + xSize;
  const left = (100 - total) / 2;
  const baseline = 50 + m.capHeight / 2;
  const xLeft = left + m.inkWidth + gap;
  const inset = STROKE / 2;
  const a = { x: xLeft + inset, y: baseline - xSize + inset };
  const b = { x: xLeft + xSize - inset, y: baseline - inset };
  for (const svg of document.querySelectorAll("svg.logo")) {
    const word = svg.querySelector("text");
    word.setAttribute("x", left + m.inkLeft);
    word.setAttribute("y", baseline);
    const [one, two] = svg.querySelectorAll("line");
    setLine(one, a.x, a.y, b.x, b.y);
    setLine(two, b.x, a.y, a.x, b.y);
    svg.style.visibility = "visible";
  }
}

function setLine(seg, x1, y1, x2, y2) {
  seg.setAttribute("x1", x1);
  seg.setAttribute("y1", y1);
  seg.setAttribute("x2", x2);
  seg.setAttribute("y2", y2);
}

function addStroke(svg, ax, ay, bx, by, cls) {
  const seg = el("line", { stroke: CYAN, "stroke-width": 6, "stroke-linecap": "round" }, svg);
  seg.setAttribute("x1", ax);
  seg.setAttribute("y1", ay);
  seg.setAttribute("x2", bx);
  seg.setAttribute("y2", by);
  if (cls) seg.setAttribute("class", cls);
}

// Header
const head = html("div", "", "", root);
head.style.cssText = "display:flex;flex-direction:column;gap:8px";
html("span", "muted", "Final direction A: the wordmark", head);
const h1 = html("h1", "", "90", head);
html("span", "cyan", "x", h1);
html("h1", "", "", head).remove();
h1.append(" icon and splash");
html("p", "", "The wordmark everywhere: app icon, favicon, iOS launch screen, loading splash and link card. The x is two cyan strokes, so the splash can draw it in.", head);

// Icon sizes
const s1 = html("section", "", "", root);
html("h2", "", "App icon and favicon", s1);
const sizeCard = html("div", "card", "", s1);
const sizes = html("div", "sizes", "", sizeCard);
for (const [px, label] of [[128, "Home screen"], [64, "64px"], [32, "32px"], [16, "16px tab"]]) {
  const cell = html("div", "", "", sizes);
  cell.appendChild(drawLogo(px, true, false));
  html("span", "", label, cell);
}
const tabs = html("div", "tabs", "", sizeCard);
html("div", "tab", "Inbox", tabs);
const onTab = html("div", "tab on", "", tabs);
onTab.appendChild(drawLogo(16, true, false));
onTab.append("Today " + DOT + " 90x");
html("div", "tab", "LeetCode", tabs);
// Phones: home screen, iOS launch image, animated splash
const s2 = html("section", "", "", root);
html("h2", "", "On the phone", s2);
const phones = html("div", "phones", "", s2);
const home = html("div", "phone home", "", phones);
const names = ["Photos", "Mail", "90x", "Maps", "Notes", "Music", "Slack", "Clock"];
for (const n of names) {
  const a = html("div", "app", "", home);
  const ico = html("div", "ico", "", a);
  if (n === "90x") ico.appendChild(drawLogo(44, true, false));
  else ico.classList.add("blank");
  html("span", "", n, a);
}
const launch = html("div", "phone", "", phones);
const launchIn = html("div", "center", "", launch);
launchIn.appendChild(drawLogo(110, false, false));

const splashPhone = html("div", "phone", "", phones);
const splashIn = html("div", "center", "", splashPhone);
const splash = html("div", "splash", "", splashIn);
splash.appendChild(drawLogo(120, false, true));
const bar = html("div", "bar", "", splash);
html("i", "", "", bar);
const note = html("div", "card", "", s2);
html("p", "", "Left: the home screen icon. Middle: the iOS launch image, shown instantly on a cold start so there's no white flash. Right: the in-app loading splash. The 90 fades in, the x draws its two strokes, then a thin progress line runs until the app is ready (2.5 s at most, once per session).", note);
const replay = html("button", "", "Replay splash", note);
replay.type = "button";
function play() {
  splash.classList.remove("go");
  void splash.offsetWidth;
  splash.classList.add("go");
}
replay.addEventListener("click", play);
// play() runs after layout, below
// Link card
const s3 = html("section", "", "", root);
html("h2", "", "Shared-link card", s3);
const og = html("div", "og", "", s3);
og.appendChild(drawLogo(150, true, false));
const ogText = html("div", "", "", og);
html("div", "og-t", "Interview-ready in 90 days.", ogText);
html("div", "og-sub", "With friends " + DOT + " 90x.amanarya.com", ogText);
html("p", "muted", "What shows when a 90x link is pasted into WhatsApp or Slack.", s3);

// Measure only once Sora has loaded: fallback glyphs have other widths.
document.fonts.load(`700 ${FONT_SIZE}px Sora`).then(() => document.fonts.ready).then(() => {
  layoutLogos();
  play();
});
