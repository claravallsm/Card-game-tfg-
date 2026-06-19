from sympy.combinatorics import Permutation
from sympy.combinatorics.perm_groups import PermutationGroup

b= Permutation([ [2, 4, 3]])
c = Permutation([[1, 6, 5], [2, 4, 3]])
d = Permutation([[2, 3], [4, 6]])
G = PermutationGroup(b,c, d)

mida_grup = G.order()
print(f"La mida del grup generat és: {mida_grup}")