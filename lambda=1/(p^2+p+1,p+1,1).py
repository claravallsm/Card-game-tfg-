import numpy as np

def create_dobble_matrix(n):
    points = []
    for x in range(n):
        for y in range(n):
            points.append((x, y, 1)) 
    for x in range(n):
        points.append((x, 1, 0))
    points.append((1, 0, 0)) 
    
    lines = points 
    v = len(points) 
    matrix = np.zeros((v, v), dtype=int)
    
    for j, (a, b, c) in enumerate(lines):
        for i, (x, y, z) in enumerate(points):
            if (a*x + b*y + c*z) % n == 0:
                matrix[i, j] = 1      
    return matrix

n=7 
matrix = create_dobble_matrix(n)
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
