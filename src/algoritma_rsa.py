import random
import binascii
import codecs
from hashlib import sha1

def convert(s): # Convert string to ASCII
    return ([ord(c) for c in s])

def gcd(a, b):
    if (b != 0):
        return gcd(b, a%b)
    else:
        return a

def modulusInverse(a, b):
     
    for x in range(1, b):
        if (a * x) % b == 1:
            return x
    return -1

def fastModulusInverse(a, b):
    return fast(a, b-2, b)

def fast(x, y, z):
    result = 1
    while y > 0:
        if y % 2 == 1:
            result = (result * x) % z
        y = y // 2
        x = (x * x) % z
    return result

def isPrime(x):
    if x == 1:
        return False
    elif x == 2:
        return True
    else:
        for i in range (2, x):
            if (x % i == 0):
                return False
        return True

def generatePrime():
    while 1:
        p = random.getrandbits(6)
        if isPrime(p) and p > 11:
            break
    
    while 1:
        q = random.getrandbits(6)
        if isPrime(q) and q > 11 and q != p:
            break

    return p, q

def generateKey():
    p, q = generatePrime()
    
    # if both numbers prime
    n = p * q

    # totient of n = (p-1)(q-1)
    t = (p-1)*(q-1)

    # choose a number as public key
    publicKey = random.randrange(1, t)

    # check if publicKey is coprime with t
    c = gcd(publicKey,t)
    while c != 1:
        publicKey = random.randrange(1,t)
        c = gcd (publicKey,t)
    
    # create private key
    privateKey = modulusInverse(publicKey, t)

    # return public and private key
    return ((publicKey, n) , (privateKey, n))


def encrypt(key, plaintext):
    publicKey, n = key
    result = []
    #cipherText = [pow(ord(x), publicKey, n) for x in plaintext]
    for x in plaintext:
        cipherText = pow(ord(x), publicKey, n)
        result.append(hex(cipherText))
    return result
    
def decrypt(key, ciphertext):
    privateKey, n = key
    result = []
    for i in ciphertext:
        plain = (int(i, 16) for i in ciphertext)
    for j in plain:
        p = pow(j, privateKey, n)
        result.append(p)
    return result

# convert array to string TESTED
def listToString(list):
    n = len(list)
    result = ''
    for i in range(n):
        result = result + str(list[i]) + ' '
    return result

# implementasi library SHA-1
def hashFunction(message):
    hashed = sha1(message.encode("UTF-8")).hexdigest()
    return hashed

def sign(message, public):
    hashed = hashFunction(message)
    sign = encrypt(public, hashed)
    sign_str = listToString(sign)
    return "<ds>"+sign_str+"</ds>"

# search digital signature jika digital sign embedded dalam file TESTED
def searchSignature(message):
    signature = ''
    start = message.find("<ds>")
    if "<ds>" in message:
        end = message.find("</ds>")
        if "</ds>" in message:
            for i in range(start+4, end):
                signature += message[i]
    return signature

# verify jika digital signature di file terpisah TESTED tinggal ulik2 dikit    
def verify(receivedHash, message, private):
    ourHashed = hashFunction(message) #result hash mentah
    sign = decrypt(private, receivedHash)
    print(sign)
    sign_str = ''
    for i in range(len(sign)):
        sign_str += chr(sign[i])
    print(sign_str)
    if sign_str == ourHashed:
        return True
    else:
        return False

def splitter(signature):
    result = signature.split(" ")
    result.remove("")
    return result


if __name__ == '__main__':
    public, private = generateKey()

    print(" *** Your public key is ", public, " and your private key is ", private)

    message = input(" Enter a message (plaintext): ")
    encrypted_msg = encrypt(public, message)
    
    # print(" Your plaintext: ", message)
    # print(" Your message in ASCII", convert(message))
    # print(" Your encrypted message in hexadecimal is: ", (encrypted_msg))
    

    # print(" Decrypting message with private key ", private, " . . .")

    # decrypted_msg = decrypt(private,encrypted_msg)
    # print(" Your message in ASCII is: ", decrypted_msg)
    # print(" Your message: ", ''.join(chr(i) for i in decrypted_msg))

    hashed = hashFunction(message)
    # sign = encrypt(public, hashed)
    sign = sign(message, private)

    print(sign)

    if verify(splitter(searchSignature(sign)), message, public):
        print("success")
    else:
        print("failed")

# p sama q paling ngga >= 11 (?)
# n gabisa kurang dari ASCII plaintext