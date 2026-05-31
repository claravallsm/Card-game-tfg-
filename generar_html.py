import numpy as np
import base64
import os

def generate_bibd_37_9_2():
    v = 37
    base_block = [1, 7, 9, 10, 12, 16, 26, 33, 34]
    matrix = np.zeros((v, v), dtype=int)
    for i in range(v):
        for punt in base_block:
            matrix[i][(punt + i) % v] = 1
    return matrix

def img_a_base64(ruta):
    with open(ruta, "rb") as f:
        return "data:image/jpeg;base64," + base64.b64encode(f.read()).decode()

FOTOS = r"C:\Users\USER\Desktop\FOTOS TFG"

# 33 arreu + 4 primers animals
noms_fitxers = []
for i in range(33):
    noms_fitxers.append(os.path.join(FOTOS, f"arreu_{i}.jpg"))

ruta_animals = os.path.join(FOTOS, "animals")
animals = sorted([f for f in os.listdir(ruta_animals) if f.endswith(".jpg")])[:4]
for a in animals:
    noms_fitxers.append(os.path.join(ruta_animals, a))

matrix = generate_bibd_37_9_2()
imatges_b64 = [img_a_base64(f) for f in noms_fitxers]

cartes = []
for bloc_idx in range(37):
    indices = [int(x) for x in np.where(matrix[bloc_idx] == 1)[0]]
    cartes.append(indices)

import json
cartes_json = json.dumps(cartes)
imatges_json = json.dumps(imatges_b64)

html = f"""<!DOCTYPE html>
<html lang="ca">
<head>
<meta charset="UTF-8">
<title>Joc BIBD (37,9,2)</title>
<style>
  body {{ font-family: sans-serif; background: #f0f0f0; padding: 20px; text-align: center; }}
  h1 {{ color: #333; }}
  .cartes {{ display: flex; gap: 40px; justify-content: center; margin-top: 30px; }}
  .carta {{
    background: white; border-radius: 50%;
    width: 320px; height: 320px;
    display: grid; grid-template-columns: repeat(3, 1fr);
    gap: 5px; padding: 15px;
    box-shadow: 0 4px 10px rgba(0,0,0,0.2);
  }}
  .carta img {{
    width: 100%; height: 85px;
    object-fit: contain; cursor: pointer;
    border-radius: 8px; transition: transform 0.1s;
  }}
  .carta img:hover {{ transform: scale(1.1); }}
  #missatge {{ font-size: 24px; margin-top: 20px; font-weight: bold; }}
  #punts {{ font-size: 20px; color: #555; }}
  button {{
    margin-top: 20px; padding: 10px 30px;
    font-size: 18px; border-radius: 10px;
    border: none; background: #4CAF50;
    color: white; cursor: pointer;
  }}
  button:hover {{ background: #45a049; }}
</style>
</head>
<body>
<h1>🎴 Joc de cartes BIBD (37,9,2)</h1>
<div id="punts">Punts: 0</div>
<div id="missatge"></div>
<div class="cartes">
  <div class="carta" id="carta1"></div>
  <div class="carta" id="carta2"></div>
</div>
<button onclick="novaRonda()">Nova ronda</button>

<script>
const cartes = {cartes_json};
const imatges = {imatges_json};
let punts = 0;
let simbolComú = -1;
let carta1Idx, carta2Idx;

function novaRonda() {{
  document.getElementById("missatge").textContent = "";
  carta1Idx = Math.floor(Math.random() * 37);
  do {{ carta2Idx = Math.floor(Math.random() * 37); }} while (carta2Idx === carta1Idx);
  
  const c1 = cartes[carta1Idx];
  const c2 = cartes[carta2Idx];
  const comuns = c1.filter(x => c2.includes(x));
  simbolComú = comuns[0];
  
  mostrarCarta("carta1", c1, carta1Idx);
  mostrarCarta("carta2", c2, carta2Idx);
}}

function mostrarCarta(id, simbols, cartaIdx) {{
  const div = document.getElementById(id);
  div.innerHTML = "";
  simbols.forEach(idx => {{
    const img = document.createElement("img");
    img.src = imatges[idx];
    img.onclick = () => comprovar(idx, cartaIdx);
    div.appendChild(img);
  }});
}}

function comprovar(idx, cartaIdx) {{
  if (idx === simbolComú) {{
    punts++;
    document.getElementById("punts").textContent = "Punts: " + punts;
    document.getElementById("missatge").textContent = "✅ Correcte!";
    document.getElementById("missatge").style.color = "green";
    setTimeout(novaRonda, 1000);
  }} else {{
    document.getElementById("missatge").textContent = "❌ Incorrecte!";
    document.getElementById("missatge").style.color = "red";
  }}
}}

novaRonda();
</script>
</body>
</html>"""

with open("joc.html", "w", encoding="utf-8") as f:
    f.write(html)

print("Fet! Obre joc.html al navegador.")