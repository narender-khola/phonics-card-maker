#!/usr/bin/env python3
"""
Phonics flash-card generator.
-----------------------------------------------------------------------------
HOW TO MAKE A NEW SET (e.g. the /s/ sound with snake + sun):

1. Drop your photos into the  images/  folder (square-ish photos look best).
2. Edit the CONFIG block below:
       - SOUND      -> the letter/sound, e.g. "s"
       - TITLE_NOTE -> the little line under the sound (optional)
       - ITEMS      -> one entry per card: a name + a list of photo files.
                       List several files per card to give "more options"
                       you can flip through in the browser.
3. Run:   python3 make_cards.py
4. Open the generated  cards.html  in a browser.
       - Use the ‹ › arrows on a card to pick a different photo.
       - Click "Download card" to save a single card as a PNG.
       - Click "Print cut sheet" (or Ctrl/Cmd-P) for a photo-size sheet
         with dashed cut lines — print, then cut along the lines.

Photos here are cropped square automatically by the browser (object-fit).
No internet or extra libraries needed — the images get baked into cards.html.
=============================================================================
"""

import base64
import json
import mimetypes
import os
import sys

# ============================ CONFIG =========================================
SOUND = "f"
TITLE_NOTE = "Both words start with the /f/ sound."

ITEMS = [
    {"name": "Fox",     "images": ["fox-1.jpg", "fox-2.jpg", "fox-3.jpg"]},
    {"name": "Feather", "images": ["feather-1.jpg", "feather-2.jpg", "feather-3.jpg"]},
]

OUTPUT = "cards.html"          # generated file
IMAGES_DIR = "images"          # where the photos live
# =============================================================================


def data_uri(path):
    mime = mimetypes.guess_type(path)[0] or "image/jpeg"
    with open(path, "rb") as fh:
        b64 = base64.b64encode(fh.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def build_items():
    here = os.path.dirname(os.path.abspath(__file__))
    items = []
    for it in ITEMS:
        uris = []
        for fname in it["images"]:
            p = os.path.join(here, IMAGES_DIR, fname)
            if not os.path.exists(p):
                sys.exit(f"ERROR: image not found: {p}")
            uris.append(data_uri(p))
        items.append({"name": it["name"], "images": uris})
    return items


def main():
    items = build_items()
    payload = {"sound": SOUND, "note": TITLE_NOTE, "items": items}
    html = TEMPLATE.replace("/*__DATA__*/ null", json.dumps(payload))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), OUTPUT)
    with open(out, "w") as fh:
        fh.write(html)
    kb = os.path.getsize(out) // 1024
    print(f"Wrote {OUTPUT} ({kb} KB) with {len(items)} cards for sound /{SOUND}/.")
    print(f"Open it in a browser: {out}")


TEMPLATE = r"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Phonics cards</title>
<style>
  :root {
    --paper: #fffaf2;
    --ink: #3a2e26;
    --muted: #8a7a6d;
    --accent: #e8622a;
    --accent-deep: #c74d18;
    --card: #ffffff;
    --line: #ecdfce;
    /* one printed card = photo size. Change these to resize the cut cards. */
    --card-w: 3.4in;
    --card-h: 4.4in;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0;
    background:
      radial-gradient(circle at 18% 12%, #fff1dc 0, transparent 42%),
      radial-gradient(circle at 88% 85%, #ffe9d8 0, transparent 45%),
      var(--paper);
    color: var(--ink);
    font-family: "Trebuchet MS", "Segoe UI", system-ui, sans-serif;
    min-height: 100vh;
  }

  /* ---------- screen toolbar ---------- */
  .bar {
    position: sticky; top: 0; z-index: 5;
    display: flex; flex-wrap: wrap; align-items: center; gap: 14px;
    padding: 16px 22px;
    background: rgba(255,250,242,.9);
    backdrop-filter: blur(6px);
    border-bottom: 1px solid var(--line);
  }
  .bar h1 { margin: 0; font-size: 20px; font-weight: 800; }
  .bar .snd {
    display: inline-block; background: var(--ink); color: var(--paper);
    border-radius: 9px; padding: 0 .32em; transform: rotate(-3deg);
  }
  .bar .spacer { flex: 1; }
  .btn {
    font: inherit; font-weight: 700; font-size: 15px;
    border: 2px solid var(--accent); color: #fff; background: var(--accent);
    padding: 9px 16px; border-radius: 999px; cursor: pointer;
    transition: transform .08s ease, background .15s ease;
  }
  .btn:hover { background: var(--accent-deep); border-color: var(--accent-deep); }
  .btn:active { transform: translateY(1px); }
  .btn.ghost { background: #fff; color: var(--accent-deep); }
  .btn:focus-visible { outline: 3px solid #ffbf9a; outline-offset: 2px; }

  .hint { padding: 14px 22px 0; color: var(--muted); font-size: 14px; }

  /* ---------- the sheet of cards ---------- */
  .sheet {
    display: flex; flex-wrap: wrap; gap: 26px;
    justify-content: center;
    padding: 26px 22px 60px;
  }
  .card {
    position: relative;
    width: var(--card-w); height: var(--card-h);
    background: var(--card);
    border: 2px dashed #d9c7b2;      /* dashed = cut line */
    border-radius: 16px;
    padding: .22in;
    display: flex; flex-direction: column; gap: .18in;
    box-shadow: 0 16px 30px -20px rgba(90,50,20,.5);
  }
  /* corner crop marks */
  .card::before, .card::after {
    content: ""; position: absolute; width: 12px; height: 12px;
    border: 2px solid #caa; opacity: .5;
  }
  .card::before { top: -2px; left: -2px; border-right: 0; border-bottom: 0; }
  .card::after  { bottom: -2px; right: -2px; border-left: 0; border-top: 0; }

  .badge {
    position: absolute; top: .34in; left: .34in;
    background: var(--ink); color: var(--paper);
    font-weight: 800; font-size: 15px;
    border-radius: 8px; padding: 2px 9px; transform: rotate(-4deg);
    z-index: 2;
  }
  .photo {
    flex: 1 1 auto; min-height: 0;
    border-radius: 12px; overflow: hidden;
    background: linear-gradient(160deg, #fff2e2, #ffe3cc);
    display: grid; place-items: center; position: relative;
  }
  .photo img { width: 100%; height: 100%; object-fit: cover; display: block; }

  /* photo switcher (screen only) */
  .nav {
    position: absolute; inset: 0; display: flex; justify-content: space-between;
    align-items: center; padding: 0 6px; pointer-events: none;
  }
  .nav button {
    pointer-events: auto; width: 34px; height: 34px; border-radius: 50%;
    border: 0; cursor: pointer; font-size: 18px; font-weight: 900; line-height: 1;
    background: rgba(255,255,255,.85); color: var(--ink);
    box-shadow: 0 2px 8px rgba(0,0,0,.25);
  }
  .nav button:hover { background: #fff; }
  .dots {
    position: absolute; bottom: 8px; left: 0; right: 0;
    display: flex; justify-content: center; gap: 6px; pointer-events: none;
  }
  .dots i {
    width: 7px; height: 7px; border-radius: 50%;
    background: rgba(255,255,255,.6); box-shadow: 0 0 0 1px rgba(0,0,0,.2);
  }
  .dots i.on { background: #fff; }

  .name {
    text-align: center; font-weight: 800;
    font-size: .46in; line-height: 1; letter-spacing: .01em;
  }
  .name .lead { color: var(--accent-deep); }

  .tools {
    display: flex; justify-content: center; padding-bottom: 6px;
  }
  .dl {
    font: inherit; font-weight: 700; font-size: 13px;
    border: 1.5px solid var(--line); background: #fff; color: var(--muted);
    border-radius: 999px; padding: 5px 12px; cursor: pointer;
  }
  .dl:hover { color: var(--accent-deep); border-color: var(--accent); }

  /* ---------- print: photo-size cut cards only ---------- */
  @media print {
    .bar, .hint, .nav, .dots, .tools { display: none !important; }
    body { background: #fff; }
    .sheet { gap: 0.18in; padding: 0.3in; }
    .card {
      box-shadow: none;
      break-inside: avoid;
      -webkit-print-color-adjust: exact; print-color-adjust: exact;
    }
    .badge { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  }
</style>
</head>
<body>
<script id="payload" type="application/json">/*__DATA__*/ null</script>

<div class="bar">
  <h1>Sound <span class="snd" id="barSnd"></span> cards</h1>
  <span class="spacer"></span>
  <button class="btn ghost" onclick="window.print()">🖨️ Print cut sheet</button>
</div>
<p class="hint" id="hint"></p>

<div class="sheet" id="sheet"></div>

<script>
  const DATA = JSON.parse(document.getElementById('payload').textContent);
  const state = [];   // current photo index per card

  document.getElementById('barSnd').textContent = '/' + DATA.sound + '/';
  document.getElementById('hint').textContent =
    (DATA.note ? DATA.note + '  ' : '') +
    'Use the ‹ › arrows to change a photo, "Download card" to save one, or "Print cut sheet" and cut along the dashed lines.';

  const sheet = document.getElementById('sheet');

  DATA.items.forEach((item, i) => {
    state[i] = 0;
    const card = document.createElement('div');
    card.className = 'card';
    const lead = item.name.charAt(0), rest = item.name.slice(1);
    card.innerHTML = `
      <div class="badge">/${DATA.sound}/</div>
      <div class="photo">
        <img id="img-${i}" alt="${item.name}">
        ${item.images.length > 1 ? `
        <div class="nav">
          <button aria-label="Previous photo" onclick="flip(${i},-1)">‹</button>
          <button aria-label="Next photo" onclick="flip(${i},1)">›</button>
        </div>
        <div class="dots" id="dots-${i}"></div>` : ''}
      </div>
      <div class="name"><span class="lead">${lead}</span>${rest}</div>
      <div class="tools"><button class="dl" onclick="download(${i})">⬇ Download card</button></div>
    `;
    sheet.appendChild(card);
    render(i);
  });

  function render(i) {
    const item = DATA.items[i];
    document.getElementById('img-'+i).src = item.images[state[i]];
    const dots = document.getElementById('dots-'+i);
    if (dots) {
      dots.innerHTML = item.images.map((_, k) =>
        `<i class="${k === state[i] ? 'on' : ''}"></i>`).join('');
    }
  }
  function flip(i, dir) {
    const n = DATA.items[i].images.length;
    state[i] = (state[i] + dir + n) % n;
    render(i);
  }

  // ---- draw one card to a canvas and download as PNG ----
  function download(i) {
    const item = DATA.items[i];
    const S = 2;                       // supersample for crisp text
    const W = 700 * S, PAD = 46 * S;
    const photo = W - PAD * 2;         // square photo
    const nameH = 150 * S;
    const H = PAD + photo + nameH;
    const cv = document.createElement('canvas');
    cv.width = W; cv.height = H;
    const g = cv.getContext('2d');

    // card background
    round(g, 0, 0, W, H, 34 * S); g.fillStyle = '#ffffff'; g.fill();

    const img = new Image();
    img.onload = () => {
      // cover-fit into square
      g.save();
      round(g, PAD, PAD, photo, photo, 24 * S); g.clip();
      const s = Math.max(photo / img.width, photo / img.height);
      const dw = img.width * s, dh = img.height * s;
      g.drawImage(img, PAD + (photo - dw) / 2, PAD + (photo - dh) / 2, dw, dh);
      g.restore();

      // sound badge
      g.save();
      g.translate(PAD + 30 * S, PAD + 30 * S); g.rotate(-0.07);
      g.font = `800 ${26 * S}px "Trebuchet MS", sans-serif`;
      const label = '/' + DATA.sound + '/';
      const tw = g.measureText(label).width;
      round(g, -10 * S, -22 * S, tw + 20 * S, 40 * S, 9 * S);
      g.fillStyle = '#3a2e26'; g.fill();
      g.fillStyle = '#fffaf2'; g.textBaseline = 'middle'; g.fillText(label, 0, 0);
      g.restore();

      // name (highlight first letter)
      const y = PAD + photo + nameH / 2;
      g.textBaseline = 'middle'; g.textAlign = 'left';
      g.font = `800 ${64 * S}px "Trebuchet MS", sans-serif`;
      const lead = item.name.charAt(0), rest = item.name.slice(1);
      const total = g.measureText(item.name).width;
      let x = (W - total) / 2;
      g.fillStyle = '#c74d18'; g.fillText(lead, x, y);
      x += g.measureText(lead).width;
      g.fillStyle = '#3a2e26'; g.fillText(rest, x, y);

      const a = document.createElement('a');
      a.download = `${DATA.sound}-${item.name.toLowerCase()}.png`;
      a.href = cv.toDataURL('image/png');
      a.click();
    };
    img.src = item.images[state[i]];
  }

  function round(g, x, y, w, h, r) {
    g.beginPath();
    g.moveTo(x + r, y);
    g.arcTo(x + w, y, x + w, y + h, r);
    g.arcTo(x + w, y + h, x, y + h, r);
    g.arcTo(x, y + h, x, y, r);
    g.arcTo(x, y, x + w, y, r);
    g.closePath();
  }
</script>
</body>
</html>
"""

if __name__ == "__main__":
    main()
