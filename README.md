# Linear-Cryptanalysis
Implementations and linear cryptanalysis of a substitution-permutation network, based off [this paper](http://www.cs.bc.edu/~straubin/crypto2017/heys.pdf) by Howard M. Heys.

Read my blog post [here](https://kevinl10.github.io/posts/Linear-Cryptanalysis-Pt-1/) for a more detailed explanation of the attack.

# Usage
`python3 attack.py` generates a random key, along with a specified number of plaintext/ciphertext samples. To see the biases for all possible key bit pairs, set the `DEBUG` option to `True`.

# Todo

Examine the relationships between:
- The number of samples and the accuracy of the attack
- The magnitude of the bias and the number of samples needed for consistent accuracy