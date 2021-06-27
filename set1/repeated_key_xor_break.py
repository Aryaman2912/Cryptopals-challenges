import base64

def hamming_distance(s, t):
    hd = 0
    for a,b in zip(s,t):
        hd += 1 - (a == b)

    return hd

def get_key_lengths(ciphertext):
    normalized_hamming_distances = {}
    for key_len in range(2, 40):
        substrings = [ciphertext[i:i+key_len] for i in range(0,len(ciphertext),key_len)]
        if len(substrings[-1]) != key_len:
            substrings.pop()
        total_hd = 0
        for x, y in zip(substrings, substrings[1:]):
            total_hd += hamming_distance(x,y)
        
        total_hd /= (len(substrings) - 1)

        normalized_hd = total_hd / key_len

        normalized_hamming_distances[key_len] = normalized_hd

    normalized_hamming_distances = sorted(normalized_hamming_distances,key=normalized_hamming_distances.get)
    possible_key_lengths = normalized_hamming_distances[:min(5,len(normalized_hamming_distances))]

    return possible_key_lengths

s1 = "fuse fuel for falling flocks"
s2 = "wokka wokka!!!"

def get_score(plaintext):
    pass
def single_key_xor(ciphertext, key):
    output = b''

    for byte in ciphertext:
        output += bytes([byte ^ key])
    
    return output

def get_key_byte(ciphertext):
    for key in range(256):
        plaintext = single_key_xor(ciphertext,key)
        score = get_score(plaintext)

def get_plaintexts(ciphertext, possible_key_lengths):
    plaintexts = []
    for key_len in possible_key_lengths:
        key = b''
        for i in range(key_len):
            block = b''
            for j in range(i, len(ciphertext), key_len):
                block += ciphertext[j]
        
        key += get_key_byte(ciphertext)
            

def repeated_key_xor_break(ciphertext):
    possible_key_lengths = get_key_lengths(ciphertext)
    possible_plaintexts = get_plaintexts(ciphertext, possible_key_lengths)
    print(possible_key_lengths)
    return "",""

def main():
    with open('file.txt') as file:
        ciphertext = base64.b64decode(file.read())

    plaintext, key = repeated_key_xor_break(ciphertext)


if __name__ == '__main__':
    main()