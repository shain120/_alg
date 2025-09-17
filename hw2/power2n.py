# 方法 1
def power2na(n):
    return 2**n

# 方法 2a：用遞迴
def power2nb(n):
    if n == 0:
        return 1
    return power2nb(n-1)+power2nb(n-1)
    # power2n(n-1)+power2n(n-1)

# 方法2b：用遞迴
def power2nc(n):
    if n == 0:
        return 1
    return 2 * power2nc(n-1)

# 方法 3：用遞迴+查表
pow2 = [None]*1000
pow2[0] = 1
pow2[1] = 2

def power2nd(n):
    pass
    if not pow2[n] is None:
        return pow2[n]
    pow2[n] = 2 * power2nd(n-1)
    return pow2[n]
    # power2n(n-1)+power2n(n-1) 
    
print(power2nd(100))