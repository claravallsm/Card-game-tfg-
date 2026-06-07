import math
v = 56
lam = 0  

def is_perfect_square(n):
    if n < 0:
        return False
    r = int(math.isqrt(n))
    return r * r == n

solucions = []

for k in range(2, v - 1):
    l=v - 1 - k   
    numerador = k * (k - 1)
    denominador =  l  
    if numerador % denominador != 0:
        continue
    mu = numerador // denominador
    
    d = (lam - mu)**2 + 4 * (k - mu)
    if not is_perfect_square(d):
        continue
    
    sqrt_d = int(math.isqrt(d))
    kl = k + l
    
    num1 = 2*k + (lam - mu)*kl - sqrt_d*kl
    num2 = 2*k + (lam - mu)*kl + sqrt_d*kl
    den1 = -2 * sqrt_d
    den2 = 2 * sqrt_d

    if den1 == 0 or den2 == 0:
        continue
    
    if num1 % den1 != 0 or num2 % den2 != 0:
        continue
    print(f"k={k}, l={l}, mu={mu}, d={d}")
