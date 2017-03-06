# Shamir's secret-sharing scheme
This is a simple implementation of Shamir's secret-sharing scheme over GF(2⁸). The secret is split into several shares, rather than transforming the whole secret into larger moduli. This leads to small look-up tables and (basically) constant-time computation.

## Complexity

The complexity of computing shares is O(n²L) where n is the number of shares and L the length of the secret. Finding a secret from m shares (m is threshold) takes O(m²L) time.

## Security

Shamir's secret-sharing scheme offers information-theoretical security. Given m - 1 shares and guessing the last share gives 2⁸ (equally likely) possibilities for the secret (which is a bijective mapping). Hence, the m - 1 reveal nothing about the secret. Since the L different shares are independent, no information about the secret as a whole is revealed.