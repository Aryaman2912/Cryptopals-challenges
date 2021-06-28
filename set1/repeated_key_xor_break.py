import base64
import string

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
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }
    return sum([character_frequencies.get(chr(byte), 0) for byte in plaintext.lower()])

def single_key_xor(ciphertext, key):
    output = b''

    for byte in ciphertext:
        output += bytes([byte ^ key])
    
    return output

def get_key_byte(ciphertext):
    probable_plaintexts = []
    for key in range(256):
        plaintext = single_key_xor(ciphertext,key)
        # print(plaintext)
        score = get_score(plaintext)
        # print(score)
        scores = {
            'plaintext':plaintext,
            'score': score,
            'key':key
            }
        probable_plaintexts.append(scores)
    # print(sorted(probable_plaintexts, key=lambda x: x['score'])[0])
    return sorted(probable_plaintexts, key=lambda x: x['score'], reverse=True)[0]

def repeated_key_xor(ciphertext, key):
    output = b''
    ind = 0

    for byte in ciphertext:
        output += bytes([byte ^ key[ind]])
        ind = (ind + 1) % len(key)
    
    return output

def get_plaintext(ciphertext, possible_key_lengths):
    plaintexts = []
    for key_len in possible_key_lengths:
        key = b''
        for i in range(key_len):
            block = b''
            for j in range(i, len(ciphertext), key_len):
                block += bytes([ciphertext[j]])
            # print(block)
            key += bytes([get_key_byte(block)['key']])
            # print(key)
        pt = repeated_key_xor(ciphertext, key)
        score = get_score(pt)
        d = {
            'pt' : pt,
            'score' : score,
            'key' : key
        }
        plaintexts.append(d)
        
    return sorted(plaintexts, key = lambda x: x['score'], reverse=True)[0]
        
    # return plaintexts

def repeated_key_xor_break(ciphertext):
    possible_key_lengths = get_key_lengths(ciphertext)
    # possible_key_lengths = [29]
    possible_plaintext = get_plaintext(ciphertext, possible_key_lengths)
    return possible_plaintext['pt'], possible_plaintext['key']

def main():
    with open('file.txt') as file:
        ciphertext = base64.b64decode(file.read())
    plaintext, key = repeated_key_xor_break(ciphertext)
    print(plaintext.decode('utf-8'))
    print(key)

if __name__ == '__main__':
    main()