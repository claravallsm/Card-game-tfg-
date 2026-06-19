import numpy as np

def rho(p):
    if isinstance(p, str): 
        return p  
    g, i = p
    return (g, (i + 1) % 11)

def sigma(p):
    if isinstance(p, str): 
        return p 
    g, i = p
    nou_i = (4 * i) % 11
    if 1 <= g <= 4:
        return (g + 1, nou_i)
    elif g == 5:
        return (1, nou_i)
    elif g == 6 or g == 7:
        return (g, nou_i)
        
    return p

def tau(p):
    if p == 'A': return 'B'
    if p == 'B': return 'A'
    g, i = p
    return (g, (10 * i) % 11)  

def get_orbit(base_block):
    orbit = [frozenset(base_block)]
    for block in orbit: 
        for move in [rho, sigma, tau]:
            new_block = frozenset(move(p) for p in block)
            if new_block not in orbit:
                orbit.append(new_block)
    return orbit

def generate_bibd_79_13_2():
    special_points = ['A', 'B']
    cyclic_points = [(g, i) for g in range(1, 8) for i in range(11)]
    all_points = special_points + cyclic_points
    
    point_to_idx = {p: idx for idx, p in enumerate(all_points)}

    b1 = ['A', 'B'] + [(6, i) for i in range(11)]
    b2 = ['A', 'B'] + [(7, i) for i in range(11)]
    b3 = ['A', (1,1), (1,4), (2,4), (2,5), (3,5), (3,9), (4,9), (4,3), (5,3), (5,1), (6,0), (7,0)]
    b4 = ['B', (1,10), (1,7), (2,7), (2,6), (3,6), (3,2), (4,2), (4,8), (5,8), (5,10), (6,0), (7,0)]
    b5 = [(1,0), (2,2), (2,9), (2,4), (2,7), (3,5), (3,6), (5,4), (5,7), (6,2), (6,9), (7,5), (7,6)]

    all_unique_blocks = set()
    all_unique_blocks.update(get_orbit(b1))
    all_unique_blocks.update(get_orbit(b2))
    all_unique_blocks.update(get_orbit(b3))
    all_unique_blocks.update(get_orbit(b4)) 
    all_unique_blocks.update(get_orbit(b5))
    
    all_blocks = list(all_unique_blocks)
    
    matrix = np.zeros((79, 79), dtype=int)
    for r_idx, block in enumerate(all_blocks):
        for p in block:
            c_idx = point_to_idx[p]
            matrix[r_idx][c_idx] = 1             
    return matrix

matrix = generate_bibd_79_13_2()
print("Obtenim la següent matriu d'incidència")
for i in range(79):
    print(matrix[i])

resultat = np.dot(matrix, matrix.T)
print("Comprovem el teorema ")
for i in range(79):
    fila = resultat[i]
    print(fila)
v_vector = np.ones(79, dtype=int)
resultat_k = np.dot(v_vector, matrix)
print(resultat_k)