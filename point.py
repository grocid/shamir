from tables import *

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

class Point:

    def __init__(self, value):
        self.value = value % 256

    def __add__(self, point):
        return Point(self.value ^ point.value)

    def __iadd__(self, point):
        self.value ^= point.value
        return self

    def __mul__(self, point):
        if point.value == 0 or self.value == 0:
            return Point(0)
        return Point(expTable[(logTable[self.value] + logTable[point.value]) % 255])

    def __imul__(self, point):
        if point.value == 0 or self.value == 0:
            self.value = 0
        else:
            self.value = expTable[(logTable[self.value] + logTable[point.value]) % 255]
        return self

    def __div__(self, point):
        if point.value == 0:
            raise ArithmeticError('Division by zero')
        return Point(expTable[(255 + logTable[self.value] - logTable[point.value]) % 255])

    def __idiv__(self, point):
        if point.value == 0:
            raise ArithmeticError('Division by zero')
        self.value = expTable[(255 + logTable[self.value] - logTable[point.value]) % 255]
        return self
