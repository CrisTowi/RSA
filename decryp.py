import copy

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
 
def blocks2numList(blocks,n):
    '''inverse function of numList2blocks.'''
    toProcess = copy.copy(blocks)
    returnList = []
    for numBlock in toProcess:
        inner = []
        for i in range(0, n):
            inner.append(numBlock)
            numBlock >>= 8
        inner.reverse()
        returnList.extend(inner)
    return returnList
 
def decrypt(secret, modN, d, blockSize):
    '''reverse function of encrypt'''
    numBlocks = []
    numList = []
    for blocks in secret:
        numBlocks.append(modExp(blocks, d, modN))
    numList = blocks2numList(numBlocks, blockSize)
    message = numList[0]
    return message
 
if __name__=='__main__':
    file_n = open('n.txt')
    n = int(file_n.read())
    file_d = open('d.txt')
    d = int(file_d.read())
    file_e = open('e.txt')
    e = int(file_e.read())

    file_e = open('cipher.txt')
    cipher = [int(file_e.read())]

    message = decrypt(cipher, n, d, 1)
    print(message)