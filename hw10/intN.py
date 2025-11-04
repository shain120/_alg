import numpy as np

step = 0.1

def range(n):
    return [(0, 1)] * n

def integrate(f, rx):
    n = len(rx)

    def recursive_integrate(f, dim, vars):
        if len(dim) > 0:
            (a, b) = dim[0] #[0,1]
            
            total = 0.0
            for x in np.arange(a, b, step):
                total += recursive_integrate(f, dim[1:], vars + [x])
            return total
        else:
            # 所有變數都有值 → 計算函數值
            return f(*vars) * (step ** n)

    return recursive_integrate(f, rx, [])

def f(*args):
    return sum(x**2 for x in args)

print(integrate(f, range(4)))  
