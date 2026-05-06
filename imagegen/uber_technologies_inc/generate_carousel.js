const fs = require("fs");
const path = require("path");

const outDir = __dirname;

const slides = [
  {
    n: 1,
    headline: "Uber's Hidden Engine",
    supporting: "The breakthrough is not the car. It is the marketplace layer.",
    visual: "A dense city grid resolves into one glowing dispatch node.",
    prompt: "Square 1:1 editorial Instagram image, central safe area with 15% padding, deep burgundy headline text on warm paper background, Desert Rose palette, city grid lines converging into a glowing dispatch node, premium minimal data-art style, high contrast, no text near edges.",
    motif: "network",
    accent: "#b87d6d"
  },
  {
    n: 2,
    headline: "Science Is Moving",
    supporting: "AV dispatch research rose from 100 to 146 works.",
    visual: "A clean publication trend climbs across five restrained columns.",
    prompt: "Square 1:1 modern editorial data visual, high-contrast typography, five rising publication bars inside safe margins, Desert Rose with deep burgundy and clay, subtle university-paper texture, mobile-safe centered composition.",
    motif: "bars",
    accent: "#5d2e46"
  },
  {
    n: 3,
    headline: "IP Is Not The Moat",
    supporting: "A large patent footprint, but weak evidence of acceleration.",
    visual: "Patent pages stack behind a single caution line.",
    prompt: "Square Instagram slide, minimal patent-document stack, one precise caution line, warm sand background, burgundy and muted rose accents, high readability, generous central padding, no crowded typography.",
    motif: "papers",
    accent: "#9f6f2f"
  },
  {
    n: 4,
    headline: "Scale Changes The Math",
    supporting: "13.6B trips give algorithms a live learning surface.",
    visual: "Billions of trips abstracted as flowing routes over a calm map.",
    prompt: "Square 1:1 editorial technology image, flowing route lines across an abstract city map, large clear headline, Desert Rose palette plus restrained green signal color, premium operational dashboard energy without UI frames, strong contrast.",
    motif: "routes",
    accent: "#2f7a69"
  },
  {
    n: 5,
    headline: "AV Partners Need Demand",
    supporting: "Waymo, VW, May Mobility and NVIDIA plug into distribution.",
    visual: "Four partner streams feed one central marketplace hub.",
    prompt: "Square Instagram graphic, four clean streams feeding a central marketplace hub, no brand logos, editorial tech aesthetic, high contrast deep burgundy text, dusty rose and clay forms, centered safe-area layout.",
    motif: "hub",
    accent: "#b87d6d"
  },
  {
    n: 6,
    headline: "The Hard Part Remains",
    supporting: "Policy, labor and AV economics still decide the upside.",
    visual: "Three gates stand between the platform and a clear road.",
    prompt: "Square 1:1 image, three elegant gate shapes labeled by visual symbols only, road-like path, restrained Desert Rose palette, serious investor-analysis tone, high-contrast text in central safe area.",
    motif: "gates",
    accent: "#5d2e46"
  },
  {
    n: 7,
    headline: "Verdict: Momentum",
    supporting: "16.4 / 25. Strong innovator, not yet exceptional.",
    visual: "A circular score mark stabilizes at two-thirds full.",
    prompt: "Square editorial score image, circular readiness ring around 16.4 / 25, Desert Rose colors, calm premium finish, strong mobile readability, centered composition with generous margins, no edge text.",
    motif: "ring",
    accent: "#2f7a69"
  }
];

function esc(s) {
  return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

function wrapText(text, maxChars) {
  const words = text.split(" ");
  const lines = [];
  let line = "";
  for (const word of words) {
    const candidate = line ? `${line} ${word}` : word;
    if (candidate.length > maxChars && line) {
      lines.push(line);
      line = word;
    } else {
      line = candidate;
    }
  }
  if (line) lines.push(line);
  return lines;
}

function headlineLines(text) {
  return wrapText(text, 17);
}

function supportingLines(text) {
  return wrapText(text, 35);
}

function motifSvg(slide) {
  const a = slide.accent;
  if (slide.motif === "network") {
    return `
      <g opacity="0.9">
        ${Array.from({ length: 9 }, (_, i) => `<path d="M${150 + i * 95} 230 L${300 + i * 54} 770" stroke="#5d2e46" stroke-opacity="0.09" stroke-width="2"/>`).join("")}
        ${Array.from({ length: 7 }, (_, i) => `<path d="M160  ${260 + i * 70} L930 ${220 + i * 62}" stroke="#5d2e46" stroke-opacity="0.08" stroke-width="2"/>`).join("")}
        <circle cx="730" cy="405" r="78" fill="${a}" fill-opacity="0.18"/>
        <circle cx="730" cy="405" r="24" fill="${a}"/>
        <path d="M350 690 C470 535 610 510 730 405 C790 355 846 322 910 280" fill="none" stroke="${a}" stroke-width="10" stroke-linecap="round"/>
        <path d="M285 340 C410 390 522 382 730 405" fill="none" stroke="#2f7a69" stroke-width="7" stroke-linecap="round" stroke-opacity="0.82"/>
      </g>`;
  }
  if (slide.motif === "bars") {
    const values = [100, 100, 144, 132, 146];
    const max = 146;
    return `<g transform="translate(170 615)">
      ${values.map((v, i) => {
        const h = Math.round((v / max) * 230);
        return `<rect x="${i * 132}" y="${-h}" width="78" height="${h}" rx="6" fill="${i === 4 ? "#5d2e46" : "#d4a5a5"}"/>
        <text x="${i * 132 + 39}" y="44" text-anchor="middle" font-family="FreeSans, Arial" font-size="26" fill="#6f5d61">${2021 + i}</text>`;
      }).join("")}
      <path d="M39 -157 L171 -157 L303 -226 L435 -208 L567 -230" fill="none" stroke="#2f7a69" stroke-width="8" stroke-linecap="round"/>
    </g>`;
  }
  if (slide.motif === "papers") {
    return `<g transform="translate(570 270) rotate(-5)">
      <rect x="-190" y="40" width="410" height="520" rx="10" fill="#fff9f5" stroke="#5d2e46" stroke-opacity="0.22" stroke-width="3"/>
      <rect x="-150" y="92" width="240" height="20" fill="#d4a5a5"/>
      <rect x="-150" y="150" width="315" height="10" fill="#5d2e46" fill-opacity="0.18"/>
      <rect x="-150" y="188" width="280" height="10" fill="#5d2e46" fill-opacity="0.18"/>
      <rect x="-150" y="226" width="330" height="10" fill="#5d2e46" fill-opacity="0.18"/>
      <path d="M-120 388 L170 388" stroke="${a}" stroke-width="12" stroke-linecap="round"/>
      <path d="M-115 432 L125 432" stroke="#2f7a69" stroke-width="8" stroke-linecap="round" stroke-opacity="0.72"/>
    </g>`;
  }
  if (slide.motif === "routes") {
    return `<g opacity="0.95">
      <path d="M125 620 C260 450 420 750 550 560 S790 340 955 530" fill="none" stroke="${a}" stroke-width="12" stroke-linecap="round"/>
      <path d="M185 790 C330 700 410 595 525 600 S690 715 860 650" fill="none" stroke="#5d2e46" stroke-width="7" stroke-linecap="round" stroke-opacity="0.55"/>
      <path d="M160 370 C330 260 490 390 610 330 S785 205 930 300" fill="none" stroke="#d4a5a5" stroke-width="9" stroke-linecap="round"/>
      ${[[125,620],[550,560],[955,530],[185,790],[860,650],[610,330]].map(([x,y]) => `<circle cx="${x}" cy="${y}" r="16" fill="#fff9f5" stroke="#5d2e46" stroke-width="5"/>`).join("")}
    </g>`;
  }
  if (slide.motif === "hub") {
    return `<g transform="translate(540 565)">
      <circle cx="0" cy="0" r="78" fill="#5d2e46"/>
      <circle cx="0" cy="0" r="32" fill="#fff9f5"/>
      ${[[-280,-160],[-255,150],[275,-150],[285,145]].map(([x,y], i) => `
        <path d="M${x} ${y} C${x * 0.55} ${y * 0.8} ${x * 0.28} ${y * 0.36} 0 0" fill="none" stroke="${i % 2 ? "#2f7a69" : a}" stroke-width="12" stroke-linecap="round"/>
        <circle cx="${x}" cy="${y}" r="42" fill="#fff9f5" stroke="${i % 2 ? "#2f7a69" : a}" stroke-width="8"/>
      `).join("")}
    </g>`;
  }
  if (slide.motif === "gates") {
    return `<g transform="translate(135 610)">
      ${[0, 260, 520].map((x, i) => `
        <path d="M${x} 210 L${x} 40 Q${x + 58} -20 ${x + 116} 40 L${x + 116} 210" fill="none" stroke="${i === 1 ? a : "#d4a5a5"}" stroke-width="14" stroke-linecap="round"/>
        <circle cx="${x + 58}" cy="76" r="16" fill="${i === 2 ? "#2f7a69" : "#5d2e46"}"/>
      `).join("")}
      <path d="M-35 255 C185 210 385 210 710 255" fill="none" stroke="#5d2e46" stroke-opacity="0.18" stroke-width="20" stroke-linecap="round"/>
    </g>`;
  }
  return `<g transform="translate(540 585)">
    <circle cx="0" cy="0" r="185" fill="none" stroke="#5d2e46" stroke-opacity="0.12" stroke-width="28"/>
    <path d="M0 -185 A185 185 0 1 1 -155 100" fill="none" stroke="${a}" stroke-width="28" stroke-linecap="round"/>
    <text x="0" y="22" text-anchor="middle" font-family="FreeSans, Arial" font-size="70" font-weight="700" fill="#5d2e46">16.4</text>
    <text x="0" y="78" text-anchor="middle" font-family="FreeSans, Arial" font-size="30" fill="#6f5d61">of 25</text>
  </g>`;
}

function slideSvg(slide) {
  const h = headlineLines(slide.headline);
  const s = supportingLines(slide.supporting);
  return `<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="1080" height="1080" viewBox="0 0 1080 1080">
  <defs>
    <linearGradient id="bg" x1="0" x2="1" y1="0" y2="1">
      <stop offset="0" stop-color="#fff9f5"/>
      <stop offset="0.58" stop-color="#f4e3dc"/>
      <stop offset="1" stop-color="#e8d5c4"/>
    </linearGradient>
    <pattern id="grid" width="72" height="72" patternUnits="userSpaceOnUse">
      <path d="M72 0 H0 V72" fill="none" stroke="#5d2e46" stroke-width="1" stroke-opacity="0.055"/>
    </pattern>
  </defs>
  <rect width="1080" height="1080" fill="url(#bg)"/>
  <rect width="1080" height="1080" fill="url(#grid)"/>
  <circle cx="930" cy="130" r="210" fill="#d4a5a5" fill-opacity="0.24"/>
  <circle cx="120" cy="930" r="260" fill="#b87d6d" fill-opacity="0.14"/>
  ${motifSvg(slide)}
  <g transform="translate(145 140)">
    <text x="0" y="0" font-family="FreeSans, Arial" font-size="28" font-weight="700" letter-spacing="4" fill="#6f5d61">UBER INNOVATION</text>
    ${h.map((line, i) => `<text x="0" y="${84 + i * 78}" font-family="FreeSans, Arial" font-size="72" font-weight="700" fill="#5d2e46">${esc(line)}</text>`).join("")}
    <g transform="translate(0 ${108 + h.length * 78})">
      <rect x="0" y="-34" width="620" height="${62 + s.length * 38}" rx="10" fill="#fff9f5" fill-opacity="0.82"/>
      ${s.map((line, i) => `<text x="28" y="${22 + i * 38}" font-family="FreeSans, Arial" font-size="31" font-weight="700" fill="#241b20">${esc(line)}</text>`).join("")}
    </g>
  </g>
  <g transform="translate(145 950)">
    <rect x="0" y="0" width="160" height="8" rx="4" fill="${slide.accent}"/>
    <text x="186" y="12" font-family="FreeSans, Arial" font-size="26" font-weight="700" fill="#5d2e46">Slide ${slide.n} / 7</text>
  </g>
</svg>`;
}

for (const slide of slides) {
  const name = `slide-${String(slide.n).padStart(2, "0")}`;
  fs.writeFileSync(path.join(outDir, `${name}.svg`), slideSvg(slide));
}

const summary = [
  "# Uber Technologies Instagram Carousel",
  "",
  "## Carousel summary",
  "",
  "- The concept: Uber's innovation story is a marketplace engine with AV optionality, not a pure autonomy invention story.",
  "- The visual direction: Desert Rose editorial data-art with high-contrast burgundy typography, warm paper surfaces, and clean operational motifs.",
  "",
  "## Slides",
  "",
  ...slides.flatMap((slide) => [
    `Slide ${slide.n}`,
    `Headline: ${slide.headline}`,
    `Supporting text: ${slide.supporting}`,
    `Visual suggestion: ${slide.visual}`,
    `Image prompt: ${slide.prompt}`,
    ""
  ]),
  "## Assets",
  "",
  ...slides.map((slide) => `- slide-${String(slide.n).padStart(2, "0")}.png`)
].join("\n");

fs.writeFileSync(path.join(outDir, "carousel-summary.md"), summary);
