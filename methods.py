# 10000000000000000000000000010 = [29,2] = 268435458
# 11111111111111111111111111111 = 536870911


def bytes_from_file(filename, chunksize=2**13):
    with open(filename, "rb") as f:
        while True:
            chunk = f.read(chunksize)
            if chunk:
                for b in chunk:
                    yield b
            else:
                break


def lfsr(filename, register):
    if filename[len(filename) - 4:] == '.cph':
        filetemp = filename[:(len(filename) - 4)]
        file_out = open(filetemp, 'wb')
    else:
        file_out = open(filename + '.cph', 'wb')
    mask = 268435458
    mask_obr = 536870911
    b_arr = bytearray()
    b_arr_key = bytearray()
    for b in bytes_from_file(filename):
        key_byte = 0
        for i in range(7, -1, -1):
            check = register & mask
            if register >= 268435456:
                key_byte += 2 ** i
            register <<= 1
            if check == 268435456 or check == 2:
                register += 1
            register &= mask_obr
        b_arr.append(b ^ key_byte)
        b_arr_key.append(key_byte)
    file_out.write(b_arr)
    file_out.close()
    return b_arr_key


def make_ascii_key(key):
    result = bytearray()
    for i in range(len(key)):
        result.append(int(key[i]))
    return result


def RC4(filename, key):
    key = make_ascii_key(key.split(' '))
    S = [i for i in range(256)]
    j = 0
    for i in range(256):
        j = (j + S[i] + key[i % len(key)]) % 256
        S[i], S[j] = S[j], S[i]
    if filename[len(filename) - 5:] == '.cphr':
        filetemp = filename[:(len(filename) - 5)]
        file_out = open(filetemp, 'wb')
    else:
        file_out = open(filename + '.cphr', 'wb')
    b_arr = bytearray()
    b_arr_key = bytearray()

    i = 0
    j = 0
    for b in bytes_from_file(filename):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        key_byte = S[(S[i] + S[j]) % 256]
        b_arr.append(b ^ key_byte)
        b_arr_key.append(key_byte)
    file_out.write(b_arr)
    file_out.close()
    return b_arr_key


if __name__ == "__main__":
    lfsr("bane.jpg", 536870911)
