from Crypto.Cipher import AES



def fixSize(str):
	while len(str) %16 != 0:
		str += ' '
	return str


def encrypt(str, key):
	obj = AES.new(key, AES.MODE_ECB)
	message = fixSize(str)
	ciphertext = obj.encrypt(message)
	return ciphertext


def decrypt(str, key):
	obj = AES.new(key, AES.MODE_ECB)
	plaintext = obj.decrypt(str)
	return plaintext


# if __name__ == "__main__":
# 	str = "This is the message that I typed in!"
# 	print str
# 	ciphertext = encrypt(str)
# 	print ciphertext
# 	print decrypt(ciphertext)