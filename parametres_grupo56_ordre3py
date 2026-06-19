import math

def es_quadrat_perfecte(n):
    if n <= 0:
        return False
    r = math.isqrt(n)
    return r * r == n

resultats_valids = []

for k_prima in range(2, 55):
    l = 55 - k_prima
    numerador = k_prima * (k_prima - 1)
    if numerador % l != 0:
        continue

    mu = numerador // l
    lambda_prima = 0
    d = (lambda_prima - mu)**2 + 4 * (k_prima - mu)
    if not es_quadrat_perfecte(d):
        continue

    numerador_1 = 2*k_prima + (lambda_prima - mu)*(k_prima + l) + math.isqrt(d) * (k_prima + l)
    denominador_1 = 2 * math.isqrt(d)
    numerador__1 = 2*k_prima + (lambda_prima - mu)*(k_prima + l) + (-1) * math.isqrt(d) * (k_prima + l)
    denominador__1 = (-1) * 2 * math.isqrt(d)

    if (denominador_1 != 0 and numerador_1 %
         denominador_1 == 0) and \
       (denominador__1 != 0 and numerador__1 % denominador__1 == 0):
        resultats_valids.append((k_prima, l, mu, lambda_prima, d))


for k_prima, l, mu, lambda_prima, d in resultats_valids:
    print(f"k={k_prima} l={l} mu= {mu} lamda'={lambda_prima} {d}")