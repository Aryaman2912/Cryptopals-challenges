from single_byte_xor_cipher import get_probable_strings

file = open("file.txt","r")

for line in file:
    messages = get_probable_strings((line.strip()))
    op = open(f"ops/{line.strip()}.txt","w")
    for message,key in messages:
        print(line.strip(),key)
        op.write(f"key -> {message}\nMessage -> {key}\n")