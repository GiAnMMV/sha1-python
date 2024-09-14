from math import ceil

def leftrotate(a, b):
    return ((a << b) + (a << b >> 32)) & 0xFFFFFFFF

def sha1(file):
    l = len(file)
    file += b'\x80'
    file = file.ljust(64*ceil((l+9) / 64) - 8, b'\x00') + int.to_bytes(l*8, 8)

    res = [0x67452301, 0xEFCDAB89, 0x98BADCFE, 0x10325476, 0xC3D2E1F0]
    for c in range(len(file)//64):
        rA = res[0]
        rB = res[1]
        rC = res[2]
        rD = res[3]
        rE = res[4]
        
        chunk = file[c*64:(c+1)*64]
        words = []
        for i in range(16):
            words.append(int.from_bytes(chunk[i*4:(i+1)*4]))
        for i in range(64):
            words.append(leftrotate(words[i+13] ^ words[i+8] ^ words[i+2] ^ words[i], 1))
        
        for n in range(80):
            if n < 20:
                func = (rB & rC) | ((rB ^ 0xFFFFFFFF) & rD)
                const = 0x5A827999
            elif n < 40:
                func = rB ^ rC ^ rD
                const = 0x6ED9EBA1
            elif n < 60:
                func = (rB & rC) | (rB & rD) | (rC & rD)
                const = 0x8F1BBCDC
            else:
                func = rB ^ rC ^ rD
                const = 0xCA62C1D6

            func = func & 0xFFFFFFFF

            const = (leftrotate(rA, 5) + func + rE + const + words[n]) & 0xFFFFFFFF
            rE = rD
            rD = rC
            rC = leftrotate(rB, 30)
            rB = rA
            rA = const

        res[0] = (res[0] + rA) & 0xFFFFFFFF
        res[1] = (res[1] + rB) & 0xFFFFFFFF
        res[2] = (res[2] + rC) & 0xFFFFFFFF
        res[3] = (res[3] + rD) & 0xFFFFFFFF
        res[4] = (res[4] + rE) & 0xFFFFFFFF

    return int.to_bytes(res[0], 4) + int.to_bytes(res[1], 4) + int.to_bytes(res[2], 4) + int.to_bytes(res[3], 4) + int.to_bytes(res[4], 4)
