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

