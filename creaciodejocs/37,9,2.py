import numpy as np

def generate_bibd_37_9_2():
    v = 37
    base_block = [1, 7, 9, 10, 12, 16, 26, 33, 34] # potencies a la ^4 com 37-1 /4 = 9 com : $a^{p-1} \equiv 1$ fermat
    matrix = np.zeros((v, v), dtype=int)

    for i in range(v):
        for punt in base_block:
            # Sumem 'i' a cada punt del bloc base i apliquem mòdul
            punt_mogut = (punt + i) % v
            matrix[i][punt_mogut] = 1
    return matrix


matrix= generate_bibd_37_9_2()
print(matrix)
resultat = np.dot(matrix, matrix.T)
print("Coeficients de la matriu resultant")
for i in range(37):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(37, dtype=int)

resultat_k = np.dot(v_vector, matrix)

print("Coeficients del vector resultant")
print(resultat_k)



from PIL import Image
import matplotlib.pyplot as plt
import os

import random

directori_script = os.path.dirname(os.path.abspath(__file__))
noms_fitxers = []

# Subcarpetes: 3 de cada
carpetes = ["animals", "aliments", "fenomens atmosferics"]
for carpeta in carpetes:
    ruta = os.path.join(directori_script, "FOTOS TFG", carpeta)
    arxius = sorted([f for f in os.listdir(ruta) if f.endswith(".jpg")])
    seleccio = random.sample(arxius, min(3, len(arxius)))
    noms_fitxers += [os.path.join(ruta, f) for f in seleccio]

# Arreu: directament a FOTOS TFG
ruta_arreu = os.path.join(directori_script, "FOTOS TFG")
arxius_arreu = sorted([f for f in os.listdir(ruta_arreu) if f.startswith("arreu") and f.endswith(".jpg")])
seleccio_arreu = random.sample(arxius_arreu, 37 - 3*len(carpetes))
noms_fitxers += [os.path.join(ruta_arreu, f) for f in seleccio_arreu]

def obtenir_imatges_del_bloc(bloc_idx, llista_fotos, matriu):
    # Busquem quins punts tenen un '1' en la fila del bloc escollit
    indices_punts = np.where(matriu[bloc_idx] == 1)[0]
    # Retornem les rutes de les fotos corresponents
    return [llista_fotos[i] for i in indices_punts]

def mostrar_joc(bloc_triat, matriu, fotos):
    imatges_bloc = obtenir_imatges_del_bloc(bloc_triat, fotos, matriu)
    
    fig, axes = plt.subplots(3, 3, figsize=(12, 8)) 

# Com que ara tenim 3 files, 'axes' és una matriu de 3x3. Amb .flatten() la tornem a convertir en una llista de 6 per poder fer el "for i in range(6)" igual que abans.
    axes = axes.flatten()
    fig.suptitle(f"Bloc associat al punt {bloc_triat}")
    for i, img_path in enumerate(imatges_bloc):
        img = Image.open(img_path) 
        axes[i].imshow(img)
        axes[i].axis('off')
    plt.show()

mostrar_joc(0, matrix, noms_fitxers)
mostrar_joc(1, matrix, noms_fitxers)
