import random
from point import *

'''
Copyright (C) 2016 Carl Londahl <carl.londahl@gmail.com>
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
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
                



