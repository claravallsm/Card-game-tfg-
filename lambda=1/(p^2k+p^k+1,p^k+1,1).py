import numpy as np
import galois

def create_dobble_matrix_galois(n):
    GF = galois.GF(n)
    elements = GF.elements 
    points = []
    for x in elements:
        for y in elements:
            points.append(GF([x, y, 1]))
    for x in elements:
        points.append(GF([x, 1, 0]))
        
    points.append(GF([1, 0, 0]))
    lines = points 
    v = len(points) 
    
    matrix = np.zeros((v, v), dtype=int)
    
    for j, line_vec in enumerate(lines):
        for i, point_vec in enumerate(points):
            dot_product = np.sum(line_vec * point_vec)
            if dot_product == 0:
                matrix[i, j] = 1             
    return matrix

n = 4
matrix = create_dobble_matrix_galois(n)

print("Obtenim la següent matriu d'incidència")
for i in range(n*n+1):
    print(matrix[i])

resultat = np.dot(matrix, matrix.T)
print("Comprovem el teorema ")
for i in range(n*n+n+1):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(n*n+n+1, dtype=int)
resultat_k = np.dot(v_vector, matrix)

print(resultat_k)
