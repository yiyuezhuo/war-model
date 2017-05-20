# -*- coding: utf-8 -*-
"""
Created on Sat May 20 16:58:04 2017

@author: yiyuezhuo
"""

class DictVector(dict):
    def __iadd__(self, vector):
        for army_type,value in vector.items():
            self[army_type] += value
        return self
    def copy(self):
        return self.__class__(dict.copy(self))
    def __add__(self, vector):
        new_vector = self.__class__()
        new_vector += self
        new_vector += vector
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
