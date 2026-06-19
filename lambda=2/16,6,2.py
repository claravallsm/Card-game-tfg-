import numpy as np

def generate_bibd_16_6_2_grid():
    points = [(r, c) for r in range(4) for c in range(4)]
    matrix = np.zeros((16, 16), dtype=int)
    
    for b_idx, (br, bc) in enumerate(points):
        for p_idx, (pr, pc) in enumerate(points): 
            if (pr == br or pc == bc) and (pr, pc) != (br, bc):
                matrix[b_idx, p_idx] = 1              
    return matrix

matrix = generate_bibd_16_6_2_grid()
print("Obtenim la següent matriu d'incidència")
for i in range(16):
    print(matrix[i])

resultat = np.dot(matrix, matrix.T)
print("Comprovem el teorema ")
for i in range(16):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(16, dtype=int)
resultat_k = np.dot(v_vector, matrix)
print(resultat_k)