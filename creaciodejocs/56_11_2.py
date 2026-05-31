import numpy as np

def rho(p):
    g, i = p        
    nova_i = (i + 1) % 7 
    return (g, nova_i) 

def sigma(p):
    g, i = p
    if g == 1: return (2, (2 * i) % 7)
    if g == 2: return (3, (2 * i) % 7)
    if g == 3: return (1, (2 * i) % 7)
    if g == 4: return (5, (2 * i) % 7)
    if g == 5: return (6, (2 * i) % 7)
    if g == 6: return (4, (2 * i) % 7)
    if g == 7: return (7, (2 * i) % 7)
    if g == 8: return (8, (2 * i) % 7)

def tau(p):
    g, i = p
    if g == 1: return (4, (6 * i) % 7)
    if g == 2: return (5, (6 * i) % 7)
    if g == 3: return (6, (6 * i) % 7)
    if g == 4: return (1, (6 * i) % 7) # invers de 6 es (6*6=36=1)
    if g == 5: return (2, (6 * i) % 7)
    if g == 6: return (3, (6 * i) % 7)
    if g == 7: return (8, (6 * i) % 7)
    if g == 8: return (7, (6 * i) % 7)

def get_orbit(base_block):
    orbit = [frozenset(base_block)]
    for block in orbit: 
        for move in [rho, sigma, tau]:
            new_block = frozenset(move(p) for p in block)
            if new_block not in orbit:
                orbit.append(new_block)
    return orbit

def generate_bibd_56_11_2():
    # (família, membre) on família ∈ [1,8] i membre ∈ [0,6]
    points = [(g, i) for g in range(1, 9) for i in range(7)]
    point_to_idx = {p: idx for idx, p in enumerate(points)}
    
   
    b1 = [(1,1), (2,2), (3,4), (4,1), (5,2), (6,4), (7,0), (7,3), (7,6), (7,5), (8,0)]
    b2 = [(1,2), (1,5), (2,2), (2,5), (3,1), (3,6), (4,0), (4,1), (4,6), (7,1), (8,6)]

    blocks_set_1 = get_orbit(b1)
    blocks_set_2 = get_orbit(b2)
    all_blocks = list(blocks_set_1) + list(blocks_set_2)

    matrix = np.zeros((56, 56), dtype=int)
    for row_idx, block in enumerate(all_blocks):
        for p in block:
            col_idx = point_to_idx[p]
            matrix[row_idx][col_idx] = 1    
    return matrix

matrix = generate_bibd_56_11_2()

resultat = np.dot(matrix, matrix.T)
print("Coeficients de la matriu resultant")
for i in range(56):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(56, dtype=int)

resultat_k = np.dot(v_vector, matrix)

print("Coeficients del vector resultant")
print(resultat_k)
from PIL import Image
import matplotlib.pyplot as plt
import os

directori_script = os.path.dirname(os.path.abspath(__file__))
ruta_carpeta = os.path.join(directori_script, "FOTOS")

arxius_reals = sorted(
    [f for f in os.listdir(ruta_carpeta)],
    key=lambda x: int(n) if (n := ''.join(filter(str.isdigit, x))) else 0
)
noms_fitxers = [os.path.join(ruta_carpeta, f) for f in arxius_reals]


def obtenir_imatges_del_bloc(bloc_idx, llista_fotos, matriu):
    # Busquem quins punts tenen un '1' en la fila del bloc escollit
    indices_punts = np.where(matriu[bloc_idx] == 1)[0]
    # Retornem les rutes de les fotos corresponents
    return [llista_fotos[i] for i in indices_punts]


def mostrar_joc(bloc_triat, matriu, fotos):
    imatges_bloc = obtenir_imatges_del_bloc(bloc_triat, fotos, matriu)
    
    fig, axes = plt.subplots(1, 11, figsize=(12, 8)) 

# Com que ara tenim 3 files, 'axes' és una matriu de 3x3. Amb .flatten() la tornem a convertir en una llista de 6 per poder fer el "for i in range(6)" igual que abans.
    axes = axes.flatten()
    fig.suptitle(f"Bloc associat al punt {bloc_triat}")
    for i, img_path in enumerate(imatges_bloc):
        img = Image.open(img_path) 
        axes[i].imshow(img)
        axes[i].axis('off')
    plt.show()

# Exemple: Mostrem el bloc del punt 0
mostrar_joc(0, matrix, noms_fitxers)