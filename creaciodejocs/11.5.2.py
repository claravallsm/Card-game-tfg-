import numpy as np
def generate_bibd_11_5_2():
    v = 11   
    base_block = [1, 3, 4, 5, 9] 
    matrix = np.zeros((v, v), dtype=int)

    for i in range(v):
        for punt in base_block:
            # Apliquem el desplaçament cíclic mòdul 11
            punt_mogut = (punt + i) % v
            matrix[i][punt_mogut] = 1
            
    return matrix

matrix = generate_bibd_11_5_2()
print(matrix)
resultat = np.dot(matrix, matrix.T)
print("Coeficients de la matriu resultant")
for i in range(11):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(11, dtype=int)

resultat_k = np.dot(v_vector, matrix)

print("Coeficients del vector resultant")
print(resultat_k)
