from datetime import datetime
import sympy
import time

def discrete_logarithm(alpha, beta, n, timeout_minutes=5):
    current_x = 0
    start_time = time.time()
    timeout_seconds = timeout_minutes * 60
    while True:
        if int(pow(alpha, current_x, n+1)) == beta:
            return current_x
        current_x += 1
        elapsed_time = time.time() - start_time
        if elapsed_time > timeout_seconds:
            return None
        
def decimal_to_binary(n):
    binary = bin(n)[2:]
    return binary

def horner_scheme(x, power, module):
    binary_representation = decimal_to_binary(power)
    result = 1
    for i in binary_representation:
        result = (result * result) % module
        if i == '1':
            result = (result * x) % module
    return result

def canonical_representation(n):
    factors = sympy.factorint(n)
    return factors

def search_r(base, n, alpha):
    r = {}
    for element in base:
        temp = []
        for i in range(element):
            arg = horner_scheme(alpha, int(n*i/element), n+1)
            temp.append(arg)
        r[element] = temp
    return r

def search_equation(n, key, alpha, beta, arg1, arg2):
    x = arg2.index(horner_scheme(beta, int(n/key), n+1))
    power = x
    for i in range(1, arg1):
        a_rev = horner_scheme(alpha, power, n+1) 
        temp = beta*pow(a_rev, -1, n+1)
        res = horner_scheme(temp,int(n/key**(i+1)), n+1)
        answer = arg2.index(res)
        power += answer*key**i
        x = (x + answer*key**i) % key**arg1
    return x, key**arg1

def chinese_remainder_theorem(sle):
    M = 1
    solution = 0
    for p1, p2 in sle:
        M *= p2
    for p1, p2 in sle:
        Mi = int(M/p2)
        Ni = pow(Mi, -1, p2)
        solution = (solution + p1*Ni*Mi)%M
    return solution

def Pohlig_Hellman(alpha, beta, n):
    can_repr = canonical_representation(n)
    r = search_r(can_repr.keys(), n, alpha)
    sle = []
    for key in can_repr:
        sle.append(search_equation(n, key, alpha, beta, can_repr[key], r[key]))
    return chinese_remainder_theorem(sle)

def main():
    alpha = int(input("a = "))
    beta = int(input("b = "))
    n = int(input("n = "))
    start = datetime.now()
    x = discrete_logarithm(alpha, beta, n)
    stop = datetime.now()
    print(f"\nAlgorithm running time: {stop-start}")
    print(f"x = {x}")
    start = datetime.now()
    x = Pohlig_Hellman(alpha, beta, n)
    stop = datetime.now()
    print(f"Algorithm running time: {stop-start}")
    print(f"x = {x}")

    
if __name__ == "__main__":
    main()
