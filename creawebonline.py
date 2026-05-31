import numpy as np
from PIL import Image
import os, random, base64, json, io

# ── el teu codi original ────────────────────────────────────────────────────

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

# les fotos estan a la mateixa carpeta que aquest script
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

# ── convertir fotos a base64 ────────────────────────────────────────────────

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

# ── generar HTML ────────────────────────────────────────────────────────────

matrix_json = json.dumps(matrix.tolist())
fotos_json  = json.dumps(fotos_b64)

html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Dobble · BIBD(37,9,2)</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap" rel="stylesheet">
<style>
  :root {{
    --bg: #0e0e0f; --surface: #1a1a1c; --surface2: #242426;
    --accent: #c8f135; --text: #f0efe8; --muted: #6b6b70;
    --border: rgba(255,255,255,0.08); --success: #c8f135; --error: #ff6b6b;
    --radius: 16px;
  }}
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ background: var(--bg); color: var(--text); font-family: 'DM Sans', sans-serif;
    min-height: 100vh; display: flex; flex-direction: column; align-items: center; }}
  header {{ width: 100%; max-width: 900px; padding: 2rem 1.5rem 1rem;
    display: flex; align-items: baseline; gap: 1rem; }}
  header h1 {{ font-family: 'Space Mono', monospace; font-size: 1.6rem;
    letter-spacing: -0.02em; color: var(--accent); }}
  header .sub {{ font-size: 0.8rem; color: var(--muted); font-family: 'Space Mono', monospace; }}
  .stats {{ display: flex; gap: 10px; padding: 0 1.5rem; width: 100%;
    max-width: 900px; margin-bottom: 1.5rem; flex-wrap: wrap; }}
  .stat {{ background: var(--surface); border: 1px solid var(--border);
    border-radius: 8px; padding: 8px 16px; font-size: 0.78rem;
    font-family: 'Space Mono', monospace; color: var(--muted); }}
  .stat b {{ color: var(--text); }}
  #game {{ width: 100%; max-width: 900px; padding: 0 1rem; }}
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
    margin-bottom: 1.5rem; min-height: 80px; display: flex; flex-direction: column;
    align-items: center; justify-content: center; gap: 6px; transition: border-color 0.3s; }}
  .result-box.ok {{ border-color: var(--success); }}
  .result-box.err {{ border-color: var(--error); }}
  .result-main {{ font-size: 1rem; font-weight: 500; }}
  .result-sub {{ font-size: 0.8rem; color: var(--muted); font-family: 'Space Mono', monospace; }}
  .btns {{ display: flex; gap: 10px; justify-content: center;
    margin-bottom: 2rem; flex-wrap: wrap; }}
  button {{ background: transparent; border: 1px solid var(--border); color: var(--text);
    padding: 10px 22px; border-radius: 8px; font-family: 'Space Mono', monospace;
    font-size: 0.78rem; cursor: pointer; transition: background 0.15s, border-color 0.15s; }}
  button:hover {{ background: var(--surface2); border-color: rgba(255,255,255,0.2); }}
  button.primary {{ background: var(--accent); color: #0e0e0f;
    border-color: var(--accent); font-weight: 700; }}
  button.primary:hover {{ opacity: 0.88; }}
</style>
</head>
<body>

<header>
  <h1>dobble.</h1>
  <span class="sub">BIBD(37,9,2) — λ=2</span>
</header>

<div class="stats">
  <div class="stat">punts: <b id="s-score">0</b></div>
  <div class="stat">rondes: <b id="s-rounds">0</b></div>
  <div class="stat">cartes: <b>37</b></div>
  <div class="stat">símbols/carta: <b>9</b></div>
  <div class="stat">comuns: <b>2</b></div>
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
  <div class="result-box" id="result">
    <div class="result-main">Troba els 2 símbols comuns</div>
    <div class="result-sub">fes clic sobre un símbol de la carta esquerra</div>
  </div>
  <div class="btns">
    <button class="primary" onclick="novaRonda()">nova ronda →</button>
    <button onclick="mostraPista()">pista</button>
  </div>
</div>

<script>
const MATRIX = {matrix_json};
const FOTOS  = {fotos_json};

let i1=0, i2=1, seleccionat=null, pista=false, score=0, rounds=0;
const imgs = FOTOS.map(src => {{ const im=new Image(); im.src=src; return im; }});

function blocs(idx) {{
  return MATRIX[idx].map((v,i) => v===1?i:-1).filter(x=>x>=0);
}}
function comuns() {{
  const s1=new Set(blocs(i1));
  return blocs(i2).filter(s=>s1.has(s));
}}
function placeSimbols(n,R) {{
  const cols=3, r=R/3.8;
  const step = (R*2 - r*2) / (cols-1);
  const offset = r + 4;
  const pos=[];
  for(let i=0;i<9;i++) {{
    const row=Math.floor(i/3), col=i%3;
    const angle = (i/9)*Math.PI*2 + Math.random()*0.4 - 0.2;
    const jx = (Math.random()-0.5)*8;
    const jy = (Math.random()-0.5)*8;
    const x = offset + col*step + jx;
    const y = offset + row*step + jy;
    pos.push([x,y]);
  }}
  return pos;
}}
function drawCard(canvas,idx,highlight=[],dimRest=false) {{
  const ctx=canvas.getContext('2d'),W=canvas.width,R=W/2;
  ctx.clearRect(0,0,W,W);
  ctx.beginPath();ctx.arc(R,R,R-2,0,Math.PI*2);
  ctx.fillStyle='#1a1a1c';ctx.fill();
  const syms=blocs(idx),pos=placeSimbols(syms.length,R);
  canvas.dataset.syms=JSON.stringify(syms);
  canvas.dataset.pos=JSON.stringify(pos);
  syms.forEach((symIdx,i) => {{
    const [x,y]=pos[i],r=Math.floor(R/3.8);
    const isHL=highlight.includes(symIdx);
    ctx.globalAlpha=(dimRest&&!isHL)?0.15:1;
    if(isHL) {{
      ctx.beginPath();ctx.arc(x,y,r+4,0,Math.PI*2);
      ctx.fillStyle='rgba(200,241,53,0.15)';ctx.fill();
      ctx.strokeStyle='#c8f135';ctx.lineWidth=2;ctx.stroke();
    }}
    const im=imgs[symIdx];
    const draw=()=>{{
      ctx.save();ctx.beginPath();ctx.arc(x,y,r,0,Math.PI*2);ctx.clip();
      ctx.drawImage(im,x-r,y-r,r*2,r*2);ctx.restore();
    }};
    if(im.complete) draw();
    else im.onload=()=>{{ctx.globalAlpha=(dimRest&&!isHL)?0.15:1;draw();ctx.globalAlpha=1;}};
  }});
  ctx.globalAlpha=1;
  ctx.beginPath();ctx.arc(R,R,R-2,0,Math.PI*2);
  ctx.strokeStyle='rgba(255,255,255,0.06)';ctx.lineWidth=1.5;ctx.stroke();
}}
function setResult(cls,main,sub) {{
  const box=document.getElementById('result');
  box.className='result-box'+(cls?' '+cls:'');
  box.innerHTML=`<div class="result-main">${{main}}</div><div class="result-sub">${{sub}}</div>`;
}}
function novaRonda() {{
  seleccionat=null;pista=false;
  i1=Math.floor(Math.random()*37);
  do{{i2=Math.floor(Math.random()*37);}}while(i2===i1);
  document.getElementById('c1').classList.remove('active');
  document.getElementById('c2').classList.remove('active');
  drawCard(document.getElementById('c1'),i1);
  drawCard(document.getElementById('c2'),i2);
  setResult('','Troba els 2 símbols comuns','fes clic sobre un símbol de la carta esquerra');
}}
function mostraPista() {{
  pista=true;
  const c=comuns();
  drawCard(document.getElementById('c1'),i1,c,true);
  drawCard(document.getElementById('c2'),i2,c,true);
  setResult('','símbols comuns ressaltats',`índexs: ${{c.join(' i ')}}`);
}}
function handleClick(canvas,cardIdx,evt) {{
  if(pista) return;
  const rect=canvas.getBoundingClientRect();
  const mx=(evt.clientX-rect.left)*(canvas.width/rect.width);
  const my=(evt.clientY-rect.top)*(canvas.height/rect.height);
  const syms=JSON.parse(canvas.dataset.syms||'[]');
  const pos=JSON.parse(canvas.dataset.pos||'[]');
  let clicked=null;
  syms.forEach((s,i)=>{{if(Math.hypot(mx-pos[i][0],my-pos[i][1])<32) clicked=s;}});
  if(clicked===null) return;
  if(cardIdx===i1) {{
    seleccionat=clicked;
    canvas.classList.add('active');
    setResult('',`símbol seleccionat: #${{clicked}}`,'ara fes clic al mateix símbol a la carta dreta');
  }} else if(cardIdx===i2&&seleccionat!==null) {{
    const c=comuns();
    const ok=c.includes(clicked)&&c.includes(seleccionat)&&clicked===seleccionat;
    const ok2=c.includes(clicked)&&c.includes(seleccionat);
    if(ok||ok2){{score++;document.getElementById('s-score').textContent=score;}}
    rounds++;document.getElementById('s-rounds').textContent=rounds;
    drawCard(document.getElementById('c1'),i1,c);
    drawCard(document.getElementById('c2'),i2,c);
    if(ok||ok2) setResult('ok','✓ correcte! +1 punt',`comuns: #${{c.join(' i #')}}`);
    else setResult('err','✗ incorrecte',`eren: #${{c.join(' i #')}}`);
    seleccionat=null;
    setTimeout(novaRonda,2000);
  }}
}}
document.getElementById('c1').addEventListener('click',e=>handleClick(document.getElementById('c1'),i1,e));
document.getElementById('c2').addEventListener('click',e=>handleClick(document.getElementById('c2'),i2,e));
novaRonda();
</script>
</body>
</html>"""

output_path = os.path.join(directori_script, "dobble.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(html)

size_mb = os.path.getsize(output_path) / 1024 / 1024
print(f"\nFet! dobble.html generat ({size_mb:.1f} MB)")
print(f"Ubicació: {output_path}")
print("\nAra puja dobble.html al GitHub i activa Pages.")
