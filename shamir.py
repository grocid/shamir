import random
from point import *

'''
Copyright 2018 Carl Londahl <carl.londahl@gmail.com>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
this list of conditions and the following disclaimer in the documentation
and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its contributors
may be used to endorse or promote products derived from this software without
specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''

class Shamir:

    def unsplit(self, xcords, ycords, evaluation):
        P = Point(1)
        S = Point(0)
        Z = Point(evaluation)
        # Pre-compute nominator
        for xcord in xcords:
            P *= Z + Point(xcord)
        # Perform Lagrange interpolation over GF(2^8)
        for xcord, ycord in zip(xcords, ycords):
            Q = P / (Z + Point(xcord))
            Px = Point(xcord)
            Py = Point(ycord)
            # ...and evalaute it in x = 0
            for denom in xcords:
                if xcord != denom:
                    Q /= (Px + Point(denom))
            S += Py * Q
        return S.value

    def split(self, shares, threshold, secret):
        rng = random.SystemRandom()
        # Define polynomial to be P(0) = secret
        coeffs = [secret] + [rng.randint(0, 256) for _ in range(threshold - 1)]
        coords = []
        result = []
        # Find a set with unique shares
        while len(coords) < shares:
            drawn = rng.randint(1, 255)
            if not drawn in coords:
                coords += [drawn]
        # Evaluate polynomial in all coords
        for coord in coords:
            B = Point(1)
            S = Point(0)
            X = Point(coord)
            for coeff in coeffs:
                S += (B * Point(coeff))
                B *= X
            result.append(S.value)
        return coords, result
