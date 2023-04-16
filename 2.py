from cryptography.hazmat.primitives.ciphers import algorithms, modes, Cipher
aes = algorithms.AES

CBCkey = '140b41b22a29beb4061bda66b6747e14'
CBCc = ['4ca00ff4c898d61e1edbf1800618fb2828a226d160dad07883d04e008a7897ee2e4b7465d5290d0c0e6c6822236e1daafb94ffe0c5da05d9476be028ad7c1d81', '5b68629feb8606f9a6667670b75b38a5b4832d0f26e1ab7da33249de7d4afc48e713ac646ace36e872ad5fb8a512428a6e21364b0c374df45503473c5242a253']

CTRkey = '36f18357be4dbd77f050515c73fcf9f2'
CTRc = ['69dda8455c7dd4254bf353b773304eec0ec7702330098ce7f7520d1cbbb20fc388d1b0adb5054dbd7370849dbf0b88d393f252e764f1f5f7ad97ef79d59ce29f5f51eeca32eabedd9afa9329', '770b80259ec33beb2561358a9f2dc617e46218c0a53cbeca695ae45faa8952aa0e311bde9d4e01726d3184c34451']

def xor(a, b):
    return bytes([x ^ y for x, y in zip(a, b)])

def CBCdecipher(key, c):
    key = bytes.fromhex(key)
    c = bytes.fromhex(c)
    AESdecipher = Cipher(algorithms.AES(key), modes.ECB()).decryptor()

    l = []
    for i in range(len(c)-16,0,-16):
        m = AESdecipher.update(c[i:i+16])
        m = xor(m, c[i-16:i])
        if i == len(c)-16:
            m = m[:-m[-1]]
        # print(m)
        l.append(m)
    l.reverse()
    return b''.join(l)

def CTRdecipher(key, c):
    key = bytes.fromhex(key)
    c = bytes.fromhex(c)

    AESencipher = Cipher(algorithms.AES(key), modes.ECB()).encryptor()
    iv = c[:16]

    l = []
    for i in range(16,len(c),16):
        iv1 = iv[:-1]+bytes([iv[-1]+i//16-1])
        f = AESencipher.update(iv1)
        m = xor(c[i:i+16], f)
        l.append(m)
    return b''.join(l)

for i in range(2):
    print(CBCdecipher(CBCkey, CBCc[i]))

for i in range(2):
    print(CTRdecipher(CTRkey, CTRc[i]))
