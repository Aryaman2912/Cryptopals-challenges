import base64

def hamming_distance(s, t):
    '''
    Function to find the hamming distance of two strings
    Arguments:
            s: A byte string representing one chunk in the ciphertext
            t: A byte string representing the next chunk in the ciphertext
    Returns:
            hd: Integer representing the hamming distance of the two strings
    '''
    hd = 0
    for a,b in zip(s,t):
        hd += a ^ b

    return hd

def get_key_lengths(ciphertext):
    '''
    Function to find the key length of the ciphertext
    Arguments:
            ciphertext: A byte string representing the ciphertext
    Returns:
            possible_key_lengths: 5 of the most likely key lengths
    '''

    normalized_hamming_distances = {}

    # iterate through all key lengths from 2 to 40
    for key_len in range(2, 40):
        # divide the ciphertext into chunks of length key_len
        substrings = [ciphertext[i:i+key_len] for i in range(0,len(ciphertext),key_len)]
        if len(substrings[-1]) != key_len:
            substrings.pop()

        # find the average hamming distance between each consecutive chunk and normalize it w.r.t the key length
        total_hd = 0
        for x, y in zip(substrings, substrings[1:]):
            total_hd += hamming_distance(x,y)
        
        total_hd /= (len(substrings) - 1)

        normalized_hd = total_hd / key_len

        normalized_hamming_distances[key_len] = normalized_hd

    # sort the normalized hamming distances, and take the first five key_lens
    normalized_hamming_distances = sorted(normalized_hamming_distances,key=normalized_hamming_distances.get)
    possible_key_lengths = normalized_hamming_distances[:min(5,len(normalized_hamming_distances))]

    return possible_key_lengths


def get_score(plaintext):
    '''
    Function to get the score of a plaintext string. Higher the score, more likely it is to be an english string
    Argument:
            plaintext: Byte string
    Returns:
            score: A double representing the score of the string
    '''
    character_frequencies = {
        'a': .08167, 'b': .01492, 'c': .02782, 'd': .04253,
        'e': .12702, 'f': .02228, 'g': .02015, 'h': .06094,
        'i': .06094, 'j': .00153, 'k': .00772, 'l': .04025,
        'm': .02406, 'n': .06749, 'o': .07507, 'p': .01929,
        'q': .00095, 'r': .05987, 's': .06327, 't': .09056,
        'u': .02758, 'v': .00978, 'w': .02360, 'x': .00150,
        'y': .01974, 'z': .00074, ' ': .13000
    }

    # score is the weighted average of the plaintext string. The weights are the character frequencies of alphabets in the english language
    score = sum([character_frequencies.get(chr(byte), 0) for byte in plaintext.lower()]) / len(plaintext) 
    return score

def single_key_xor(ciphertext, key):
    '''
    Function to perform xor of ciphertext and a single character of the key
    Arguments:
            ciphertext: A byte string representing the ciphertext
            key: An integer between 0 and 255 representing a character of the key
    Returns:
            output: A byte string which is the result of the xor between plaintext and key
    '''
    output = b''
    # xor each character with the key and add it to the output
    for byte in ciphertext:
        output += bytes([byte ^ key])
    
    return output

def get_key_byte(ciphertext):
    '''
    Function to obtain one byte of the key
    Argument:
            ciphertext: byte string
    Returns:
            key_byte: dictionary containing plaintext, key and score
    '''
    probable_plaintexts = []
    # iterate through all key values from 0 to 255, find the key with the highest score
    for key in range(256):
        plaintext = single_key_xor(ciphertext,key)
        score = get_score(plaintext)
        scores = {
            'plaintext':plaintext,
            'score': score,
            'key':key
            }
        probable_plaintexts.append(scores)
    key_byte = sorted(probable_plaintexts, key=lambda x: x['score'], reverse=True)[0]
    return key_byte

def repeated_key_xor(ciphertext, key):
    '''
    Function to perform xor of the ciphertext and key
    Arguments:
            ciphertext: byte string
            key: byte string
    Returns:
            output: byte string containing xor of ciphertext and key
    '''
    output = b''
    ind = 0
    #xor each byte in the ciphertext with the corresponding byte in the key. Wrap around the key if needed
    for byte in ciphertext:
        output += bytes([byte ^ key[ind]])
        ind = (ind + 1) % len(key)
    
    return output

def get_plaintext(ciphertext, possible_key_lengths):
    '''
    Function to get the plaintext given the possible key lengths
    Arguments:
            ciphertext: byte string
            possible_key_lengths: list containing 5 possible key_lengths
    Returns:
            plaintext: dictionary containing plaintext, key and score
    '''
    plaintexts = []
    # iterate through possible _key_lengths, obtain chunks of ciphertext based on the key length, find key byte for each chunk
    # once entire key is obtained, obtain the plaintext and find its score
    # among all plaintexts, choose the one with the highest score
    for key_len in possible_key_lengths:
        key = b''
        for i in range(key_len):
            block = b''
            for j in range(i, len(ciphertext), key_len):
                block += bytes([ciphertext[j]])
            key += bytes([get_key_byte(block)['key']])
        pt = repeated_key_xor(ciphertext, key)
        score = get_score(pt)
        d = {
            'pt' : pt,
            'score' : score,
            'key' : key
        }
        plaintexts.append(d)
        
    return sorted(plaintexts, key = lambda x: x['score'], reverse=True)[0]
        
def repeated_key_xor_break(ciphertext):
    '''
    Function to break repeated key xor
    Arguments:
            ciphertext: byte string
    Returns:
            plaintext, key
    '''
    possible_key_lengths = get_key_lengths(ciphertext)
    possible_plaintext = get_plaintext(ciphertext, possible_key_lengths)
    return possible_plaintext['pt'], possible_plaintext['key']

# main function
def main():
    # decode the base64 encode input file
    with open('input_6.txt') as file:
        ciphertext = base64.b64decode(file.read())
    plaintext, key = repeated_key_xor_break(ciphertext)

    # write output to output file
    with open('output_6.txt','w') as output_file:
        output_file.write(plaintext.decode('utf-8'))
        output_file.write(f'Key -> {key}')

if __name__ == '__main__':
    main()