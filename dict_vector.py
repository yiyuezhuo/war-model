# -*- coding: utf-8 -*-
"""
Created on Sat May 20 16:58:04 2017

@author: yiyuezhuo
"""

class DictVector(dict):
    def copy(self):
        return self.__class__(dict.copy(self))
    def __iadd__(self, vector):
        for army_type,value in vector.items():
            self[army_type] += value
        return self
    def __add__(self, vector):
        new_vector = self.__class__()
        new_vector += self
        new_vector += vector
        return new_vector
    def __isub__(self, vector):
        for army_type,value in vector.items():
            self[army_type] -= value
        return self
    def __sub__(self, vector):
        new_vector = self.__class__()
        new_vector += self
        new_vector -= vector
        return new_vector
    def sum(self):
        return sum(self.values())
    def __imul__(self, vector):
        for army_type,value in vector.items():
            self[army_type] *= value
        return self
    def __mul__(self, vector):
        new_vector = self.__class__()
        new_vector += self
        new_vector *= vector
        return new_vector
    def __itruediv__(self, vector):
        for army_type,value in vector.items():
            self[army_type] /= value
        return self
    def __truediv__(self, vector):
        new_vector = self.__class__()
        new_vector += self
        new_vector /= vector
        return new_vector
    def __rtruediv__(self, constant):
        new_vector = self.__class__()
        for key,value in new_vector.items():
            new_vector[key] = constant/self[key]
        return new_vector
    def max0(self):
        new_vector = self.__class__()
        for key,value in self.items():
            new_vector[key] = max(0, value)
        return new_vector
    '''
    def __itruediv__(self, vector):
        return self.__idiv__(vector)
    def __truediv__(self, vector):
        return self.__div__(vector)
    '''
        

