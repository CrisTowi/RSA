import random
import math
 
def euclid(a,b):
    '''returns the Greatest Common Divisor of a and b'''
    a = abs(a)
    b = abs(b)
 
    if a < b:
        a, b = b, a
 
    while b != 0:
        a, b = b, a % b
 
    return a
 
def coprime(L):
    '''returns 'True' if the values in the list L are all co-prime
       otherwier, it returns 'False'. '''
 
    for i in range (0, len(L)):
        for j in range (i + 1, len(L)):
            if euclid(L[i], L[j]) != 1:
                return False
 
    return True
 
def extendedEuclid(a,b):
    '''return a tuple of three values: x, y and z, such that x is
       the GCD of a and b, and x = y * a + z * b'''
    footprint = []

    if a < b:
        isASmallerThanB = True
        a, b = b, a
    else:
        isASmallerThanB = False
    while b != 0:
        footprint.append((a % b, 1, a, -(a//b), b))

        a, b = b, a % b
 

    footprint.reverse()
    footprint.pop(0)

    x = footprint[0][1]
    y = footprint[0][3]

    for i in range (1, len(footprint)):
        x_temp = x
        y_temp = y
        x = y_temp * footprint[i][1]
        y = y_temp * footprint[i][3] + x_temp
        #print (x, y)
 
    if (isASmallerThanB != True):
        return (a, x, y)
    else:
        return (a, y, x)
 
def modInv(a,m):
    '''returns the multiplicative inverse of a in modulo m as a
       positve value between zero and m-1'''

    if coprime([a, m]) == False:
        return 0
    else:
        linearcombination = extendedEuclid(a, m)
        return linearcombination[1] % m
 
 
def extractTwos(m):
    '''m is a positive integer. A tuple (s, d) of integers is returned
    such that m = (2 ** s) * d.'''

    assert m >= 0
    i = 0
    while m & (2 ** i) == 0:
        i += 1
    return (i, m >> i)
 
 
def int2baseTwo(x):
    '''x is a positive integer. Convert it to base two as a list of integers
    in reverse order as a list.'''

    assert x >= 0
    bitInverse = []
    while x != 0:
        bitInverse.append(x & 1)
        x >>= 1
    return bitInverse
 
def modExp(a,d,n):
    '''returns a ** d (mod n)'''

    assert d >= 0
    assert n >= 0
    base2D = int2baseTwo(d)
    base2DLength = len(base2D)
    modArray = []
    result = 1
    for i in range (1, base2DLength + 1):
        if i == 1:
            modArray.append(a % n)
        else:
            modArray.append((modArray[i - 2] ** 2) % n)
    for i in range (0, base2DLength):
        if base2D[i] == 1:
            result *= base2D[i] * modArray[i]
    return result % n
 
def millerRabin(n, k):
    '''Test to see if n is a prime number'''
    assert n >= 1

    assert k > 0

 
    if n == 2:
        return True

 
    if n % 2 == 0:
        return False

 
    extract2 = extractTwos(n - 1)
    s = extract2[0]
    d = extract2[1]
    assert 2 ** s * d == n - 1
 
    def tryComposite(a):

        x = modExp(a, d, n)
        if x == 1 or x == n - 1:
            return None
        else:
            for j in range (1,s):
                x = modExp(x, 2, n)
                if x == 1:
                    return False
                elif x == n - 1:
                    return None
            return False
 
    for i in range (0, k):
        a = random.randint(2, n - 2)
        if tryComposite(a) == False:
            return False
    return True
 
def findAPrime(a,b,k):
    '''Return a prime number between a and b. '''
    x = random.randint(a, b)
    for i in range(0, int(10 * math.log(x) + 3)):
        if millerRabin(x, k):
            return x
        else:
            x += 1
    raise ValueError
 
def newKey(a,b,k):
    ''' Try to find two large primes roughly between a and b '''
    try:
        p = findAPrime(a, b, k)
        while True:
            q = findAPrime(a, b, k)
            if q != p:
                break
    except:
        raise ValueError
    n = p * q
    m = (p-1) * (q-1)
    while True:
        e = random.randint(1, m)
        if coprime([e, m]):
            break
    d = modInv(e, m)
    return (n, e, d)

 
if __name__=='__main__':
    (n, e, d) = newKey(10**19, 10**20, 50)
    print ('n = {0}'.format(n))
    print ('e = {0}'.format(e))
    print ('d = {0}'.format(d))


    result = open('n.txt', 'w')
    result.write('{0}'.format(n))    
    result = open('e.txt', 'w')
    result.write('{0}'.format(e))    
    result = open('d.txt', 'w')
    result.write('{0}'.format(d))
