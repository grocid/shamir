import json, base64, os
from shamir import *

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
    print ('Running test instances (30, 20) with 100 independent keys...')
    for i in range(100):
        secret_key = os.urandom(64)
        splitter = KeySplitter()
        splits = splitter.split(shares, threshold, secret_key)
        assert(splitter.unsplit(splits) == secret_key)