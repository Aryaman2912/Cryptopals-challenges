import string
from fixed_xor import xor

letters = string.ascii_lowercase + string.ascii_uppercase + string.digits

def get_IoC(string):

    '''
    This function finds the index of coincidence of a string
    Arguments:
            string: input string xored with a character
    Returns:
            ioc: index of coincidence
    '''
    n = len(string)
    freq_sum = 0.0
    for l in letters:
        freq_sum += (string.count(l)*(string.count(l) - 1))
    ioc = freq_sum / (n*(n-1))

    return ioc

def get_alphanumeric_string(string):
    '''
    This function removes any non-alphanumeric characters in a string
    Argument:  
            string: a string
    Returns:
            alphanumeric string derived from input argument
    '''

    temp = ''
    for l in string:
        if l in letters:
            temp += l

    string = temp

    return string


def get_probable_strings(ciphertext):
    '''
    This function finds all messages that have a good probability of being the result of encryption of the ciphertext
    Argument:
            ciphertext
    Returns:
            messages: a list of possible messages
    '''

    hex_alphabet = '0123456789abcdef'

    # l contains hex values of all characters from #00 to #ff
    l = []
    for i in hex_alphabet:
        for j in hex_alphabet:
            l.append(i+j)

    messages = []
    # xor the ciphertext with each character and check if it can be a valid message
    for c in l:
        res = xor(ciphertext,c*(len(ciphertext)//2))        # xor ct with character
        
        try:
            message = bytearray.fromhex(res).decode()       # convert hex to ascii if possible
            raw_len = len(message)
            message = get_alphanumeric_string(message)      # remove unnecessary characters
            ioc = get_IoC(message)                          # find IoC
            len_message = len(message)
            if len_message/raw_len >= 0.5 and ioc >= 0.03:     # Based on the IoC and number of unnecessary characters, add the message to the list
                messages.append({c,message})

        except:
            pass

    return messages

if __name__ == '__main__':
    ciphertext = input("Enter the ciphertext: ")

    messages = get_probable_strings(ciphertext)

    print("The message can be any of these: ")
    print("--------------------------------------------------------------------------------------------")
    for key,message in messages:
        print(f'Key -> {key}\nMessage->{message}')
        print("--------------------------------------------------------------------------------------------")    
