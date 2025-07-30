from BLSSLIB.sharedInfo import chars

def base64Decode(encoded_str):
    bits = 0
    bit_count = 0
    result = bytearray()

    for char in encoded_str:
        index = chars.index(char)
        bits = (bits << 6) | index
        bit_count += 6
        while bit_count >= 8:
            bit_count -= 8
            result.append((bits >> bit_count) & 0xFF)

    return bytes(result)
