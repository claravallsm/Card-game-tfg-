import numpy as np

def generate_bibd_56_11_2_from_pdf():
    # 1. Definim els generadors del grup a, b, c, d sobre els 56 punts (pàg. 5-6 del PDF)
    # Convertim a indexació de base 0 (restant 1 a cada número) per comoditat en Python.
    
    # Permutació 'a': producte de cicles de longitud 7
    perm_a_cycles = [
        [1, 2, 3, 4, 5, 6, 7], [8, 9, 10, 11, 12, 13, 14], [15, 16, 17, 18, 19, 20, 21],
        [22, 23, 24, 25, 26, 27, 28], [29, 30, 31, 32, 33, 34, 35],
        [36, 37, 38, 39, 40, 41, 42], [43, 44, 45, 46, 47, 48, 49],
        [50, 51, 52, 53, 54, 55, 56]
    ]
    
    # Permutació 'b'
    perm_b_cycles = [
        [1], [45], [2, 3, 7], [4, 5, 6], [8, 27, 42], [9, 10, 26], [11, 38, 25], 
        [12, 19, 37], [13, 21, 18], [14, 36, 20], [15, 34, 17], [16, 35, 33], 
        [22, 31, 53], [23, 51, 30], [24, 39, 50], [28, 54, 41], [29, 52, 32], 
        [40, 55, 56], [43, 44, 46], [47, 48, 49]
    ]
    
    # Permutació 'c'
    perm_c_cycles = [
        [1], [2, 8, 41], [3, 27, 28], [4, 36, 31], [5, 20, 53], [6, 14, 22], 
        [7, 42, 54], [9, 29, 34], [10, 52, 17], [11, 24, 46], [12, 30, 48], 
        [13, 55, 33], [15, 26, 32], [16, 21, 56], [18, 40, 35], [19, 23, 49], 
        [25, 50, 44], [37, 51, 47], [38, 39, 43], [45]
    ]
    
    # Permutació 'd'
    perm_d_cycles = [
        [1], [2, 34], [3, 54], [4, 39], [5, 13], [6, 29], [7, 56], [8], [9, 44], 
        [10, 16], [11], [12, 19], [14], [15, 41], [17, 55], [18, 52], [20, 42], 
        [21, 24], [22, 26], [23], [25], [27, 36], [28, 40], [30, 47], [31, 33], 
        [32, 50], [35, 43], [37, 45], [38], [46, 53], [48], [49, 51]
    ]

    # Funció auxiliar per convertir una llista de cicles en un diccionari o llista de mapeig (0-indexed)
    def cycles_to_permutation(cycles):
        p = list(range(56))
        for cycle in cycles:
            for idx in range(len(cycle)):
                current_val = cycle[idx] - 1
                next_val = cycle[(idx + 1) % len(cycle)] - 1
                p[current_val] = next_val
        return p

    # Construïm l'acció de les funcions
    act_a = cycles_to_permutation(perm_a_cycles)
    act_b = cycles_to_permutation(perm_b_cycles)
    act_c = cycles_to_permutation(perm_c_cycles)
    act_d = cycles_to_permutation(perm_d_cycles)

    # 2. Definim el Bloc Inicial unió l'òrbita canònica (pàg. 5)
    # El document diu: {1} U {12, 19, 23, 30, 37, 45, 47, 48, 49, 51}
    base_block = frozenset([x - 1 for x in [1, 12, 19, 23, 30, 37, 45, 47, 48, 49, 51]])

    # 3. Generem tota l'òrbita de blocs aplicant les transformacions del grup de forma iterativa
    all_blocks = [base_block]
    
    # Farem un bucle d'expansió per trobar els 56 blocs únics generats per l'acció de G
    for block in all_blocks:
        for perm in [act_a, act_b, act_c, act_d]:
            new_block = frozenset(perm[point] for point in block)
            if new_block not in all_blocks:
                all_blocks.append(new_block)
                if len(all_blocks) == 56:
                    break
        if len(all_blocks) == 56:
            break

    # 4. Construcció de la matriu d'incidència (56 x 56)
    matrix = np.zeros((56, 56), dtype=int)
    for row_idx, block in enumerate(all_blocks):
        for point in block:
            matrix[row_idx][point] = 1 
            
    return matrix

# --- EXECUCIÓ I COMPROVACIÓ DEL TEOREMA ---

matrix = generate_bibd_56_11_2_from_pdf()
print("Obtenim la següent matriu d'incidència")
for i in range(56):
    print(matrix[i])

resultat = np.dot(matrix, matrix.T)
print("Comprovem el teorema ")
for i in range(56):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(56, dtype=int)
resultat_k = np.dot(v_vector, matrix)
print(resultat_k)

