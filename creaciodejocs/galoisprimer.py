import numpy as np

def create_dobble_matrix(n):
    points = []
    for x in range(n):
        for y in range(n):
            points.append((x, y, 1)) # genera n^2 punts
    for x in range(n):
        points.append((x, 1, 0)) # genera n punts
    points.append((1, 0, 0)) # un punt més
    
    v = len(points) 
    
    lines = points # per dualitat, les línies tenen els mateixos coeficients que els punts
    
    matrix = np.zeros((v, v), dtype=int)
    
    for j, (a, b, c) in enumerate(lines):
        for i, (x, y, z) in enumerate(points):
            # Si el producte escalar és 0 (mod n) com estem a Zn, el punt i està a la línia j
            if (a*x + b*y + c*z) % n == 0:
                matrix[i, j] = 1
                
    return matrix

n=7 #bibd del pla projectiu d'ordre 2
matrix = create_dobble_matrix(n)

for i in range(n):
    print(matrix[i])

resultat = np.dot(matrix, matrix.T)
print("Coeficients de la matriu resultant")
for i in range(n*n+n+1):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(n*n+n+1, dtype=int)

resultat_k = np.dot(v_vector, matrix)

print("Coeficients del vector resultant")
print(resultat_k)
