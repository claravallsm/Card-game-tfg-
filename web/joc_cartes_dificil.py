import numpy as np
from PIL import Image
import os, random, base64, json, io

import numpy as np
def generate_bibd_56_11_2(): 
    a = { 1:2, 2:3, 3:4, 4:5, 5:6, 6:7, 7:1, 8:9, 9:10, 10:11, 11:12, 12:13, 13:14, 14:8,
        15:16, 16:17, 17:18, 18:19, 19:20, 20:21, 21:15, 22:23, 23:24, 24:25, 25:26, 26:27, 27:28, 28:22,
        29:30, 30:31, 31:32, 32:33, 33:34, 34:35, 35:29, 36:37, 37:38, 38:39, 39:40, 40:41, 41:42, 42:36,
        43:44, 44:45, 45:46, 46:47, 47:48, 48:49, 49:43, 50:51, 51:52, 52:53, 53:54, 54:55, 55:56, 56:50}
    
    b = {1:1, 45:45, 2:3, 3:7, 7:2, 4:5, 5:6, 6:4, 8:27, 27:42, 42:8, 9:10, 10:26, 26:9,
        11:38, 38:25, 25:11, 12:19, 19:37, 37:12, 13:21, 21:18, 18:13, 14:36, 36:20, 20:14,
        15:34, 34:17, 17:15, 16:35, 35:33, 33:16, 22:31, 31:53, 53:22, 23:51, 51:30, 30:23,
        24:39, 39:50, 50:24, 28:54, 54:41, 41:28, 29:52, 52:32, 32:29, 40:55, 55:56, 56:40,
        43:44, 44:46, 46:43, 47:48, 48:49, 49:47}
    c = {1:1, 45:45, 2:8, 8:41, 41:2, 3:27, 27:28, 28:3, 4:36, 36:31, 31:4, 5:20, 20:53, 53:5,
        6:14, 14:22, 22:6, 7:42, 42:54, 54:7, 9:29, 29:34, 34:9, 10:52, 52:17, 17:10,
        11:24, 24:46, 46:11, 12:30, 30:48, 48:12, 13:55, 55:33, 33:13, 15:26, 26:32, 32:15,
        16:21, 21:56, 56:16, 18:40, 40:35, 35:18, 19:23, 23:49, 49:19, 25:50, 50:44, 44:25,
        37:51, 51:47, 47:37, 38:39, 39:43, 43:38}
    
    d = {1:1, 8:8, 11:11, 14:14, 23:23, 25:25, 38:38, 48:48, 2:34, 34:2, 3:54, 54:3, 4:39, 39:4, 
        5:13, 13:5, 6:29, 29:6, 7:56, 56:7, 9:44, 44:9, 10:16, 16:10, 12:19, 19:12, 15:41, 41:15, 17:55, 55:17, 18:52, 52:18,
        20:42, 42:20, 21:24, 24:21, 22:26, 26:22, 27:36, 36:27, 28:40, 40:28, 30:47, 47:30,
        31:33, 33:31, 32:50, 50:32, 35:43, 43:35, 37:45, 45:37, 46:53, 53:46, 49:51, 51:49}
    
    base_block = frozenset([1, 12, 19, 23, 30, 37, 45, 47, 48, 49, 51])

    all_blocks = [base_block]
    for block in all_blocks:
        for perm in [a, b, c, d]:
            new_block = frozenset(perm[point] for point in block)
            if new_block not in all_blocks:
                all_blocks.append(new_block)
                if len(all_blocks) == 56:
                    break
        if len(all_blocks) == 56:
            break
            
    matrix = np.zeros((56, 56), dtype=int)
    for row_idx, block in enumerate(all_blocks):
        for point in block:
            matrix[row_idx][point - 1] = 1
            
    return matrix

matrix = generate_bibd_56_11_2()
directori_script = os.path.dirname(os.path.abspath(__file__))

# Pugem un nivell per sortir de la carpeta 'web' i anar a la carpeta arrel del TFG
directori_arrel = os.path.dirname(directori_script) # Això ens porta a "fotos tfg"

noms_fitxers = []

# 1. Carregar fotos de les carpetes temàtiques (excloent la genèrica de moment)
carpetes_tematiques = ["animals", "aliments", "fenomens atmosferics"]
for carpeta in carpetes_tematiques:
    ruta = os.path.join(directori_arrel, carpeta)
    if os.path.exists(ruta):
        arxius = sorted([f for f in os.listdir(ruta) if f.endswith(".jpg")])
        seleccio = random.sample(arxius, len(arxius))
        noms_fitxers += [os.path.join(ruta, f) for f in seleccio]
    else:
        print(f"Alerta: No s'ha trobat la carpeta temàtica: {ruta}")

# 2. Carregar la resta d'imatges des de la carpeta 'fotos_generiques'
ruta_generiques = os.path.join(directori_arrel, "fotos_generiques")

if os.path.exists(ruta_generiques):
    arxius_generics = sorted([f for f in os.listdir(ruta_generiques) if f.endswith(".jpg")])
    quants_falten = 56 - len(noms_fitxers)
    
    if len(arxius_generics) >= quants_falten:
        seleccio_generica = random.sample(arxius_generics, quants_falten)
    else:
        seleccio_generica = arxius_generics
        
    noms_fitxers += [os.path.join(ruta_generiques, f) for f in seleccio_generica]
else:
    print(f"Error: No s'ha trobat la carpeta 'fotos_generiques' a: {ruta_generiques}")

def foto_a_base64(path, mida=(300, 300)):
    img = Image.open(path).convert("RGB").resize(mida, Image.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    data = base64.b64encode(buf.getvalue()).decode("utf-8")
    return f"data:image/jpeg;base64,{data}"

print(f"Convertint {len(noms_fitxers)} fotos...")
fotos_b64 = []
for i, path in enumerate(noms_fitxers):
    fotos_b64.append(foto_a_base64(path))
    print(f"  {i+1}/56: {os.path.basename(path)}")

matrix_json = json.dumps(matrix.tolist())
fotos_json  = json.dumps(fotos_b64)

page = '''<!DOCTYPE html>
<html lang="ca">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>Find the Two (Difficult Version) - BIBD Game</title>
    <style>
        :root {
            --bg: #0e0e0f; 
            --sur: #1a1a1c; 
            --sur2: #242426;
            --acc: #1D9E75; 
            --txt: #f0efe8; 
            --mut: #6b6b70;
            --bor: rgba(255,255,255,0.08); 
            --warn: #EF9F27; 
            --err: #E24B4A;
        }
        
        * { 
            box-sizing: border-box; 
            margin: 0; 
            padding: 0; 
            -webkit-tap-highlight-color: transparent; 
        }
        
        body { 
            background: var(--bg); 
            color: var(--txt); 
            font-family: system-ui, -apple-system, sans-serif;
            min-height: 100vh; 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
        }
        
        header { 
            width: 100%; 
            max-width: 900px; 
            padding: 1.5rem 1.5rem 0.5rem; 
        }
        
        h1 { 
            font-size: 1.6rem; 
            color: var(--acc); 
            font-weight: 700;
        }
        
        .sub { 
            font-size: 0.8rem; 
            color: var(--mut); 
            margin-top: 4px; 
        }
        
        .stats { 
            display: flex; 
            gap: 12px; 
            padding: 0.75rem 1.5rem; 
            width: 100%; 
            max-width: 900px; 
            flex-wrap: wrap; 
        }
        
        .stat { 
            background: var(--sur); 
            border: 1px solid var(--bor); 
            border-radius: 8px;
            padding: 8px 16px; 
            font-size: 0.85rem; 
            color: var(--mut); 
        }
        
        .stat b { 
            color: var(--txt); 
        }
        
        #tbar-wrap { 
            width: calc(100% - 3rem); 
            max-width: 900px; 
            background: var(--sur);
            border-radius: 99px; 
            height: 8px; 
            margin: 0.75rem 0; 
            overflow: hidden; 
        }
        
        #tbar { 
            height: 100%; 
            border-radius: 99px; 
            background: var(--acc);
            transition: width 0.25s linear, background 0.4s; 
        }
        
        #game { 
            width: 100%; 
            max-width: 900px; 
            padding: 0 1rem; 
            position: relative; 
        }
        
        .row { 
            display: flex; 
            gap: 1.5rem; 
            justify-content: center; 
            align-items: center;
            margin-bottom: 1.25rem; 
            flex-wrap: wrap; 
        }
        
        .cwrap { 
            display: flex; 
            flex-direction: column; 
            align-items: center; 
            gap: 8px; 
        }
        
        .clabel { 
            font-size: 0.7rem; 
            color: var(--mut); 
            letter-spacing: 0.1em; 
            text-transform: uppercase; 
            font-weight: 600;
        }
        
        canvas { 
            border-radius: 50%; 
            border: 1.5px solid var(--bor);
            touch-action: none; 
            display: block; 
            background: var(--sur); 
            box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        }
        
        .rbox { 
            background: var(--sur); 
            border: 1px solid var(--bor); 
            border-radius: 14px;
            padding: 1rem 1.25rem; 
            text-align: center; 
            margin-bottom: 0.75rem;
            min-height: 75px; 
            display: flex; 
            flex-direction: column;
            align-items: center; 
            justify-content: center; 
            gap: 4px; 
            transition: border-color 0.3s, box-shadow 0.3s; 
        }
        
        .rbox.ok1 { border-color: var(--warn); }
        .rbox.ok2 { border-color: var(--acc); }
        .rbox.err { border-color: var(--err); }
        
        .rmain { 
            font-size: 1.05rem; 
            font-weight: 600; 
        }
        
        .rsub { 
            font-size: 0.8rem; 
            color: var(--mut); 
        }
        
        .hint { 
            background: var(--sur2); 
            border: 1px solid var(--bor); 
            border-radius: 8px;
            padding: 6px 12px; 
            font-size: 0.75rem; 
            color: var(--mut); 
            text-align: center; 
            margin-bottom: 0.75rem; 
        }
        
        .btns { 
            display: flex; 
            gap: 12px; 
            justify-content: center; 
            margin-bottom: 1.5rem; 
            flex-wrap: wrap; 
        }
        
        button { 
            background: transparent; 
            border: 1px solid var(--bor); 
            color: var(--txt);
            padding: 14px 28px; 
            border-radius: 10px; 
            font-size: 1rem; 
            font-weight: 600;
            cursor: pointer; 
            touch-action: manipulation; 
            -webkit-appearance: none; 
            user-select: none; 
            transition: background 0.2s, transform 0.1s;
        }
        
        button:active {
            transform: scale(0.98);
        }
        
        button.acc { 
            background: var(--acc); 
            color: #0e0e0f; 
            border-color: var(--acc); 
        }
        
        button.hid { 
            display: none !important; 
        }
        
        #overlay { 
            position: absolute; 
            inset: 0; 
            background: rgba(14,14,15,0.95);
            border-radius: 14px; 
            display: none; 
            flex-direction: column;
            align-items: center; 
            justify-content: center; 
            gap: 16px; 
            z-index: 10; 
            padding: 2rem; 
        }
        
        #overlay .big { 
            font-size: 2rem; 
            font-weight: 700; 
            color: var(--acc); 
        }
        
        #overlay .osub { 
            font-size: 0.95rem; 
            color: var(--mut); 
            text-align: center; 
            line-height: 1.8; 
        }
        
        #pantalla-ini {
            position: fixed; 
            inset: 0; 
            background: var(--bg);
            display: flex; 
            align-items: center; 
            justify-content: center;
            z-index: 200; 
            padding: 1.5rem;
        }
        
        .ini-box {
            background: var(--sur); 
            border: 1px solid var(--bor);
            border-radius: 16px; 
            padding: 2.25rem; 
            max-width: 480px;
            width: 100%; 
            display: flex; 
            flex-direction: column; 
            gap: 1.25rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        }
        
        .ini-box h2 { 
            color: var(--acc); 
            font-size: 1.6rem; 
            text-align: center; 
        }
        
        .ini-sub { 
            font-size: 0.8rem; 
            color: var(--mut); 
            text-align: center; 
            margin-top: -8px;
        }
        
        .ini-box ul { 
            list-style: none; 
            display: flex; 
            flex-direction: column; 
            gap: 0.75rem; 
        }
        
        .ini-box ul li {
            font-size: 0.85rem; 
            color: var(--mut);
            padding-left: 1rem; 
            border-left: 2px solid var(--acc); 
            line-height: 1.5;
        }
        
        .ini-box ul li b { 
            color: var(--txt); 
        }
        
        #b-comencar { 
            width: 100%; 
            padding: 16px; 
            font-size: 1.05rem; 
            margin-top: 0.5rem; 
        }
    </style>
</head>
<body>

<div id="pantalla-ini">
    <div class="ini-box">
        <h2>Com es juga</h2>
        <p class="ini-sub">BIBD(56, 11, 2) &middot; 2 minuts</p>
        <ul>
            <li>Tens <b>2 minuts</b> per trobar el màxim de símbols possibles.</li>
            <li>En cada parell de cartes hi ha <b>exactament 2 símbols en comú</b>.</li>
            <li>Clica un símbol a la carta esquerra, i després el <b>mateix</b> a la dreta.</li>
            <li>Pots trobar <b>1 símbol (+1 pt)</b> i prémer Passa per assegurar el punt.</li>
            <li>O trobar els <b>2 símbols (+2 pts)</b> per aconseguir la màxima puntuació.</li>
            <li>Si et quedes encallat, prem <b>Salta (0 pts)</b> per canviar de ronda.</li>
        </ul>
        <button class="acc" id="b-comencar" onclick="document.getElementById('pantalla-ini').style.display='none'; ini();">Clica per començar</button>
    </div>
</div>

<header>
    <h1>Find the two</h1>
    <div class="sub">BIBD(56,11,2) &middot; 2 minuts</div>
</header>

<div class="stats">
    <div class="stat">Punts: <b id="sc">0</b></div>
    <div class="stat">Rondes: <b id="sr">0</b></div>
    <div class="stat">Temps: <b id="st">2:00</b></div>
</div>

<div id="tbar-wrap"><div id="tbar" style="width:100%"></div></div>

<div id="game">
    <div class="row">
        <div class="cwrap">
            <div class="clabel">Carta 1</div>
            <canvas id="c1" width="260" height="260"></canvas>
        </div>
        <div class="cwrap">
            <div class="clabel">Carta 2</div>
            <canvas id="c2" width="260" height="260"></canvas>
        </div>
    </div>
    
    <div class="hint">1 símbol comú &rarr; +1 pt &nbsp;&middot;&nbsp; tots 2 &rarr; +2 pts</div>
    <div class="rbox" id="res"><div class="rsub">Prem per començar el repte</div></div>
    
    <div class="btns">
        <button class="acc hid" id="b-ini">Inicia</button>
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
var NC     = 55;

var G = {
    i1:0, i2:1,
    estat:'idle',
    selEsq:null,
    prim:null,
    score:0, rounds:0,
    secs:120,
    timer:null,
    run:false,
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
    var p = [];
    var dx = R * 0.46;                                  // separació horitzontal de les files de 3
    var ys = [R - R*0.60, R - R*0.20, R + R*0.20, R + R*0.60]; // 4 nivells verticals

    // Fila 1 (3)
    p.push([R - dx, ys[0]], [R, ys[0]], [R + dx, ys[0]]);
    // Fila 2 (3)
    p.push([R - dx, ys[1]], [R, ys[1]], [R + dx, ys[1]]);
    // Fila 3 (3)
    p.push([R - dx, ys[2]], [R, ys[2]], [R + dx, ys[2]]);
    // Fila 4 (2, centrada)
    p.push([R - dx*0.5, ys[3]], [R + dx*0.5, ys[3]]);

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
    var r0 = Math.floor(R / 4.8);
    
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
            if (isSel) {
                ctx.beginPath(); ctx.arc(x,y,r+6,0,Math.PI*2);
                ctx.fillStyle = 'rgba(239,159,39,0.25)'; ctx.fill();
                ctx.strokeStyle = '#EF9F27'; ctx.lineWidth = 2.5; ctx.stroke();
            }
            if (h) {
                ctx.beginPath(); ctx.arc(x,y,r+6,0,Math.PI*2);
                ctx.fillStyle = 'rgba(29,158,117,0.22)'; ctx.fill();
                ctx.strokeStyle = '#1D9E75'; ctx.lineWidth = 2.5; ctx.stroke();
            }
            var im = imgs[s];
            ctx.save();
            ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.clip();
            if (im.complete && im.naturalWidth) ctx.drawImage(im, x-r, y-r, r*2, r*2);
            else { ctx.fillStyle = '#333'; ctx.fill(); }
            ctx.restore();
            if (isSel) {
                ctx.strokeStyle = '#EF9F27'; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.arc(x,y,r,0,Math.PI*2); ctx.stroke();
            }
            if (h) {
                ctx.strokeStyle = '#1D9E75'; ctx.lineWidth = 2;
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
        '<br>Record personal: <b style="color:#EF9F27">' + G.best + ' pts</b>';
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
    setRes('', 'Troba els símbols comuns',
        'clica un símbol a la carta esquerra, després el mateix a la dreta');
}
function passa() {
    if (!G.run || G.estat !== 'un') return;
    G.rounds++; document.getElementById('sr').textContent = G.rounds;
    setRes('ok1', '+1 pt - Has passat', '');
    hid('b-pas', true); hid('b-sal', true);
    setTimeout(nova, 1000);
}
function salta() {
    if (!G.run) return;
    G.rounds++; document.getElementById('sr').textContent = G.rounds;
    var c = comuns(G.i1, G.i2);
    draw(c1, G.i1, c, []); draw(c2, G.i2, c, []);
    setRes('err', '0 pts - Has saltat', 'Eren els símbols #' + c.join(' i #'));
    hid('b-pas', true); hid('b-sal', true);
    setTimeout(nova, 1400);
}
function clic(cv, esq, e) {
    e.preventDefault();
    if (!G.run) return;
    var p = getXY(e, cv), mx = p[0], my = p[1];
    var sy = JSON.parse(cv.dataset.sy || '[]');
    var ps = JSON.parse(cv.dataset.ps || '[]');
    var r0 = Math.floor(cv.width / 2 / 4.8) + 6;
    var cl = null;
    sy.forEach(function(s, i) {
        if (Math.hypot(mx - ps[i][0], my - ps[i][1]) < r0) cl = s;
    });
    if (cl === null) return;
    var c = comuns(G.i1, G.i2);

    if (esq) {
        if (G.estat === 'un' && cl === G.prim) {
            setRes('ok1', 'Ja has trobat aquest!', 'busca el SEGON o prem Passa');
            return;
        }
        G.selEsq = cl;
        if (G.estat === 'idle') G.estat = 'espera';
        if (G.estat === 'un') {
            draw(c1, G.i1, [G.prim], [], cl);
        } else {
            draw(c1, G.i1, [], [], cl);
        }
        setRes(G.estat === 'un' ? 'ok1' : '',
            'Seleccionat: Símbol #' + cl,
            G.estat === 'un' ? 'clica el MATEIX a la dreta (2n símbol)' : 'clica el MATEIX a la carta dreta');
        return;
    }

    if (G.selEsq === null) return;
    if (c.indexOf(cl) < 0 || cl !== G.selEsq) {
        setRes('err', 'Incorrecte',
            G.estat === 'un' ? 'torna a intentar o prem Passa' : 'no coincideixen, torna-ho a intentar');
        if (G.estat === 'un') draw(c1, G.i1, [G.prim], []);
        else draw(c1, G.i1);
        G.selEsq = null;
        return;
    }
    if (G.estat === 'idle' || G.estat === 'espera') {
        G.prim = cl; G.estat = 'un';
        G.score++; document.getElementById('sc').textContent = G.score;
        draw(c1, G.i1, [G.prim], []);
        draw(c2, G.i2, [G.prim], []);
        setRes('ok1', '+1 pt! Símbol #' + cl + ' trobat',
            'busca el 2n per +1 pt més, o prem Passa');
        hid('b-pas', false); hid('b-sal', true);
        G.selEsq = null;
    } else if (G.estat === 'un') {
        if (cl === G.prim) {
            setRes('ok1', 'Ja has trobat aquest!', 'busca el SEGON diferent o prem Passa');
            draw(c1, G.i1, [G.prim], []);
            G.selEsq = null; return;
        }
        G.score++; G.rounds++;
        document.getElementById('sc').textContent = G.score;
        document.getElementById('sr').textContent = G.rounds;
        draw(c1, G.i1, c, []); draw(c2, G.i2, c, []);
        setRes('ok2', '+2 pts! Els 2 símbols trobats!', 'Comuns: #' + c.join(' i #'));
        hid('b-pas', true); hid('b-sal', true);
        G.selEsq = null; G.estat = 'idle';
        setTimeout(nova, 1600);
    }
}
function ini() {
    G.score = 0; G.rounds = 0; G.secs = TSECS; G.run = true;
    G.estat = 'idle'; G.selEsq = null; G.prim = null;
    document.getElementById('sc').textContent = '0';
    document.getElementById('sr').textContent = '0';
    document.getElementById('st').textContent = '2:00';
    document.getElementById('tbar').style.width = '100%';
    document.getElementById('tbar').style.background = '#1D9E75';
    document.getElementById('overlay').style.display = 'none';
    hid('b-ini', true); hid('b-pas', true); hid('b-sal', true);
    if (G.timer) clearInterval(G.timer);
    G.timer = setInterval(tick, 1000);
    nova();
}
function rei() { ini(); }

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

page = page.replace('__MATRIX__', matrix_json).replace('__FOTOS__', fotos_json)

output_path = os.path.join(directori_script, "joc_cartes_dificil.html")
with open(output_path, "w", encoding="utf-8") as f:
    f.write(page)

size_mb = os.path.getsize(output_path) / 1024 / 1024
print(f"\nFet! joc_cartes_dificil.html generat ({size_mb:.1f} MB)")
print(f"Ubicacio: {output_path}")