from random import randint

ROUNDS = 4

s_box = (
	0xE, 0x4, 0xD, 0x1, 
	0x2, 0xF, 0xB, 0x8, 
	0x3, 0xA, 0x6, 0xC, 
	0x5, 0x9, 0x0, 0x7,
)

inv_s_box = (
	0xE, 0x3, 0x4, 0x8,
	0x1, 0xC, 0xA, 0xF,
	0x7, 0xD, 0x9, 0x6,
	0xB, 0x2, 0x0, 0x5,
)

# Note that our P-box is a self-inverse function
p_box = (
	0x0, 0x4, 0x8, 0xC, 
	0x1, 0x5, 0x9, 0xD, 
	0x2, 0x6, 0xA, 0xE, 
	0x3, 0x7, 0xB, 0xF,
)

# Divide input into 4 blocks of 4 bits each; perform S-box substitutions on each block
def substitute(s):
	s_blocks = [(s >> 12) & 0xf, (s >> 8) & 0xf, (s >> 4) & 0xf, s & 0xf]
	s_blocks = [s_box[b] for b in s_blocks]
	return (s_blocks[0] << 12) | (s_blocks[1] << 8) | (s_blocks[2] << 4) | s_blocks[3]

# Divide input into 4 blocks of 4 bits each; perform inverse S-box substitutions on each block
def inv_substitute(s):
	s_blocks = [(s >> 12) & 0xf, (s >> 8) & 0xf, (s >> 4) & 0xf, s & 0xf]
	s_blocks = [inv_s_box[b] for b in s_blocks]
	return (s_blocks[0] << 12) | (s_blocks[1] << 8) | (s_blocks[2] << 4) | s_blocks[3]

# Permute input bit-by-bit according to the P-box
def permute(p):
	p_permuted = 0
	for i in range(16):
		if p & (1 << i):
			p_permuted |= (1 << p_box[i])
	return p_permuted

# Encrypt 16-bit plaintext with five (ROUNDS + 1) 16-bit keys
def encrypt(plaintext, keys):
	assert(len(keys) == ROUNDS + 1)
	data = plaintext

	for i in range(ROUNDS - 1):
		# Key mixing
		data ^= keys[i]
		# Substitution
		data = substitute(data)
		# Permutation
		data = permute(data)
	
	# Perform last round separately (no permutation)
	data ^= keys[ROUNDS - 1]
	data = substitute(data)
	data ^= keys[ROUNDS]

	return data

def decrypt(ciphertext, keys):
	assert(len(keys) == ROUNDS + 1)
	data = ciphertext

	# Decrypt last round separately (no permutation)
	data ^= keys[ROUNDS]
	data = inv_substitute(data)
	data ^= keys[ROUNDS - 1]

	for i in reversed(range(0, ROUNDS - 1)):
		# Undo permutation (permute is a self-inverse function)
		data = permute(data)
		# Undo substitution
		data = inv_substitute(data)
		# Undo key mixing
		data ^= keys[i]

	return data

# Check that encryption/decryption works
pt = randint(1, (1 << 16) - 1)
keys = [randint(1, (1 << 16) - 1) for i in range(ROUNDS + 1)]
ct = encrypt(pt, keys)
assert(pt == decrypt(ct, keys))