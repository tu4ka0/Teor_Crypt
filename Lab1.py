import random
from decimal import Decimal
import time
import math

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

def check(a, B):
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
            return 0, 0
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

def solution_sle(matrix):
    pass

def test_millera_rabina(n, k=15):
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
    answer[n] = 1
    return True

def division(n):
    for i in range(2, 48):
        if n % i == 0:
            t = time.time() - start
            if i in answer:
                answer[i] += 1
            else:
                answer[i] = 1
            n = Decimal(n)
            print(f'Дільник {i} знайдений методом пробних ділень')
            print(f'Час знаходження:{t} ')
            return int(n/i)
    else:
        return False
    
def method_pollard(n):
    x = 5
    y = 5
    while True:
        x = f(x) % n
        y = f(f(y)) % n
        result = gcd((y-x)%n, n)
        if result == 1:
            continue
        t = time.time() - start
        if result in answer:
            answer[result] += 1
        else:
            answer[result] = 1
        n = Decimal(n)
        #print(f'Дільник {result} знайдений р-методом Полларда')
        #print(f'Час знаходження:{t} ')
        return int(n/result)
    
def method_brillhart_morrison(n):
    L = math.exp(math.sqrt(math.log(n) * math.log(math.log(n))))
    a = 1 / math.sqrt(2)

    B = [-1] + sieve_of_eratosthenes(int(L**a), n)

    S, s, s_mod2 = [], [], []
    arr = [[1, 0]]

    sqrt_n = n ** 0.5
    alpha = sqrt_n
    a = int(alpha)

    v, u, b = 1, a, a
    arr.append([a, check_1(a, n)])

    temp = check(check_1(b, n), B)
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

        temp = check(check_1(b, n), B)
        S.append(temp[0])

        if temp[0] != 0:
            s.append(temp[0])
            s_mod2.append(temp[1])

    for i in s_mod2:
        print(i)
    #solution_sle(s_mod2)
    
def algorithm(n):
    check = test_millera_rabina(n)
    if check:
        return False
    temp = division(n)
    if temp:
        return temp   
    temp = method_pollard(n)
    return temp


def main():
    while True:
        global answer
        answer = {}      
        menu = input("""Оберіть дію, яку ви бажаєте виконати:
                     1. Порівняння швидкості спрацювання методу Полларда та методу Брiлхарта-Моррiсона 
                     2. Запустити алгортм пошуку канонічного розкладу
                     3. Завершити роботу)\n""").lstrip()
        if menu == '1':
            n = int(input('Введіть число:'))
            method_pollard(n)
        if menu == '2':
            n = int(input('Введіть число:'))
            method_brillhart_morrison(n)
        if menu == '3':
            user_input = int(input('Введіть число:'))
            n = user_input
            global start 
            start = time.time()
            while True:
                n = algorithm(n)
                if not n:
                    break
                else:
                    continue
            stop = time.time()
            print(f'Канонічний розклад числа {user_input}: {"*".join(f"{key}^{value}" for key, value in answer.items())}\nЧас роботи:{stop-start}')
        if menu == '4':
            break
    
if __name__ == '__main__':
    main()