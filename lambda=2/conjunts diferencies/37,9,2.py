import numpy as np

def generate_bibd_37_9_2():
    v = 37
    base_block = [1, 7, 9, 10, 12, 16, 26, 33, 34] 
    matrix = np.zeros((v, v), dtype=int)

    for i in range(v):
        for punt in base_block:
            punt_mogut = (punt + i) % v
            matrix[i][punt_mogut] = 1
    return matrix


matrix= generate_bibd_37_9_2()
print("Obtenim la següent matriu d'incidència")
for i in range(37):
    print(matrix[i])

resultat = np.dot(matrix, matrix.T)
print("Comprovem el teorema ")
for i in range(37):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(37, dtype=int)
resultat_k = np.dot(v_vector, matrix)
print(resultat_k)