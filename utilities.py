def decode(bit_string):
    decoded_list = []
    x = 1
    while bit_string != 0:
        if bit_string & 1:
            decoded_list.append(x)
        x += 1
        bit_string >>= 1

    return decoded_list

# def distance_to_goal(matrix):
#     x = [e for sub in matrix for e in sub]
#     return x.count(0)