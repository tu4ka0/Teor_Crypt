from datetime import datetime
import math
import random
import numpy as np
from functools import reduce
import sympy as sp

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

def sieve_of_eratosthenes(limit):
    primes = []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for number in range(2, int(limit**0.5) + 1):
        if is_prime[number]:
            primes.append(number)
            for multiple in range(number * number, limit + 1, number):
                is_prime[multiple] = False
    for number in range(int(limit**0.5) + 1, limit + 1):
        if is_prime[number]:
            primes.append(number)
    return primes

def check(n, factor_base):
    factors = dict.fromkeys(factor_base, 0)
    if n == 1:
        return 0
    for p in factor_base:
        while n % p == 0:
            factors[p] += 1
            n //= p
    if n > 1:
        return 0
    return factors

def subtract(arr1, arr2, n):
    for i in range(len(arr1)):
        arr1[i] = (arr1[i] - arr2[i])%n
    return arr1

def gcd(a,b):
    while b:
        a, b = b, a % b
    return a

def simple_arr(numbers):
    ncd = reduce(gcd, numbers)
    np_numbers = np.array(numbers)
    if ncd == 1:
        return list(np_numbers)
    return list(np.divide(np_numbers, ncd).astype(int))

def punkt_3(n, a, S):
    sle = []
    b = []
    len_s = len(S)
    while len(sle) < len_s:
        i = random.randint(0,n-1)
        temp = check(horner_scheme(a,i,n+1), S)
        if temp:
            temp = list(temp.values())
            temp = simple_arr(temp + [i] + [n])
            if temp[-1] != n:
                continue
            temp = temp[:-1]
            if temp not in sle:
                sle.append(temp[:-1])
                b.append(temp[-1])
    return sle, b
        
def solution_sle(n, a, S):
    while True:
        sle = punkt_3(n,a,S)
        matrix = sp.Matrix(sle[0])
        try:
            inv_matrix = matrix.inv_mod(n)
            break
        except:
            continue
    result = inv_matrix*sp.Matrix(sle[1])
    result = result.applyfunc(lambda x: x % n)
    return result

def punkt_4(a,b,n,S):
    while True:
        l = random.randint(0,n-1)
        temp = b*horner_scheme(a,l,n+1)%(n+1)
        temp1 = check(temp, S)
        if temp1:
            return list(temp1.values()), l
        
def answer(arg1, arg2, n):
    result = 0
    for i in range(len(arg1)):
        result +=arg1[i]*arg2[0][i]
    return (result - arg2[1])%n

def index_calculus(a, b, n):
    c = 3.38
    B = int(c*math.exp(0.5*math.sqrt(math.log(n) * math.log(math.log(n)))))
    S = sieve_of_eratosthenes(B)
    temp1 = list(solution_sle(n, a, S))
    temp2 = punkt_4(a,b,n,S)
    temp3 = answer(temp1, temp2, n)
    return temp3

def main():
    a = int(input("a = "))
    b = int(input("b = "))
    n = int(input("n = "))
    start = datetime.now()
    temp = index_calculus(a, b, n)
    print(f"x = {temp}")
    (print(f"\nAlgorithm running time: {datetime.now()-start}"))

if __name__ == "__main__":
    main()
