from cipher import *
from math import fabs
from random import randint
import numpy as np
import sys, timeit

def getBit(num, idx):
	return (num >> idx) & 0x1

start_time = timeit.default_timer()
SAMPLES = 10 ** 4

# Set DEBUG to True to see all biases for different keys
DEBUG = False

# Generate random keys
keys = [randint(1, (1 << 16) - 1) for i in range(ROUNDS + 1)]
plaintexts, ciphertexts = [], []

# Collect plaintext/ciphertext samples
for i in range(SAMPLES):
	n = randint(1, (1 << 16) - 1)
	plaintexts.append(n)
	ciphertexts.append(encrypt(n, keys))

print("Keys:", [hex(key) for key in keys])

biases = np.zeros((16, 16))
best_keys = (0,)

for i in range(256):
	sys.stdout.write(f"[x] Progress: {i}/256\r")

	k2 = (i >> 4) & 0xF
	k4 = i & 0xF
	cnt = 0

	for a in range(SAMPLES):
		pt = plaintexts[a]
		ct = ciphertexts[a]

		# Calculate the bits before the last S-box
		V = [((ct >> 8) & 0xF) ^ k2, ((ct >> 0) & 0xF) ^ k4]
		U = [inv_s_box[nib] for nib in V]

		val = getBit(U[0], 0) ^ getBit(U[0], 2) ^ getBit(U[1], 0) ^ getBit(U[1], 2)
		val ^= getBit(pt, 8) ^ getBit(pt, 9) ^ getBit(pt, 11)

		# If the linear approximation holds, then increment the counter
		if val == 0:
			cnt += 1

	# Keep track of the (k2, k4) pair that has the greatest bias
	bias = fabs(cnt/SAMPLES - 0.5)
	if bias > best_keys[0]:
		best_keys = (bias, k2, k4)
	biases[k2][k4] = bias

print(f"[+] Expected: {hex((keys[-1] >> 8) & 0xF)} and {hex(keys[-1] & 0xF)}")
print(f"[+] Found: {hex(best_keys[1])} and {hex(best_keys[2])}")
print(f"[+] Time taken: {timeit.default_timer() - start_time}")

# Display biases for all the possible (two-bit) keys
if DEBUG:
	np.set_printoptions(edgeitems=10,linewidth=180)
	print(biases)