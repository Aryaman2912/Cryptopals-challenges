# The following program returns the xor values of two equal length xor strings

def xor(s1,s2):
    '''
    This function performs xor of two equal length hex strings
    
    Arguments:
            s1: hex string 1
            s2: hex string 2
    
    Returns:
            hex string equal to xor of the two input strings
    '''

    hex_to_int = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}	# dictionary mapping hex to decimal
    int_to_hex = {0:'0',1:'1',2:'2',3:'3',4:'4',5:'5',6:'6',7:'7',8:'8',9:'9',10:'a',11:'b',12:'c',13:'d',14:'e',15:'f'}    # dictionary mapping decimal to hex
    xor_string = ''.join([int_to_hex[(hex_to_int[x] ^ hex_to_int[y])] for x,y in zip(s1,s2)])
    
    return xor_string

if __name__ == '__main__':
    # input two strings of equal length
    s1 = input("Enter the first hexadecimal string: ")
    s2 = input("Enter the second hexadecimal string: ")

    xor_string = xor(s1,s2)

    print(f'The xor of the two input hex strings is {xor_string}')