import copy
import random
 
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

def numList2blocks(L,n):
    '''Take a list of integers(each between 0 and 127), and combines them into block size
    n using base 256. If len(L) % n != 0, use some random junk to fill L to make it '''

    returnList = []
    toProcess = copy.copy(L)
    if len(toProcess) % n != 0:
        for i in range (0, n - len(toProcess) % n):
            toProcess.append(random.randint(32, 126))
    for i in range(0, len(toProcess), n):
        block = 0
        for j in range(0, n):
            block += toProcess[i + j] << (8 * (n - j - 1))
        returnList.append(block)

    print('RETURNLIST', returnList)
    return returnList
 
def encrypt(message, modN, e, blockSize):
    '''given a string message, public keys and blockSize, encrypt using
    RSA algorithms.'''
    cipher = []
    numList = [message]
    numBlocks = numList2blocks(numList, blockSize)

    for blocks in numBlocks:
        cipher.append(modExp(blocks, e, modN))
    return cipher
 
if __name__=='__main__':

    file_n = open('n.txt')
    n = int(file_n.read())
    file_d = open('d.txt')
    d = int(file_d.read())
    file_e = open('e.txt')
    e = int(file_e.read())

    message = input('Give us a number to encrypt: ')

    cipher = encrypt(message, n, e, 1)
    print('The cipher number is: ')
    print(cipher[0])

    result = open('cipher.txt', 'w')
    result.write('{0}'.format(cipher[0]))