import numpy as np
from PIL import Image
import os, random, base64, json, io

def rho(p):
    g, i = p
    return (g, (i + 1) % 7)

def sigma(p):
    g, i = p
    if g == 1: return (2, (2*i) % 7)
    if g == 2: return (3, (2*i) % 7)
    if g == 3: return (1, (2*i) % 7)
    if g == 4: return (5, (2*i) % 7)
    if g == 5: return (6, (2*i) % 7)
    if g == 6: return (4, (2*i) % 7)
    if g == 7: return (7, (2*i) % 7)
    if g == 8: return (8, (2*i) % 7)

def tau(p):
    g, i = p
    if g == 1: return (4, (6*i) % 7)
    if g == 2: return (5, (6*i) % 7)
    if g == 3: return (6, (6*i) % 7)
    if g == 4: return (1, (6*i) % 7)
    if g == 5: return (2, (6*i) % 7)
    if g == 6: return (3, (6*i) % 7)
    if g == 7: return (8, (6*i) % 7)
    if g == 8: return (7, (6*i) % 7)

def get_orbit(base_block):
    orbit = [frozenset(base_block)]
    for block in orbit:
        for move in [rho, sigma, tau]:
            new_block = frozenset(move(p) for p in block)
            if new_block not in orbit:
                orbit.append(new_block)
    return orbit

def generate_bibd_56_11_2():
    points = [(g, i) for g in range(1, 9) for i in range(7)]
    point_to_idx = {p: idx for idx, p in enumerate(points)}
    b1 = [(1,1),(2,2),(3,4),(4,1),(5,2),(6,4),(7,0),(7,3),(7,6),(7,5),(8,0)]
    b2 = [(1,2),(1,5),(2,2),(2,5),(3,1),(3,6),(4,0),(4,1),(4,6),(7,1),(8,6)]
    all_blocks = list(get_orbit(b1)) + list(get_orbit(b2))
    matrix = np.zeros((56, 56), dtype=int)
    for row_idx, block in enumerate(all_blocks):
        for p in block:
            matrix[row_idx][point_to_idx[p]] = 1
    return matrix

matrix = generate_bibd_56_11_2()
NUM_CARDS   = matrix.shape[0]
NUM_SYMBOLS = matrix.shape[1]

directori_script = os.path.dirname(os.path.abspath(__file__))
noms_fitxers = []

carpetes = ["animals", "aliments", "fenomens atmosferics"]
for carpeta in carpetes:
    ruta = os.path.join(directori_script, carpeta)
    arxius = sorted([f for f in os.listdir(ruta) if f.endswith(".jpg")])
    noms_fitxers += [os.path.join(ruta, f) for f in arxius]

ruta_arreu = directori_script
arxius_arreu = sorted([f for f in os.listdir(ruta_arreu) if f.startswith("arreu") and f.endswith(".jpg")])
seleccio_arreu = random.sample(arxius_arreu, NUM_SYMBOLS - len(noms_fitxers))
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
    print(f"  {i+1}/{NUM_SYMBOLS}: {os.path.basename(path)}")

matrix_json = json.dumps(matrix.tolist())
fotos_json  = json.dumps(fotos_b64)

page = '''<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
<title>Find the two (difficult version) </title>
<style>
:root {
  --bg:#0e0e0f; --sur:#1a1a1c; --sur2:#242426;
  --acc:#1D9E75; --txt:#f0efe8; --mut:#6b6b70;
  --bor:rgba(255,255,255,0.08); --warn:#EF9F27; --err:#E24B4A;
}
* { box-sizing:border-box; margin:0; padding:0; -webkit-tap-highlight-color:transparent; }
body { background:var(--bg); color:var(--txt); font-family:sans-serif;
  min-height:100vh; display:flex; flex-direction:column; align-items:center; }
header { width:100%; max-width:900px; padding:1.5rem 1.5rem 0.5rem; }
h1 { font-size:1.4rem; color:var(--acc); }
.sub { font-size:0.75rem; color:var(--mut); margin-top:4px; }
.stats { display:flex; gap:10px; padding:0.75rem 1.5rem; width:100%; max-width:900px; flex-wrap:wrap; }
.stat { background:var(--sur); border:1px solid var(--bor); border-radius:8px;
  padding:8px 16px; font-size:0.78rem; color:var(--mut); }
.stat b { color:var(--txt); }
#streak { display:none; background:var(--warn); color:#0e0e0f; border-radius:8px;
  padding:8px 16px; font-size:0.78rem; font-weight:700; }
#tbar-wrap { width:calc(100% - 3rem); max-width:900px; background:var(--sur);
  border-radius:99px; height:8px; margin:0.75rem 0; overflow:hidden; }
#tbar { height:100%; border-radius:99px; background:var(--acc);
  transition:width 0.25s linear, background 0.4s; }
#game { width:100%; max-width:900px; padding:0 1rem; position:relative; }
.row { display:flex; gap:1.5rem; justify-content:center; align-items:center;
  margin-bottom:1.25rem; flex-wrap:wrap; }
.cwrap { display:flex; flex-direction:column; align-items:center; gap:8px; }
.clabel { font-size:0.68rem; color:var(--mut); letter-spacing:0.1em; text-transform:uppercase; }
canvas { border-radius:50%; border:1.5px solid var(--bor);
  touch-action:none; display:block; background:var(--sur); }
.rbox { background:var(--sur); border:1px solid var(--bor); border-radius:14px;
  padding:1rem 1.25rem; text-align:center; margin-bottom:0.75rem;
  min-height:72px; display:flex; flex-direction:column;
  align-items:center; justify-content:center; gap:4px; transition:border-color 0.3s; }
.rbox.ok1 { border-color:var(--warn); }
.rbox.ok2 { border-color:var(--acc); }
.rbox.err { border-color:var(--err); }
.rmain { font-size:1rem; font-weight:600; }
.rsub  { font-size:0.75rem; color:var(--mut); }
.hint  { background:var(--sur2); border:1px solid var(--bor); border-radius:8px;
  padding:5px 12px; font-size:0.72rem; color:var(--mut); text-align:center; margin-bottom:0.75rem; }
.btns  { display:flex; gap:10px; justify-content:center; margin-bottom:1.5rem; flex-wrap:wrap; }
button { background:transparent; border:1px solid var(--bor); color:var(--txt);
  padding:14px 28px; border-radius:8px; font-size:1rem; font-weight:600;
  cursor:pointer; touch-action:manipulation; -webkit-appearance:none; user-select:none; }
button.acc { background:var(--acc); color:#0e0e0f; border-color:var(--acc); }
button.hid { display:none !important; }
#overlay { position:absolute; inset:0; background:rgba(14,14,15,0.93);
  border-radius:14px; display:none; flex-direction:column;
  align-items:center; justify-content:center; gap:12px; z-index:10; padding:2rem; }
#overlay .big { font-size:1.8rem; font-weight:700; color:var(--acc); }
#overlay .osub { font-size:0.9rem; color:var(--mut); text-align:center; line-height:1.8; }
#bonus { position:fixed; top:20px; left:50%; transform:translateX(-50%);
  background:var(--warn); color:#0e0e0f; padding:8px 20px; border-radius:99px;
  font-weight:700; font-size:1rem; opacity:0; transition:opacity 0.3s;
  pointer-events:none; z-index:100; }
</style>
</head>
<body>
<div id="bonus">+5 seg!</div>
<header>
  <h1>Dobble Gran &middot; Contrarellotge</h1>
  <div class="sub">BIBD(56,11,2) &middot; 2 minuts</div>
</header>
<div class="stats">
  <div class="stat">punts: <b id="sc">0</b></div>
  <div class="stat">rondes: <b id="sr">0</b></div>
  <div class="stat">temps: <b id="st">2:00</b></div>
  <div id="streak">&#128293; ratxa: <span id="stk">0</span></div>
</div>
<div id="tbar-wrap"><div id="tbar" style="width:100%"></div></div>
<div id="game">
  <div class="row">
    <div class="cwrap">
      <div class="clabel">carta 1</div>
      <canvas id="c1" width="280" height="280"></canvas>
    </div>
    <div class="cwrap">
      <div class="clabel">carta 2</div>
      <canvas id="c2" width="280" height="280"></canvas>
    </div>
  </div>
  <div class="hint">1 simbol comu &rarr; +1 pt &nbsp;&middot;&nbsp; tots 2 &rarr; +2 pts &nbsp;&middot;&nbsp; ratxa x3 &rarr; +5 seg!</div>
  <div class="rbox" id="res"><div class="rsub">Prem Inicia per començar</div></div>
  <div class="btns">
    <button class="acc" id="b-ini">Inicia</button>
    <button id="b-pas" class="acc hid">Passa (+1 pt)</button>
    <button id="b-sal" class="hid">Salta (0 pts)</button>
  </div>
  <div id="overlay">
    <div class="big">Temps acabat!</div>
    <div class="osub" id="ov-sub"></div>
    <button class="acc" id="b-rei">Torna a jugar</button>
  </div>
</div>
<script>
var MATRIX = __MATRIX__;
var FOTOS  = __FOTOS__;
var TSECS  = 120;
var NC     = __NC__;

var G = {
  i1:0, i2:1,
  estat:'idle',
  selEsq:null,
  prim:null,
  score:0, rounds:0,
  secs:120,
  timer:null,
  run:false,
  streak:0,
  best: parseInt(localStorage.getItem('best56') || '0')
};

var imgs = FOTOS.map(function(s) {
  var im = new Image(); im.src = s; return im;
});

function blocs(i) {
  return MATRIX[i].map(function(v,j) { return v ? j : -1; })
                  .filter(function(x) { return x >= 0; });
}
function comuns(a, b) {
  var s = new Set(blocs(a));
  return blocs(b).filter(function(x) { return s.has(x); });
}
function posicions(R) {
  var p = [[R,R]], an = R * 0.62;
  for (var i = 0; i < 10; i++) {
    var a = i / 10 * Math.PI * 2 - Math.PI / 2;
    p.push([R + Math.cos(a) * an, R + Math.sin(a) * an]);
  }
  return p;
}


function draw(cv, idx, hl, dm, sel) {
  hl  = hl  || [];
  dm  = dm  || [];
  sel = (sel !== undefined && sel !== null) ? sel : -1;
  var ctx = cv.getContext('2d'), W = cv.width, R = W / 2;
  var sy = blocs(idx), ps = posicions(R);
  cv.dataset.sy = JSON.stringify(sy);
  cv.dataset.ps = JSON.stringify(ps);
  var r0 = Math.floor(R / 5.5);
  function rnd() {
    ctx.clearRect(0,0,W,W);
    ctx.beginPath(); ctx.arc(R,R,R-2,0,Math.PI*2);
    ctx.fillStyle = '#1a1a1c'; ctx.fill();
    sy.forEach(function(s, i) {
      var x = ps[i][0], y = ps[i][1], r = r0;
      var h     = hl.indexOf(s) >= 0;
      var d     = dm.indexOf(s) >= 0;
      var isSel = (s === sel);
      ctx.globalAlpha = d ? 0.12 : 1;
      if (h) {
        ctx.beginPath(); ctx.arc(x,y,r+6,0,Math.PI*2);
        ctx.fillStyle = 'rgba(29,158,117,0.22)'; ctx.fill();
        ctx.strokeStyle = '#1D9E75'; ctx.lineWidth = 2.5; ctx.stroke();
      } else if (isSel) {
        ctx.beginPath(); ctx.arc(x,y,r+6,0,Math.PI*2);
        ctx.fillStyle = 'rgba(239,159,39,0.25)'; ctx.fill();
        ctx.strokeStyle = '#EF9F27'; ctx.lineWidth = 2.5; ctx.stroke();
      }
      var im = imgs[s];
      ctx.save();
      ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.clip();
      if (im.complete && im.naturalWidth) ctx.drawImage(im, x-r, y-r, r*2, r*2);
      else { ctx.fillStyle = '#333'; ctx.fill(); }
      ctx.restore();
      if (h) {
        ctx.strokeStyle = '#1D9E75'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.stroke();
      } else if (isSel) {
        ctx.strokeStyle = '#EF9F27'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.stroke();
      }
    });
    ctx.globalAlpha = 1;
    ctx.beginPath(); ctx.arc(R,R,R-2,0,Math.PI*2);
    ctx.strokeStyle = 'rgba(255,255,255,0.06)'; ctx.lineWidth = 1.5; ctx.stroke();
  }
  var pend = sy.map(function(s) { return imgs[s]; })
              .filter(function(im) { return !im.complete || !im.naturalWidth; });
  if (!pend.length) { rnd(); return; }
  var n = 0;
  pend.forEach(function(im) {
    im.onload = im.onerror = function() { if (++n === pend.length) rnd(); };
  });
}

function setRes(cls, main, sub) {
  var b = document.getElementById('res');
  b.className = 'rbox' + (cls ? ' ' + cls : '');
  b.innerHTML = '<div class="rmain">' + main + '</div><div class="rsub">' + sub + '</div>';
}
function hid(id, hide) {
  document.getElementById(id).classList.toggle('hid', hide);
}
function getXY(e, cv) {
  var r = cv.getBoundingClientRect();
  var sx = cv.width / r.width, sy = cv.height / r.height;
  if (e.touches && e.touches.length) {
    return [(e.touches[0].clientX - r.left) * sx,
            (e.touches[0].clientY - r.top)  * sy];
  }
  return [(e.clientX - r.left) * sx, (e.clientY - r.top) * sy];
}

var actx = null;
function so(freq, dur, type) {
  try {
    if (!actx) actx = new (window.AudioContext || window.webkitAudioContext)();
    var o = actx.createOscillator(), g = actx.createGain();
    o.connect(g); g.connect(actx.destination);
    o.type = type || 'sine'; o.frequency.value = freq;
    g.gain.setValueAtTime(0.18, actx.currentTime);
    g.gain.exponentialRampToValueAtTime(0.001, actx.currentTime + dur);
    o.start(); o.stop(actx.currentTime + dur);
  } catch(e) {}
}
function soEncert() { so(660,0.12); setTimeout(function(){so(880,0.12);},100); }
function soDoble()  { so(660,0.1); setTimeout(function(){so(880,0.1);},90); setTimeout(function(){so(1100,0.2);},180); }
function soError()  { so(220,0.18,'sawtooth'); }
function soBonus()  { so(880,0.08); setTimeout(function(){so(1100,0.08);},70); setTimeout(function(){so(1320,0.15);},140); }

function showBonus(txt) {
  var b = document.getElementById('bonus');
  b.textContent = txt; b.style.opacity = '1';
  setTimeout(function() { b.style.opacity = '0'; }, 1200);
}
function updateStreak() {
  var el = document.getElementById('streak');
  if (G.streak >= 2) {
    el.style.display = 'block';
    document.getElementById('stk').textContent = G.streak;
  } else {
    el.style.display = 'none';
  }
}
function tick() {
  G.secs--;
  if (G.secs <= 0) {
    G.secs = 0; clearInterval(G.timer); G.timer = null; G.run = false; fi();
  }
  var m = Math.floor(G.secs / 60), s = G.secs % 60;
  document.getElementById('st').textContent = m + ':' + (s < 10 ? '0' : '') + s;
  var p = G.secs / TSECS * 100;
  var b = document.getElementById('tbar');
  b.style.width = p + '%';
  b.style.background = p > 50 ? '#1D9E75' : p > 20 ? '#EF9F27' : '#E24B4A';
}
function fi() {
  if (G.score > G.best) {
    G.best = G.score;
    localStorage.setItem('best56', G.score);
  }
  document.getElementById('ov-sub').innerHTML =
    'Has aconseguit <b style="color:#f0efe8">' + G.score + ' punts</b> en ' + G.rounds + ' rondes' +
    '<br>Record: <b style="color:#EF9F27">' + G.best + ' pts</b>';
  document.getElementById('overlay').style.display = 'flex';
  hid('b-pas', true); hid('b-sal', true);
}
function nova() {
  if (!G.run) return;
  G.estat = 'idle'; G.selEsq = null; G.prim = null;
  G.i1 = Math.floor(Math.random() * NC);
  do { G.i2 = Math.floor(Math.random() * NC); } while (G.i2 === G.i1);
  hid('b-pas', true); hid('b-sal', false);
  draw(c1, G.i1); draw(c2, G.i2);
  setRes('', 'Troba els simbols comuns',
    'clica un simbol a la carta esquerra, despres el mateix a la dreta');
}
function passa() {
  if (!G.run || G.estat !== 'un') return;
  G.rounds++; document.getElementById('sr').textContent = G.rounds;
  G.streak = 0; updateStreak();
  setRes('ok1', '+1 pt - has passat', '');
  hid('b-pas', true); hid('b-sal', true);
  setTimeout(nova, 1000);
}
function salta() {
  if (!G.run) return;
  G.rounds++; document.getElementById('sr').textContent = G.rounds;
  G.streak = 0; updateStreak();
  var c = comuns(G.i1, G.i2);
  draw(c1, G.i1, c, []); draw(c2, G.i2, c, []);
  setRes('err', '0 pts - has saltat', 'Eren: #' + c.join(' i #'));
  soError();
  hid('b-pas', true); hid('b-sal', true);
  setTimeout(nova, 1400);
}
function sumaPunts(n) {
  G.score += n;
  document.getElementById('sc').textContent = G.score;
  G.streak++;
  updateStreak();
  if (G.streak > 0 && G.streak % 3 === 0) {
    G.secs = Math.min(G.secs + 5, TSECS);
    showBonus('+5 seg! Ratxa ' + G.streak + '!');
    soBonus();
  }
}
function clic(cv, esq, e) {
  e.preventDefault();
  if (!G.run) return;
  var p = getXY(e, cv), mx = p[0], my = p[1];
  var sy = JSON.parse(cv.dataset.sy || '[]');
  var ps = JSON.parse(cv.dataset.ps || '[]');
  var r0 = Math.floor(cv.width / 2 / 5.5) + 6;
  var cl = null;
  sy.forEach(function(s, i) {
    if (Math.hypot(mx - ps[i][0], my - ps[i][1]) < r0) cl = s;
  });
  if (cl === null) return;
  var c = comuns(G.i1, G.i2);

  if (esq) {
    if (G.estat === 'un' && cl === G.prim) {
      setRes('ok1', 'Ja has trobat aquest!', 'busca el SEGON o prem Passa'); return;
    }
    G.selEsq = cl;
    if (G.estat === 'idle') G.estat = 'espera';

    if (G.estat === 'un') {
      draw(c1, G.i1, [G.prim], [], cl);
    } else {
      draw(c1, G.i1, [], [], cl);
    }
    setRes(G.estat === 'un' ? 'ok1' : '',
      'Seleccionat: #' + cl,
      G.estat === 'un' ? 'clica el MATEIX a la dreta (2n simbol)' : 'clica el MATEIX a la carta dreta');
    return;
  }

 
  if (G.selEsq === null) return;
  if (c.indexOf(cl) < 0 || cl !== G.selEsq) {
    setRes('err', 'Incorrecte',
      G.estat === 'un' ? 'torna a intentar o prem Passa' : 'no coincideixen, torna-ho a intentar');
    soError();

    if (G.estat === 'un') draw(c1, G.i1, [G.prim], []);
    else draw(c1, G.i1);
    G.selEsq = null; return;
  }
  if (G.estat === 'idle' || G.estat === 'espera') {
    G.prim = cl; G.estat = 'un';
    sumaPunts(1);
    draw(c1, G.i1, [G.prim], []); draw(c2, G.i2, [G.prim], []);
    setRes('ok1', '+1 pt! Simbol #' + cl + ' trobat',
      'busca el 2n per +1 pt mes, o prem Passa');
    soEncert();
    hid('b-pas', false); hid('b-sal', true);
    G.selEsq = null;
  } else if (G.estat === 'un') {
    if (cl === G.prim) {
      setRes('ok1', 'Ja has trobat aquest!', 'busca el SEGON diferent o prem Passa');
      draw(c1, G.i1, [G.prim], []);
      G.selEsq = null; return;
    }
    sumaPunts(1);
    G.rounds++;
    document.getElementById('sr').textContent = G.rounds;
    draw(c1, G.i1, c, []); draw(c2, G.i2, c, []);
    setRes('ok2', '+2 pts! Els 2 simbols trobats!', 'Comuns: #' + c.join(' i #'));
    soDoble();
    hid('b-pas', true); hid('b-sal', true);
    G.selEsq = null; G.estat = 'idle';
    setTimeout(nova, 1600);
  }
}
function ini() {
  G.score = 0; G.rounds = 0; G.secs = TSECS; G.run = true;
  G.estat = 'idle'; G.selEsq = null; G.prim = null; G.streak = 0;
  document.getElementById('sc').textContent = '0';
  document.getElementById('sr').textContent = '0';
  document.getElementById('st').textContent = '2:00';
  document.getElementById('tbar').style.width = '100%';
  document.getElementById('tbar').style.background = '#1D9E75';
  document.getElementById('overlay').style.display = 'none';
  document.getElementById('streak').style.display = 'none';
  hid('b-ini', true); hid('b-pas', true); hid('b-sal', true);
  if (G.timer) clearInterval(G.timer);
  G.timer = setInterval(tick, 1000);
  nova();
}
function rei() { hid('b-ini', false); ini(); }

var c1 = document.getElementById('c1');
var c2 = document.getElementById('c2');

function btn(id, fn) {
  var el = document.getElementById(id), lk = false;
  el.addEventListener('touchend', function(e) {
    e.preventDefault();
    if (lk) return;
    lk = true; fn();
    setTimeout(function() { lk = false; }, 600);
  });
  el.addEventListener('click', function() { if (!lk) fn(); });
}
btn('b-ini', ini);
btn('b-pas', passa);
btn('b-sal', salta);
btn('b-rei', rei);

function canv(cv, esq) {
  var lk = false;
  cv.addEventListener('touchstart', function(e) {
    e.preventDefault();
    if (lk) return;
    lk = true; clic(cv, esq, e);
    setTimeout(function() { lk = false; }, 600);
  }, {passive: false});
  cv.addEventListener('click', function(e) { if (!lk) clic(cv, esq, e); });
}
canv(c1, true);
canv(c2, false);

var nd = 0, tot = imgs.length;
imgs.forEach(function(im) {
  function d() { if (++nd === tot) { draw(c1, 0); draw(c2, 1); } }
  if (im.complete && im.naturalWidth) d();
  else { im.onload = d; im.onerror = d; }
});
</script>
</body>
</html>'''

page = page.replace('__MATRIX__', matrix_json) \
           .replace('__FOTOS__', fotos_json) \
           .replace('__NC__', str(NUM_CARDS))

output_path = os.path.join(directori_script, "gran.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(page)

size_mb = os.path.getsize(output_path) / 1024 / 1024
print(f"\nFet! gran.html generat ({size_mb:.1f} MB)")
print(f"Ubicacio: {output_path}")
