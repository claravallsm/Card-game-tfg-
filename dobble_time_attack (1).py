import numpy as np
from PIL import Image
import os, random, base64, json, io

def generate_bibd_37_9_2():
    v = 37
    base_block = [1, 7, 9, 10, 12, 16, 26, 33, 34]
    matrix = np.zeros((v, v), dtype=int)
    for i in range(v):
        for punt in base_block:
            punt_mogut = (punt + i) % v
            matrix[i][punt_mogut] = 1
    return matrix

matrix = generate_bibd_37_9_2()

directori_script = os.path.dirname(os.path.abspath(__file__))
noms_fitxers = []

carpetes = ["animals", "aliments", "fenomens atmosferics"]
for carpeta in carpetes:
    ruta = os.path.join(directori_script, carpeta)
    arxius = sorted([f for f in os.listdir(ruta) if f.endswith(".jpg")])
    seleccio = random.sample(arxius, min(3, len(arxius)))
    noms_fitxers += [os.path.join(ruta, f) for f in seleccio]

ruta_arreu = directori_script
arxius_arreu = sorted([f for f in os.listdir(ruta_arreu) if f.startswith("arreu") and f.endswith(".jpg")])
seleccio_arreu = random.sample(arxius_arreu, 37 - 3 * len(carpetes))
noms_fitxers += [os.path.join(ruta_arreu, f) for f in seleccio_arreu]

def foto_a_base64(path, mida=(200, 200)):
    img = Image.open(path).convert("RGB").resize(mida, Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    data = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{data}"

print(f"Convertint {len(noms_fitxers)} fotos...")
fotos_b64 = []
for i, path in enumerate(noms_fitxers):
    fotos_b64.append(foto_a_base64(path))
    print(f"  {i+1}/37: {os.path.basename(path)}")

matrix_json = json.dumps(matrix.tolist())
fotos_json  = json.dumps(fotos_b64)

html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dobble · Contrarellotge · BIBD(37,9,2)</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0e0e0f; --surface: #1a1a1c; --surface2: #242426;
    --accent: #1D9E75; --text: #f0efe8; --muted: #6b6b70;
    --border: rgba(255,255,255,0.08); --warn: #EF9F27;
    --error: #E24B4A; --radius: 16px;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif;
    min-height: 100vh; display: flex; flex-direction: column; align-items: center; }}
  header {{ width: 100%; max-width: 900px; padding: 2rem 1.5rem 1rem;
    display: flex; align-items: baseline; gap: 1rem; flex-wrap: wrap; }}
  header h1 {{ font-family: 'Space Mono', monospace; font-size: 1.5rem;
    letter-spacing: -0.02em; color: var(--accent); }}
  header .sub {{ font-size: 0.78rem; color: var(--muted); font-family: 'Space Mono', monospace; }}
  .stats {{ display: flex; gap: 10px; padding: 0 1.5rem; width: 100%;
    max-width: 900px; margin-bottom: 1rem; flex-wrap: wrap; }}
  .stat {{ background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 8px 16px; font-size: 0.78rem;
    font-family: 'Space Mono', monospace; color: var(--muted); }}
  .stat b {{ color: var(--text); }}
  #timer-bar-wrap {{ width: calc(100% - 3rem); max-width: 900px;
    background: var(--surface); border-radius: 99px; height: 8px;
    margin-bottom: 1.25rem; overflow: hidden; }}
  #timer-bar {{ height: 100%; border-radius: 99px;
    background: var(--accent); transition: width 0.25s linear, background 0.4s; }}
  #game {{ width: 100%; max-width: 900px; padding: 0 1rem; position: relative; }}
  .cards-row {{ display: flex; gap: 2rem; justify-content: center;
    align-items: center; margin-bottom: 1.5rem; flex-wrap: wrap; }}
  .card-wrap {{ display: flex; flex-direction: column; align-items: center; gap: 10px; }}
  .card-label {{ font-size: 0.7rem; font-family: 'Space Mono', monospace;
    color: var(--muted); letter-spacing: 0.1em; text-transform: uppercase; }}
  .card {{ border-radius: 50%; border: 1.5px solid var(--border); cursor: pointer;
    transition: border-color 0.2s, transform 0.15s; background: var(--surface); display: block; }}
  .card:hover {{ transform: scale(1.02); border-color: rgba(255,255,255,0.2); }}
  .card.active {{ border-color: var(--accent); border-width: 2.5px; }}
  .result-box {{ background: var(--surface); border: 1px solid var(--border);
    border-radius: var(--radius); padding: 1.25rem 1.5rem; text-align: center;
    margin-bottom: 1rem; min-height: 80px; display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 6px; transition: border-color 0.3s; }}
  .result-box.ok1 {{ border-color: var(--warn); }}
  .result-box.ok2 {{ border-color: var(--accent); }}
  .result-box.err {{ border-color: var(--error); }}
  .result-main {{ font-size: 1rem; font-weight: 500; }}
  .result-sub {{ font-size: 0.8rem; color: var(--muted); font-family: 'Space Mono', monospace; }}
  .hint-strip {{ background: var(--surface2); border: 1px solid var(--border);
    border-radius: 8px; padding: 6px 14px; font-size: 0.75rem;
    font-family: 'Space Mono', monospace; color: var(--muted);
    text-align: center; margin-bottom: 1rem; }}
  .btns {{ display: flex; gap: 10px; justify-content: center;
    margin-bottom: 2rem; flex-wrap: wrap; }}
  button {{ background: transparent; border: 1px solid var(--border); color: var(--text);
    padding: 10px 22px; border-radius: 8px; font-family: 'Space Mono', monospace;
    font-size: 0.78rem; cursor: pointer; transition: background 0.15s, border-color 0.15s; }}
  button:hover {{ background: var(--surface2); border-color: rgba(255,255,255,0.2); }}
  button.primary {{ background: var(--accent); color: #0e0e0f;
    border-color: var(--accent); font-weight: 700; }}
  button.primary:hover {{ opacity: 0.88; }}
  button:disabled {{ opacity: 0.3; cursor: default; pointer-events: none; }}
  #overlay {{ position: absolute; inset: 0;
    background: rgba(14,14,15,0.92); border-radius: var(--radius);
    display: none; flex-direction: column; align-items: center;
    justify-content: center; gap: 14px; z-index: 10; padding: 2rem; }}
  #overlay .big {{ font-size: 2.2rem; font-weight: 700; color: var(--accent); }}
  #overlay .sub {{ font-size: 0.9rem; color: var(--muted);
    font-family: 'Space Mono', monospace; text-align: center; line-height: 1.8; }}
</style>
</head>
<body>

<header>
  <h1>Dobble · Contrarellotge</h1>
  <span class="sub">BIBD(37,9,2) · 2 minuts</span>
</header>

<div class="stats">
  <div class="stat">punts: <b id="s-score">0</b></div>
  <div class="stat">rondes: <b id="s-rounds">0</b></div>
  <div class="stat">temps: <b id="s-time">2:00</b></div>
</div>

<div id="timer-bar-wrap">
  <div id="timer-bar" style="width:100%"></div>
</div>

<div id="game">
  <div class="cards-row">
    <div class="card-wrap">
      <div class="card-label">carta 1</div>
      <canvas id="c1" class="card" width="280" height="280"></canvas>
    </div>
    <div class="card-wrap">
      <div class="card-label">carta 2</div>
      <canvas id="c2" class="card" width="280" height="280"></canvas>
    </div>
  </div>

  <div class="hint-strip">
    troba 1 símbol comú → +1 pt i passa &nbsp;·&nbsp; troba els 2 → +2 pts i passa
  </div>

  <div class="result-box" id="result">
    <div class="result-sub">prem Inicia per començar el compte enrere</div>
  </div>

  <div class="btns">
    <button class="primary" id="btn-start" onclick="iniciar()">Inicia ▶</button>
    <button id="btn-passa" onclick="passaAmbUn()" style="display:none" disabled>passa (+1 pt) →</button>
    <button id="btn-skip"  onclick="saltaRonda()" style="display:none">salta (0 pts) →</button>
  </div>

  <div id="overlay">
    <div class="big">⏱ Temps acabat!</div>
    <div class="sub" id="overlay-sub"></div>
    <button class="primary" onclick="reiniciar()">Torna a jugar</button>
  </div>
</div>

<script>
const MATRIX = {matrix_json};
const FOTOS  = {fotos_json};
const TOTAL_SECS = 120;

let i1=0, i2=1, selEsq=null, primerTrobat=null;
let score=0, rounds=0;
let secsLeft=TOTAL_SECS, timerInterval=null, running=false;

const imgs = FOTOS.map(src => {{
  const im = new Image(); im.src = src; return im;
}});

function blocs(idx) {{
  return MATRIX[idx].map((v,i) => v===1 ? i : -1).filter(x => x>=0);
}}
function comuns(a, b) {{
  const s = new Set(blocs(a));
  return blocs(b).filter(x => s.has(x));
}}
function placeSimbols(R) {{
  const anell = R*0.58, pos = [[R,R]];
  for (let i=0; i<8; i++) {{
    const a = (i/8)*Math.PI*2 - Math.PI/2;
    pos.push([R + Math.cos(a)*anell, R + Math.sin(a)*anell]);
  }}
  return pos;
}}
function drawCard(canvas, idx, highlight=[], dim=[]) {{
  const ctx = canvas.getContext('2d'), W = canvas.width, R = W/2;
  const syms = blocs(idx), pos = placeSimbols(R);
  canvas.dataset.syms = JSON.stringify(syms);
  canvas.dataset.pos  = JSON.stringify(pos);
  function render() {{
    ctx.clearRect(0,0,W,W);
    ctx.beginPath(); ctx.arc(R,R,R-2,0,Math.PI*2);
    ctx.fillStyle='#1a1a1c'; ctx.fill();
    syms.forEach((s,i) => {{
      const [x,y]=pos[i], r=Math.floor(R/4.8);
      const hl=highlight.includes(s), dm=dim.includes(s);
      ctx.globalAlpha = dm ? 0.12 : 1;
      if (hl) {{
        ctx.beginPath(); ctx.arc(x,y,r+5,0,Math.PI*2);
        ctx.fillStyle='rgba(29,158,117,0.18)'; ctx.fill();
        ctx.strokeStyle='#1D9E75'; ctx.lineWidth=2; ctx.stroke();
      }}
      const im = imgs[s];
      ctx.save(); ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.clip();
      if (im.complete && im.naturalWidth>0) ctx.drawImage(im,x-r,y-r,r*2,r*2);
      else {{ ctx.fillStyle='#333'; ctx.fill(); }}
      ctx.restore();
      if (hl) {{
        ctx.strokeStyle='#1D9E75'; ctx.lineWidth=2;
        ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.stroke();
      }}
    }});
    ctx.globalAlpha=1;
    ctx.beginPath(); ctx.arc(R,R,R-2,0,Math.PI*2);
    ctx.strokeStyle='rgba(255,255,255,0.06)'; ctx.lineWidth=1.5; ctx.stroke();
  }}
  const pend = syms.map(s=>imgs[s]).filter(im=>!im.complete||im.naturalWidth===0);
  if (!pend.length) {{ render(); return; }}
  let n=0; pend.forEach(im=>{{ im.onload=im.onerror=()=>{{n++;if(n===pend.length)render();}};  }});
}}
function setResult(cls, main, sub) {{
  const b=document.getElementById('result');
  b.className='result-box'+(cls?' '+cls:'');
  b.innerHTML=`<div class="result-main">${{main}}</div><div class="result-sub">${{sub}}</div>`;
}}
function updateTimer() {{
  secsLeft--;
  if (secsLeft<=0) {{
    secsLeft=0; clearInterval(timerInterval); timerInterval=null; running=false;
    gameOver();
  }}
  const m=Math.floor(secsLeft/60), s=secsLeft%60;
  document.getElementById('s-time').textContent = m+':'+(s<10?'0':'')+s;
  const pct=(secsLeft/TOTAL_SECS)*100;
  const bar=document.getElementById('timer-bar');
  bar.style.width=pct+'%';
  bar.style.background=pct>50?'#1D9E75':pct>20?'#EF9F27':'#E24B4A';
}}
function gameOver() {{
  document.getElementById('overlay-sub').innerHTML =
    `Has aconseguit <b style="color:#f0efe8">${{score}} punts</b> en ${{rounds}} rondes`;
  document.getElementById('overlay').style.display='flex';
  document.getElementById('btn-passa').style.display='none';
  document.getElementById('btn-skip').style.display='none';
}}
function novaRonda() {{
  if (!running) return;
  selEsq=null; primerTrobat=null;
  i1=Math.floor(Math.random()*37);
  do {{ i2=Math.floor(Math.random()*37); }} while (i2===i1);
  document.getElementById('c1').classList.remove('active');
  document.getElementById('c2').classList.remove('active');
  document.getElementById('btn-passa').style.display='none';
  document.getElementById('btn-passa').disabled=true;
  document.getElementById('btn-skip').style.display='inline-block';
  drawCard(document.getElementById('c1'), i1);
  drawCard(document.getElementById('c2'), i2);
  setResult('', 'Troba els símbols comuns',
    'clica un símbol de la carta esquerra i el mateix a la dreta');
}}

// Passa amb 1 punt ja assegurat
function passaAmbUn() {{
  if (!running) return;
  rounds++; document.getElementById('s-rounds').textContent=rounds;
  setResult('ok1', '+1 pt · has passat', 'bona decisió si el temps escasseja!');
  document.getElementById('btn-passa').style.display='none';
  document.getElementById('btn-skip').style.display='none';
  setTimeout(novaRonda, 1200);
}}

// Salta sense punt
function saltaRonda() {{
  if (!running) return;
  rounds++; document.getElementById('s-rounds').textContent=rounds;
  const c=comuns(i1,i2);
  drawCard(document.getElementById('c1'), i1, c, []);
  drawCard(document.getElementById('c2'), i2, c, []);
  setResult('err', '0 pts · has saltat', `Eren: #${{c.join(' i #')}}`);
  document.getElementById('btn-passa').style.display='none';
  document.getElementById('btn-skip').style.display='none';
  setTimeout(novaRonda, 1500);
}}

function handleClick(canvas, cardIdx, evt) {{
  if (!running) return;
  const rect=canvas.getBoundingClientRect();
  const mx=(evt.clientX-rect.left)*(canvas.width/rect.width);
  const my=(evt.clientY-rect.top)*(canvas.height/rect.height);
  const syms=JSON.parse(canvas.dataset.syms||'[]');
  const pos=JSON.parse(canvas.dataset.pos||'[]');
  let clicked=null;
  syms.forEach((s,i)=>{{ if(Math.hypot(mx-pos[i][0],my-pos[i][1])<34) clicked=s; }});
  if (clicked===null) return;

  const c=comuns(i1,i2);
  const c1el=document.getElementById('c1'), c2el=document.getElementById('c2');

  if (primerTrobat===null) {{
    // ── Fase 1: busca el primer símbol ──
    if (cardIdx===i1) {{
      selEsq=clicked;
      c1el.classList.add('active');
      setResult('', `Símbol seleccionat: #${{clicked}}`,
        'ara fes clic al MATEIX símbol a la carta dreta');
    }} else if (cardIdx===i2 && selEsq!==null) {{
      c1el.classList.remove('active');
      if (c.includes(clicked) && clicked===selEsq) {{
        // Primer encert → +1 pt, activa "passa" i continua buscant el segon
        primerTrobat=clicked;
        score++; document.getElementById('s-score').textContent=score;
        drawCard(c1el, i1, [primerTrobat], []);
        drawCard(c2el, i2, [primerTrobat], []);
        setResult('ok1', `✓ +1 pt! Símbol #${{clicked}} trobat`,
          'busca el 2n símbol per +1 pt més · o prem "passa (+1 pt)" per continuar');
        document.getElementById('btn-passa').style.display='inline-block';
        document.getElementById('btn-passa').disabled=false;
        document.getElementById('btn-skip').style.display='none';
        selEsq=null;
      }} else {{
        setResult('err', '✗ Incorrecte',
          `#${{clicked}} i #${{selEsq}} no coincideixen · torna-ho a intentar`);
        selEsq=null;
      }}
    }}

  }} else {{
    // ── Fase 2: busca el segon símbol ──
    if (cardIdx===i1) {{
      if (clicked===primerTrobat) {{
        setResult('ok1', 'Ja has trobat aquest!', 'busca el SEGON símbol comú diferent');
        return;
      }}
      selEsq=clicked;
      c1el.classList.add('active');
      setResult('ok1', `Símbol seleccionat: #${{clicked}}`,
        'ara fes clic al MATEIX símbol a la carta dreta');
    }} else if (cardIdx===i2 && selEsq!==null) {{
      c1el.classList.remove('active');
      const segon=c.find(x=>x!==primerTrobat);
      if (c.includes(clicked) && clicked===selEsq && clicked!==primerTrobat) {{
        // Segon encert → +1 pt addicional, tanca la ronda
        score++; rounds++;
        document.getElementById('s-score').textContent=score;
        document.getElementById('s-rounds').textContent=rounds;
        drawCard(c1el, i1, c, []);
        drawCard(c2el, i2, c, []);
        setResult('ok2', `✓✓ +2 pts en total! Els 2 símbols trobats!`,
          `Comuns: #${{c.join(' i #')}}`);
        document.getElementById('btn-passa').style.display='none';
        selEsq=null; primerTrobat=null;
        setTimeout(novaRonda, 1800);
      }} else {{
        setResult('ok1', `✗ No és aquest · segueix buscant`,
          `tens 1 pt assegurat · prem "passa (+1 pt)" si vols continuar`);
        selEsq=null;
      }}
    }}
  }}
}}

function iniciar() {{
  score=0; rounds=0; secsLeft=TOTAL_SECS; running=true;
  selEsq=null; primerTrobat=null;
  document.getElementById('s-score').textContent='0';
  document.getElementById('s-rounds').textContent='0';
  document.getElementById('s-time').textContent='2:00';
  document.getElementById('timer-bar').style.width='100%';
  document.getElementById('timer-bar').style.background='#1D9E75';
  document.getElementById('overlay').style.display='none';
  document.getElementById('btn-start').style.display='none';
  if (timerInterval) clearInterval(timerInterval);
  timerInterval=setInterval(updateTimer, 1000);
  novaRonda();
}}
function reiniciar() {{ iniciar(); }}

document.getElementById('c1').addEventListener('click', e=>handleClick(document.getElementById('c1'),i1,e));
document.getElementById('c2').addEventListener('click', e=>handleClick(document.getElementById('c2'),i2,e));

let n=0;
imgs.forEach(im=>{{
  const done=()=>{{ n++; if(n===imgs.length){{
    drawCard(document.getElementById('c1'),0);
    drawCard(document.getElementById('c2'),1);
  }} }};
  if(im.complete&&im.naturalWidth>0) done();
  else {{ im.onload=done; im.onerror=done; }}
}});
</script>
</body>
</html>"""

output_path = os.path.join(directori_script, "dobble_time_attack.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

size_mb = os.path.getsize(output_path) / 1024 / 1024
print(f"\nFet! dobble_time_attack.html generat ({size_mb:.1f} MB)")
print(f"Ubicació: {output_path}")
