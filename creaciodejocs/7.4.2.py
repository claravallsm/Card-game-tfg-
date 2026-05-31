import numpy as np

def generate_bibd_7_4_2():
    v = 7
    base_block = [0, 1, 2, 4]  # p-1 /n = los que genera     6/2=3 ne generen 3 els quadrats + el 0
    matrix = np.zeros((v, v), dtype=int)

    for i in range(v):
        for punt in base_block:
            # Fem la rotació cíclica mòdul 7
            punt_mogut = (punt + i) % v
            matrix[i][punt_mogut] = 1
            
    return matrix

matrix = generate_bibd_7_4_2()
print(matrix)
resultat = np.dot(matrix, matrix.T)
print("Coeficients de la matriu resultant")
for i in range(7):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(7, dtype=int)

resultat_k = np.dot(v_vector, matrix)

print("Coeficients del vector resultant")
print(resultat_k)
