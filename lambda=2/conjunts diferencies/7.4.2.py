import numpy as np

def generate_bibd_7_4_2():
    v = 7
    base_block = [0, 1, 2, 4] 
    matrix = np.zeros((v, v), dtype=int)

    for i in range(v):
        for punt in base_block:
            punt_mogut = (punt + i) % v
            matrix[i][punt_mogut] = 1        
    return matrix

matrix = generate_bibd_7_4_2()

print("Obtenim la següent matriu d'incidència")
for i in range(7):
    print(matrix[i])

resultat = np.dot(matrix, matrix.T)
print("Comprovem el teorema ")
for i in range(7):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(7, dtype=int)
resultat_k = np.dot(v_vector, matrix)
print(resultat_k)
