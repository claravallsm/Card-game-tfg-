import numpy as np

def rho(p):
    g, i = p        
    nova_i = (i + 1) % 7 
    return (g, nova_i) 

def sigma(p):
    g, i = p
    if g == 1: return (2, (2 * i) % 7)
    if g == 2: return (3, (2 * i) % 7)
    if g == 3: return (1, (2 * i) % 7)
    if g == 4: return (5, (2 * i) % 7)
    if g == 5: return (6, (2 * i) % 7)
    if g == 6: return (4, (2 * i) % 7)
    if g == 7: return (7, (2 * i) % 7)
    if g == 8: return (8, (2 * i) % 7)

def tau(p):
    g, i = p
    if g == 1: return (4, (6 * i) % 7)
    if g == 2: return (5, (6 * i) % 7)
    if g == 3: return (6, (6 * i) % 7)
    if g == 4: return (1, (6 * i) % 7) # invers de 6 es (6*6=36=1)
    if g == 5: return (2, (6 * i) % 7)
    if g == 6: return (3, (6 * i) % 7)
    if g == 7: return (8, (6 * i) % 7)
    if g == 8: return (7, (6 * i) % 7)

def get_orbit(base_block):
    orbit = [frozenset(base_block)]
    for block in orbit: 
        for move in [rho, sigma, tau]:
            new_block = frozenset(move(p) for p in block)
            if new_block not in orbit:
                orbit.append(new_block)
    return orbit

def generate_bibd_56_11_2():
    # (família, membre) on família ∈ [1,8] i membre ∈ [0,6]
    points = [(g, i) for g in range(1, 9) for i in range(7)]
    point_to_idx = {p: idx for idx, p in enumerate(points)}
    
   
    b1 = [(1,1), (2,2), (3,4), (4,1), (5,2), (6,4), (7,0), (7,3), (7,6), (7,5), (8,0)]
    b2 = [(1,2), (1,5), (2,2), (2,5), (3,1), (3,6), (4,0), (4,1), (4,6), (7,1), (8,6)]

    blocks_set_1 = get_orbit(b1)
    blocks_set_2 = get_orbit(b2)
    all_blocks = list(blocks_set_1) + list(blocks_set_2)

    matrix = np.zeros((56, 56), dtype=int)
    for row_idx, block in enumerate(all_blocks):
        for p in block:
            col_idx = point_to_idx[p]
            matrix[row_idx][col_idx] = 1    
    return matrix

matrix = generate_bibd_56_11_2()

resultat = np.dot(matrix, matrix.T)
print("Coeficients de la matriu resultant")
for i in range(56):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(56, dtype=int)

resultat_k = np.dot(v_vector, matrix)

print("Coeficients del vector resultant")
print(resultat_k)