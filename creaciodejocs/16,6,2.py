import numpy as np

def generate_bibd_16_6_2_grid():
    # 1. Representem els 16 punts com coordenades (fila, columna) de 0 a 3
    points = [(r, c) for r in range(4) for c in range(4)]
    
    # 2. Inicialitzem la matriu d'incidència (16 punts x 16 blocs)
    matrix = np.zeros((16, 16), dtype=int)
    
    # 3. Construïm cada bloc B_i basat en el punt i-èssim
    for b_idx, (br, bc) in enumerate(points):
        for p_idx, (pr, pc) in enumerate(points):
            # El punt p està al bloc b si comparteixen fila o columna, però NO són el mateix punt.
            if (pr == br or pc == bc) and (pr, pc) != (br, bc):
                matrix[b_idx, p_idx] = 1
                
    return matrix

matrix = generate_bibd_16_6_2_grid()

for i in range(16):
    print(matrix[i])


resultat = np.dot(matrix, matrix.T)
print("Coeficients de la matriu resultant")
for i in range(16):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(16, dtype=int)

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
    
    fig, axes = plt.subplots(2, 3, figsize=(12, 8)) 

# Com que ara tenim 2 files, 'axes' és una matriu de 2x3. Amb .flatten() la tornem a convertir en una llista de 6 per poder fer el "for i in range(6)" igual que abans.
    axes = axes.flatten()
    fig.suptitle(f"Bloc associat al punt {bloc_triat}")

    for i, img_path in enumerate(imatges_bloc):
        img = Image.open(img_path) 
        axes[i].imshow(img)
        axes[i].axis('off')
    plt.show()

# Exemple: Mostrem el bloc del punt 0
mostrar_joc(0, matrix, noms_fitxers)