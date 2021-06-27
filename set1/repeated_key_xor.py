from fixed_xor import xor
m1 = "Burning 'em, if you ain't quick and nimble\nI go crazy when I hear a cymbal"
m2 = "I go crazy when I hear a cymbal"

key = "ICE"


# bytearray.
hex_key = key.encode('utf-8').hex()
hex_m1 = m1.encode('utf-8').hex()
hex_m2 = m2.encode('utf-8').hex()
k1 = hex_key * (len(hex_m1) // len(hex_key)) + hex_key[:len(hex_m1) % len(hex_key)]
k2 = hex_key * (len(hex_m2) // len(hex_key)) + hex_key[:len(hex_m2) % len(hex_key)]
print(xor(hex_m1,k1))
print(xor(hex_m2,k2))
