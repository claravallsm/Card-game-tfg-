import numpy as np
import galois

def create_dobble_matrix_galois(n):
    # n ha de ser una potència de primer (2, 3, 4, 5, 7, 8, 9, 11, 13, 16...)
    GF = galois.GF(n)
    elements = GF.elements # Tots els elements del cos {0, 1, ..., n-1}
    
    # 2. Generem els punts en coordenades homogènies (x, y, z)
    points = []
    
    # Tipus (x, y, 1) -> n^2 punts
    for x in elements:
        for y in elements:
            points.append(GF([x, y, 1]))
            
    # Tipus (x, 1, 0) -> n punts
    for x in elements:
        points.append(GF([x, 1, 0]))
        
    points.append(GF([1, 0, 0]))
    
    v = len(points) 
    
    lines = points 
    
    matrix = np.zeros((v, v), dtype=int)
    
    for j, line_vec in enumerate(lines):
        for i, point_vec in enumerate(points):
            dot_product = np.sum(line_vec * point_vec)
            if dot_product == 0:
                matrix[i, j] = 1
                
    return matrix

n = 7
matrix = create_dobble_matrix_galois(n)



resultat = np.dot(matrix, matrix.T)
print("Coeficients de la matriu resultant")
for i in range(n*n+n+1):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(n*n+n+1, dtype=int)

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
    
    fig, axes = plt.subplots(3, 3, figsize=(12, 8)) 

# Com que ara tenim 3 files, 'axes' és una matriu de 3x3. Amb .flatten() la tornem a convertir en una llista de 6 per poder fer el "for i in range(6)" igual que abans.
    axes = axes.flatten()
    fig.suptitle(f"Bloc associat al punt {bloc_triat}")
    for i, img_path in enumerate(imatges_bloc):
        img = Image.open(img_path) 
        axes[i].imshow(img)
        axes[i].axis('off')
    plt.show()