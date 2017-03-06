from tables import *

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