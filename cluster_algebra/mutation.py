from sympy import symbols, simplify
from copy import deepcopy

def mutate(B, xs, k):
    """
    Coefficient-free Fomin–Zelevinsky mutation at index k.
    B: n×n integer matrix (list of lists)
    xs: list of sympy symbols/expressions [x0,...,x_{n-1}]
    k:  mutation direction (0-based)
    Returns: (B_new, xs_new)
    """
    n = len(xs)
    # exchange relation for x_k'
    num1 = 1
    for i in range(n):
        if B[i][k] > 0:
            num1 *= xs[i]**B[i][k]
    num2 = 1
    for i in range(n):
        if B[i][k] < 0:
            num2 *= xs[i]**(-B[i][k])
    xk_new = (num1 + num2) / xs[k]

    # matrix mutation
    Bp = deepcopy(B)
    for i in range(n):
        for j in range(n):
            if i == k or j == k:
                Bp[i][j] = -B[i][j]
            else:
                Bp[i][j] = B[i][j] + max(B[i][k], 0)*B[k][j] + B[i][k]*max(-B[k][j], 0)

    xs_new = list(xs)
    xs_new[k] = simplify(xk_new)
    return Bp, xs_new

# Example: type A2
x0, x1 = symbols('x0 x1')
B = [[0, 1],
     [-1, 0]]

B1, X1 = mutate(B, [x0, x1], 0)   # mutate at 0
B2, X2 = mutate(B1, X1, 1)        # then at 1
print(B1, X1)
print(B2, X2)