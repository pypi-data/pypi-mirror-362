from BLSSLIB.sharedInfo import chars

def base64Encode(byte_data):
    result = ""
    bits = 0
    bit_count = 0

    for byte in byte_data:
        bits = (bits << 8) | byte
        bit_count += 8
        while bit_count >= 6:
            bit_count -= 6
            result += chars[(bits >> bit_count) & 0b111111]

    if bit_count > 0:
        result += chars[(bits << (6 - bit_count)) & 0b111111]

    return result
