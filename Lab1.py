import random
from decimal import Decimal
import math
import numpy as np
from datetime import datetime

def gcd(a:int, b:int):
    while a!=0 and b!=0:
        if a > b:
            a = a % b
        else:
            b = b % a   
    return (a+b)

def f(x):
    return x**2 + 1

def sieve_of_eratosthenes(limit, n):
    primes = []
    is_prime = [True] * (limit + 1)
    is_prime[0] = is_prime[1] = False
    for number in range(2, int(limit**0.5) + 1):
        if is_prime[number] and legandre(number, n):
            primes.append(number)
            for multiple in range(number * number, limit + 1, number):
                is_prime[multiple] = False
    for number in range(int(limit**0.5) + 1, limit + 1):
        if is_prime[number] and legandre(number, n):
            primes.append(number)
    return primes

def legandre(p ,n):
    n = n % p
    if not n:
        return 0
    if pow(n, (p - 1) // 2, p) == 1:
        return 1
    return 0

def base(a, B):
    base = [0]*len(B)
    if a < 0:
        a *= -1
        base[0] += 1
    while a > 1:
        for i in range(1, len(B)):
            if a%B[i] == 0:
                base[i] += 1
                a //= B[i]
                break
        else:
            return 0,0
    base_copy = base[:]
    for j in range(len(base_copy)):
        base_copy[j] %= 2
    return base, base_copy

def check_1(a, n):
    a = a**2%n
    if a > n-a:
        return -(n-a)
    else:
        return a

def simplification(matrix):
    matrix_t = np.transpose(matrix)
    for j in range(len(matrix_t)):
        index = np.argmax(matrix_t[j])
        if matrix_t[j][index] == 0:
            continue
        for k in range(len(matrix_t)):
            if k == j:
                continue
            if matrix_t[k][index] == 1:
                matrix_t[k] = (matrix_t[k] + matrix_t[j])%2
    matrix_t = np.transpose(matrix_t)
    return matrix_t
        
def solution_sle(matrix):
    matrix = simplification(matrix)
    matrix = np.array(matrix)
    full_solution = []
    for i in range(len(matrix)):
        temp = matrix[i][:]
        if sum(matrix[i]) == 0:
            full_solution.append(set([i]))
            continue
        index = np.where(temp == 1)[0]
        if sum(matrix[i]) >= 1: 
            solution = set()
            solution.add(i)
            for k in index:       
                 for j in range(len(matrix)):
                    if i == j:
                        continue
                    if np.array_equal(matrix[i], matrix[j]):
                        tmp_set = set([i, j])
                        if tmp_set not in full_solution:
                            full_solution.append(tmp_set)
                        continue
                    if sum(matrix[j]) == 1 and matrix[j][k] == 1:
                        solution.add(j)
                        temp = (matrix[j] + temp)%2
                        if sum(temp)==0:
                            if solution not in full_solution:
                                full_solution.append(solution)
                        break
    return full_solution
                                        
def test_millera_rabina(n, k=15):
    n = int(n)
    if n == 2 or n == 3:
        return True
    if n % 2 == 0 or n < 2:
        return False
    d, s = n-1, 0
    while d % 2 == 0:
        s += 1
        d //= 2
    for _ in range(k):
        x = random.randint(2, n-1)
        if gcd(x, n) > 1:
            return False
        x = pow(x, d, n)
        if x == 1 or x == n-1:
            continue
        for _ in range(1, s):  
            x = pow(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

def division(n):
    check = test_millera_rabina(n)
    if check:
        return n
    for i in range(2, 48):
        if n % i == 0:
            return i
    else:
        return False
    
def method_pollard(n):
    n = int(n)
    check = test_millera_rabina(n)
    if check:
        return n
    x = 5
    y = 5
    while True:
        x = f(x) % n
        y = f(f(y)) % n
        result = gcd((y-x)%n, n)
        if result == 1:
            continue
        return result
    
def method_brillhart_morrison(n):
    n = int(n)
    check = test_millera_rabina(n)
    if check:
        return n
    L = math.exp(math.sqrt(math.log(n) * math.log(math.log(n))))
    A = [1 / math.sqrt(2), math.sqrt(3)/2, math.sqrt(2)]
    for a in A:
        B = [-1] + sieve_of_eratosthenes(int(L**a), n)
        S, s, s_mod2 = [], [], []
        arr = [[1, 0]]
        sqrt_n = n ** 0.5
        alpha = sqrt_n
        a = int(alpha)
        v, u, b = 1, a, a
        arr.append([a, check_1(a, n)])
        temp = base(check_1(b, n), B)
        S.append(temp[0])
        if temp[0] != 0:
            s.append(temp[0])
            s_mod2.append(temp[1])
        while len(s) != len(B) + 1:
            v = (n - u ** 2) // v
            alpha = (sqrt_n + u) // v
            a = int(alpha)
            u = a * v - u
            b = (a * arr[-1][0] + arr[-2][0]) % n
            arr.append([b, check_1(b, n)])
            temp = base(check_1(b, n), B)
            S.append(temp[0])
            if temp[0] != 0:
                s.append(temp[0])
                s_mod2.append(temp[1])
        solution = solution_sle(s_mod2)
        for var in solution:
            X, Y = 1, 1
            for i in var:
                x = arr[(S.index(s[i]))+1][0]
                X = (X*x)%n
                y = arr[(S.index(s[i]))+1][1]
                Y = (Y*(y))
            Y = Decimal(Y).sqrt()
            Y = int(Y)%n
            dif = int(X-Y)
            d1 = gcd(dif%n, n)
            d2 = gcd(int(X+Y)%n, n)
            if d1 != 1 and d2 != 1:         
                return d1
    
def algorithm(n):
    result = {}
    n = Decimal(n)
    d = division(n)
    if d:
        print(f'Дільник {d} було знайдено методом пробних ділень')
        print(f'Час знаходження {datetime.now().strftime("%H:%M:%S.%f")[:-3]}\n')
        n = (n/d)
        if d in result:
            result[d] += 1
        else: 
            result[d] = 1
    p = method_pollard(n)
    if p:
        print(f'Дільник {p} було знайдено методом Полларда')
        print(f'Час знаходження {datetime.now().strftime("%H:%M:%S.%f")[:-3]}\n')
        n = (n/p)
        if p in result:
            result[p] += 1
        else: 
            result[p] = 1
    while n > 1:
        bm = method_brillhart_morrison(n)
        print(f'Дільник {bm} було знайдено методом Брілхарта-Моррісона')
        print(f'Час знаходження {datetime.now().strftime("%H:%M:%S.%f")[:-3]}\n')
        n = int(n/bm)
        if bm in result:
            result[bm] += 1
        else: 
            result[bm] = 1
    return result

def main():
    while True:
        global answer
        answer = {}      
        menu = input("""Оберіть дію, яку ви бажаєте виконати:
                     1. Брілхарт-Моррісон vs Полларда 
                     2. Канонічний розклад числа
                     3. Завершити роботу)\n""").lstrip()
        if menu == '1':
            n = [3009182572376191,1021514194991569,4000852962116741,15196946347083,499664789704823,269322119833303,679321846483919,96267366284849,61333127792637,2485021628404193]
            for i in n:
                print(f'Число, що факторизується: {i}')
                start = datetime.now()
                method_pollard(i)
                print(f'Час роботи методу Полларда: {datetime.now() - start}')
                start = datetime.now()
                method_brillhart_morrison(i)
                print(f'Час роботи методу Брілхарта-Моррісона: {datetime.now() - start}')               
        if menu == '2':
            n = int(input('Введіть число:'))
            start = datetime.now()
            result = algorithm(n)
            stop = datetime.now()
            print(f"""Початок роботи: {start.strftime("%H:%M:%S.%f")[:-3]}\nЗавершення роботи: {stop.strftime("%H:%M:%S.%f")[:-3]}""")
            print(f'\nКанонічний розклад числа {n}: {"*".join(f"{key}^{value}" for key, value in result.items())}')
        else:
            break
    
if __name__ == '__main__':
    main()