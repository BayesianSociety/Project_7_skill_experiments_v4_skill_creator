const fs = require("fs");
const path = require("path");

const outDir = __dirname;

const slides = [
  {
    n: 1,
    headline: "Snowflake As AI Control Plane",
    supporting: "The moat is governed enterprise data, not just warehouse speed.",
    visual: "A central data-cloud control node coordinates calm streams of enterprise signals.",
    prompt: "Square 1:1 editorial Instagram image for investor research, central safe area with 15% padding, deep burgundy headline on warm paper background, Desert Rose palette, abstract enterprise data-cloud control node with flowing governed data streams, polished minimal data-art style, strong mobile contrast, no text near edges.",
    motif: "control",
    accent: "#b87d6d"
  },
  {
    n: 2,
    headline: "Research Tailwinds Are Strong",
    supporting: "AI data-cloud papers rose sharply from 2021 to 2025.",
    visual: "Five publication columns climb beneath a precise research signal line.",
    prompt: "Square 1:1 modern editorial data visual, high-contrast typography, five rising publication bars inside generous safe margins, Desert Rose palette with deep burgundy, clay, and restrained green signal line, mobile-safe centered composition.",
    motif: "bars",
    accent: "#2f7a69"
  },
  {
    n: 3,
    headline: "Patents Show Depth",
    supporting: "1,047 patent documents, but grants eased after the 2022 peak.",
    visual: "Patent documents form a structured archive with one amber slowdown marker.",
    prompt: "Square Instagram slide, minimal patent archive and database index forms, warm sand background, high contrast burgundy typography, amber caution marker, Desert Rose editorial investor-analysis style, generous central padding, no crowded typography.",
    motif: "patents",
    accent: "#9f6f2f"
  },
  {
    n: 4,
    headline: "Industrialization Is The Standout",
    supporting: "53 regions, three clouds, and productionized data-plus-AI services.",
    visual: "Three cloud planes connect to a global deployment grid and AI service layer.",
    prompt: "Square 1:1 editorial technology image, three abstract cloud planes connected to a global deployment grid, data and AI service layer, strong burgundy headline, dusty rose and clay infrastructure shapes, restrained green live-signal accents, high readability.",
    motif: "clouds",
    accent: "#5d2e46"
  },
  {
    n: 5,
    headline: "Adoption Has Real Pull",
    supporting: "13,328 customers and 125% retention signal repeatable demand.",
    visual: "Enterprise demand streams converge into a durable expansion loop.",
    prompt: "Square Instagram graphic, enterprise customer streams converging into a clean expansion loop, no brand logos, premium data-platform aesthetic, high contrast typography, Desert Rose palette with subtle green retention signal, centered safe-area layout.",
    motif: "loop",
    accent: "#2f7a69"
  },
  {
    n: 6,
    headline: "The Caveats Matter",
    supporting: "GAAP losses, hyperscaler dependence, and AI governance cap the score.",
    visual: "Three sober risk gates stand between platform scale and exceptional status.",
    prompt: "Square 1:1 image, three elegant analytical risk gates represented by simple symbols, warm sand paper surface, serious investor-analysis tone, high contrast burgundy text, Desert Rose palette, central safe area with generous margins.",
    motif: "gates",
    accent: "#9f6f2f"
  },
  {
    n: 7,
    headline: "Verdict: Strong Momentum",
    supporting: "19.4 / 25. Strong innovator, just below exceptional.",
    visual: "A readiness ring lands just under the exceptional mark.",
    prompt: "Square editorial score image, circular readiness ring around 19.4 / 25, small exceptional threshold mark, Desert Rose colors, calm premium finish, strong mobile readability, centered composition with generous margins, no edge text.",
    motif: "ring",
    accent: "#b87d6d"
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
  return wrapText(text, 18);
}

function supportingLines(text) {
  return wrapText(text, 36);
}

function motifSvg(slide) {
  const a = slide.accent;
  if (slide.motif === "control") {
    return `
      <g opacity="0.94">
        ${[0, 1, 2, 3, 4].map((i) => `<path d="M${160 + i * 150} 765 C${230 + i * 90} 590 ${370 + i * 62} 555 540 520" fill="none" stroke="${i % 2 ? "#d4a5a5" : "#2f7a69"}" stroke-width="${i % 2 ? 8 : 10}" stroke-linecap="round" stroke-opacity="${i % 2 ? 0.74 : 0.82}"/>`).join("")}
        <circle cx="540" cy="520" r="118" fill="#fff9f5" stroke="#5d2e46" stroke-width="8"/>
        <circle cx="540" cy="520" r="56" fill="${a}" fill-opacity="0.88"/>
        <path d="M500 520 H580 M540 480 V560" stroke="#fff9f5" stroke-width="12" stroke-linecap="round"/>
        ${[[250,745],[390,645],[690,650],[835,765]].map(([x,y]) => `<circle cx="${x}" cy="${y}" r="24" fill="#fff9f5" stroke="#5d2e46" stroke-width="5"/>`).join("")}
      </g>`;
  }
  if (slide.motif === "bars") {
    const values = [85, 108, 174, 186, 366];
    const max = 366;
    return `<g transform="translate(160 690)">
      ${values.map((v, i) => {
        const h = Math.round((v / max) * 285);
        return `<rect x="${i * 142}" y="${-h}" width="84" height="${h}" rx="6" fill="${i === 4 ? "#5d2e46" : "#d4a5a5"}"/>
        <text x="${i * 142 + 42}" y="46" text-anchor="middle" font-family="FreeSans, Arial" font-size="26" fill="#6f5d61">${2021 + i}</text>`;
      }).join("")}
      <path d="M42 -66 L184 -84 L326 -135 L468 -145 L610 -285" fill="none" stroke="${a}" stroke-width="9" stroke-linecap="round"/>
      <circle cx="610" cy="-285" r="16" fill="${a}"/>
    </g>`;
  }
  if (slide.motif === "patents") {
    return `<g transform="translate(540 575)">
      ${[-120, -60, 0, 60, 120].map((x, i) => `<rect x="${x - 150}" y="${-180 + i * 22}" width="300" height="380" rx="8" fill="#fff9f5" stroke="#5d2e46" stroke-opacity="${0.12 + i * 0.03}" stroke-width="3"/>`).join("")}
      <rect x="-180" y="-110" width="360" height="250" rx="8" fill="#fff9f5" stroke="#5d2e46" stroke-width="5"/>
      <rect x="-130" y="-60" width="210" height="18" fill="#d4a5a5"/>
      <rect x="-130" y="-12" width="255" height="10" fill="#5d2e46" fill-opacity="0.18"/>
      <rect x="-130" y="25" width="220" height="10" fill="#5d2e46" fill-opacity="0.18"/>
      <path d="M-105 92 H116" stroke="${a}" stroke-width="12" stroke-linecap="round"/>
      <circle cx="172" cy="-128" r="42" fill="${a}"/>
      <path d="M156 -128 H188" stroke="#fff9f5" stroke-width="8" stroke-linecap="round"/>
    </g>`;
  }
  if (slide.motif === "clouds") {
    return `<g opacity="0.96">
      ${[[250,610],[540,560],[830,610]].map(([x,y], i) => `
        <path d="M${x - 70} ${y + 20} Q${x - 54} ${y - 36} ${x + 8} ${y - 28} Q${x + 46} ${y - 80} ${x + 104} ${y - 28} Q${x + 160} ${y - 22} ${x + 164} ${y + 32} Z" fill="#fff9f5" stroke="${i === 1 ? "#5d2e46" : "#b87d6d"}" stroke-width="7"/>
        <circle cx="${x}" cy="${y + 105}" r="18" fill="${i === 1 ? "#2f7a69" : "#d4a5a5"}"/>
      `).join("")}
      <path d="M250 715 C375 790 690 790 830 715" fill="none" stroke="#5d2e46" stroke-opacity="0.28" stroke-width="9" stroke-linecap="round"/>
      <path d="M540 662 V810" stroke="${a}" stroke-width="8" stroke-linecap="round"/>
      <rect x="335" y="810" width="410" height="48" rx="8" fill="#5d2e46"/>
      <circle cx="390" cy="834" r="10" fill="#fff9f5"/>
      <circle cx="540" cy="834" r="10" fill="#fff9f5"/>
      <circle cx="690" cy="834" r="10" fill="#fff9f5"/>
    </g>`;
  }
  if (slide.motif === "loop") {
    return `<g transform="translate(540 620)">
      <path d="M-210 20 C-210 -130 -20 -180 90 -86 C185 -6 135 128 5 128 C-105 128 -160 70 -150 -10" fill="none" stroke="${a}" stroke-width="22" stroke-linecap="round"/>
      <path d="M86 -88 L172 -94 L142 -14" fill="none" stroke="${a}" stroke-width="18" stroke-linecap="round" stroke-linejoin="round"/>
      ${[[-320,-130],[-310,160],[300,-130],[310,155],[-15,-210]].map(([x,y], i) => `
        <path d="M${x} ${y} C${x * 0.58} ${y * 0.72} ${x * 0.2} ${y * 0.36} ${i === 4 ? 20 : 0} ${i === 4 ? -120 : 0}" fill="none" stroke="${i % 2 ? "#d4a5a5" : "#2f7a69"}" stroke-width="8" stroke-linecap="round" stroke-opacity="0.74"/>
        <circle cx="${x}" cy="${y}" r="30" fill="#fff9f5" stroke="#5d2e46" stroke-width="5"/>
      `).join("")}
    </g>`;
  }
  if (slide.motif === "gates") {
    return `<g transform="translate(145 630)">
      ${[0, 260, 520].map((x, i) => `
        <path d="M${x} 216 L${x} 48 Q${x + 58} -22 ${x + 116} 48 L${x + 116} 216" fill="none" stroke="${i === 1 ? a : "#d4a5a5"}" stroke-width="14" stroke-linecap="round"/>
        <circle cx="${x + 58}" cy="82" r="16" fill="${i === 2 ? "#2f7a69" : "#5d2e46"}"/>
        <path d="M${x + 36} 148 H${x + 80}" stroke="#5d2e46" stroke-opacity="0.28" stroke-width="8" stroke-linecap="round"/>
      `).join("")}
      <path d="M-35 262 C185 215 385 215 710 262" fill="none" stroke="#5d2e46" stroke-opacity="0.18" stroke-width="20" stroke-linecap="round"/>
    </g>`;
  }
  return `<g transform="translate(540 610)">
    <circle cx="0" cy="0" r="190" fill="none" stroke="#5d2e46" stroke-opacity="0.12" stroke-width="28"/>
    <path d="M0 -190 A190 190 0 1 1 -188 28" fill="none" stroke="${a}" stroke-width="28" stroke-linecap="round"/>
    <path d="M-35 -210 L35 -210" stroke="#9f6f2f" stroke-width="10" stroke-linecap="round"/>
    <text x="0" y="20" text-anchor="middle" font-family="FreeSans, Arial" font-size="74" font-weight="700" fill="#5d2e46">19.4</text>
    <text x="0" y="78" text-anchor="middle" font-family="FreeSans, Arial" font-size="30" font-weight="700" fill="#241b20">of 25</text>
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
  <circle cx="920" cy="130" r="210" fill="#d4a5a5" fill-opacity="0.24"/>
  <circle cx="130" cy="930" r="260" fill="#b87d6d" fill-opacity="0.13"/>
  ${motifSvg(slide)}
  <g transform="translate(145 140)">
    <text x="0" y="0" font-family="FreeSans, Arial" font-size="28" font-weight="700" letter-spacing="4" fill="#6f5d61">SNOWFLAKE INNOVATION</text>
    ${h.map((line, i) => `<text x="0" y="${84 + i * 78}" font-family="FreeSans, Arial" font-size="72" font-weight="700" fill="#5d2e46">${esc(line)}</text>`).join("")}
    <g transform="translate(0 ${108 + h.length * 78})">
      <rect x="0" y="-34" width="650" height="${62 + s.length * 38}" rx="8" fill="#fff9f5" fill-opacity="0.9"/>
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
  "# Snowflake Inc. Instagram Carousel",
  "",
  "## Carousel summary",
  "",
  "- The concept: Snowflake is a strong innovation story because governed enterprise data is becoming the control plane for AI.",
  "- The visual direction: Desert Rose editorial data-art with high-contrast burgundy typography, warm paper surfaces, and precise infrastructure motifs.",
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
