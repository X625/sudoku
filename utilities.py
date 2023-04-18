def decode(bit_string):
    decoded_list = []
    x = 1
    while bit_string != 0:
        if bit_string & 1:
            decoded_list.append(x)
        x += 1
        bit_string >>= 1

    return decoded_list
