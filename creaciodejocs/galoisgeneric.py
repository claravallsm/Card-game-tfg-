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
