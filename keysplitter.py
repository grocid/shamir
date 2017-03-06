import json, base64, os
from shamir import *

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

class KeySplitter:
    
    def __init__(self):
        self.splitter = Shamir()

    def split(self, numshares, threshold, key):
        xshares = [''] * numshares
        yshares = [''] * numshares
        
        # For each symbol in the key split into shares over GF(2^8)
        for char in key:
            xcords, ycords = self.splitter.split(numshares, threshold, ord(char))
            
            for idx in range(numshares):
                xshares[idx] += chr(xcords[idx])
                yshares[idx] += chr(ycords[idx])
        
        return zip(xshares, yshares)
    
    def unsplit(self, shares):
        recovered = ''
        
        # For each sub share (corresponding to symbol in key)...
        for idx in range(len(shares[0][0])):
            xcords = []
            ycords = []
            
            # Compute the secret value
            for xcord, ycord in shares:
                xcords += [ord(xcord[idx])]
                ycords += [ord(ycord[idx])]

            recovered += chr(self.splitter.unsplit(xcords, ycords, 0))
            
        return recovered
    
    def jsonify(self, shares, threshold, split):
        data = {
            'shares': shares, 
            'threshold': threshold, 
            'split': [
                base64.b64encode(split[0]),
                base64.b64encode(split[1])
            ]
        }
        
        return json.dumps(data)

if __name__ == "__main__":
    shares = 30
    threshold = 20
    
    print 'Running (30, 20) with 100 independent keys...'
    
    for i in range(100):
        secret_key = os.urandom(64)
    
        splitter = KeySplitter()
        splits = splitter.split(shares, threshold, secret_key)
        
        assert(splitter.unsplit(splits) == secret_key)