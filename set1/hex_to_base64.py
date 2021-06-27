# The following program converts a given hexadecimal string to a base64 encoded string. This program DOES NOT include padding the strings

def hex_to_decimal(hex_string):
	'''
	This function converts a hexadecimal value to its corresponding decimal value

	Argument:
			hexadecimal value as string
	Returns:
			decimal representation of the hexadecimal string
	'''

	hex_to_int = {'0':0,'1':1,'2':2,'3':3,'4':4,'5':5,'6':6,'7':7,'8':8,'9':9,'a':10,'b':11,'c':12,'d':13,'e':14,'f':15}	# dictionary mapping hex to decimal
	hex_string = hex_string[::-1]	# reverse hex string for convenience
	num = 0
	exp = 0
	for c in hex_string:
		num += (16 ** exp) * hex_to_int[c]
		exp = exp + 1

	return num


def decimal_to_base64(decimal_value):
	'''
	This function converts a given decimal value to base64 encoding. Padding is not included here

	Argument:
			decimal_value: integer to be converted to base64
	Returns:
			base_64: string containing base64 encoded string
	'''
	# The base64 string contains characters from A-Z,a-z,0-9,+ and /

	base_64 = ''

	while decimal_value > 0:
		rem = decimal_value % 64
		decimal_value //= 64
		if rem <= 25:
			base_64 += chr(rem + ord('A'))
		elif rem <= 51:
			base_64 += chr(rem + ord('a') - 26)
		elif rem <= 61:
			base_64 += chr(rem + ord('0') - 52)
		elif rem == 62:
			base_64 += '+'
		else:
			base_64 += '/'

	base_64 = base_64[::-1]

	return base_64

def main():
	
	hex_string = input("Enter the hex string to be converted to base64: ")
	decimal = hex_to_decimal(hex_string)
	base64 = decimal_to_base64(decimal)
	print(f"The base64 representation of the string is: {base64}")
	
if __name__ == '__main__':
	main()
