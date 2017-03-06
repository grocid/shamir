# Shamir's secret-sharing scheme
This is a simple implementation of Shamir's secret-sharing scheme over GF(2⁸). The secret is split into several shares, rather than transforming the whole secret into larger moduli. This leads to small look-up tables and (basically) constant-time computation.

## Complexity

The complexity of computing shares is O(n²L) where n is the number of shares and L the length of the secret. Finding a secret from m shares (m is threshold) takes O(m²L) time.