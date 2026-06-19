import math

def es_quadrat_perfecte(n):
    if n < 0:
        return False
    r = math.isqrt(n)
    return r * r == n

resultats_valids = []
i=0
for k_prima in range(2, 55):
    l = 55 - k_prima
    for lambda_prima in range(0, k_prima):        
        numerador = k_prima * (k_prima - lambda_prima - 1)
        if numerador % l != 0:                   
            continue
        mu = numerador // l                        
        if mu <= 0:
            continue

        d = (lambda_prima - mu)**2 + 4 * (k_prima - mu)
        if not es_quadrat_perfecte(d):
            continue

        sqrt_d = math.isqrt(d)
        if sqrt_d == 0:
            continue

    
        num_mes  = 2*k_prima + (lambda_prima - mu)*(k_prima + l) - sqrt_d*(k_prima + l)
        num_menys = 2*k_prima + (lambda_prima - mu)*(k_prima + l) + sqrt_d*(k_prima + l)
        den = -2 * sqrt_d

        if num_mes % den == 0 and num_menys % (-den) == 0:
            i=i+1
            resultats_valids.append((i,k_prima, l, mu, lambda_prima, d))
           
for i,k_prima, l, mu, lambda_prima, d in resultats_valids:
    print(f"i={i} k'={k_prima} l={l} mu={mu} lambda'={lambda_prima} d={d}")
