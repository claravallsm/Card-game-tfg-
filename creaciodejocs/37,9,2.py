import numpy as np

def generate_bibd_37_9_2():
    v = 37
    base_block = [1, 7, 9, 10, 12, 16, 26, 33, 34] # potencies a la ^4 com 37-1 /4 = 9 com : $a^{p-1} \equiv 1$ fermat
    matrix = np.zeros((v, v), dtype=int)

    for i in range(v):
        for punt in base_block:
            # Sumem 'i' a cada punt del bloc base i apliquem mòdul
            punt_mogut = (punt + i) % v
            matrix[i][punt_mogut] = 1
    return matrix


matrix= generate_bibd_37_9_2()
print(matrix)
resultat = np.dot(matrix, matrix.T)
print("Coeficients de la matriu resultant")
for i in range(37):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(37, dtype=int)

resultat_k = np.dot(v_vector, matrix)

print("Coeficients del vector resultant")
print(resultat_k)

