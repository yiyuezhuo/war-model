# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:34:41 2017

@author: yiyuezhuo
"""

from config import ArmyConfig, morale_loss_constant, casualty_constant
from dict_vector import DictVector

army_config = ArmyConfig('army.csv') # it is seen as global variable in this module


class ArmyTypeVector(DictVector):
    def __init__(self, values = None, constant = None):
        if values is None and constant is None:
            values = [0 for i in range(len(army_config.type))]
        elif values is None and constant is not None:
            values = [constant for i in range(len(army_config.type))]
        if isinstance(values, list):
            values = dict(zip(army_config.type, values))
        assert isinstance(values, dict) # but strength may be not suffice
        
        for typ in army_config.type:
            self[typ] = values.get(typ,0)
        

class Army(object):
    def __init__(self, strength=None):
        '''
        if strength is None:
            strength = [0 for i in range(len(army_config.type))]
        if isinstance(strength, list):
            strength = dict(zip(army_config.type, strength))
        assert isinstance(strength, dict) # but strength may be not suffice
        '''
        self.init_strength = ArmyTypeVector(strength)
        self.last_strength = self.init_strength.copy()
    def add_strength(self, strength):
        for army_type,value in strength.items():
            self.last_strength[army_type] += value
    @property
    def loss_strength(self):
        rd = {}
        for army_type, value in self.init_strength.items():
            rd[army_type] = value - self.last_strength[army_type]
        return rd
    def _morale(self, strength):
        morale = 0
        for army_type,value in strength.items():
            morale += army_config.map[army_type]['Morale'] * value
        return morale
    def init_morale(self):
        return self._morale(self.init_strength)
    def last_morale(self):
        return self._morale(self.last_strength)
    def morale(self):
        morale_loss = sum(self.loss_strength.values()) * morale_loss_constant
        last_morale = self.last_morale()
        return (last_morale - morale_loss) / last_morale
    def _dot(self, dot_key):
        return sum([army_config.map[army_type][dot_key] * value for army_type,value in self.last_strength.items()])
    def melee_attack(self):
        return self._dot('Melee Attack')
    def skirmish_attack(self):
        return self._dot('Skirmish Attack')
    def pursue_attack(self):
        return self._dot('Pursue Attack')
    def melee_defense(self):
        return self._dot('Melee Defense')
    def skirmish_defense(self):
        return self._dot('Skirmish Defense')
    def pursue_defense(self):
        return self._dot('Pursue Defense')
            
    
class CK2Army(Army):
    def __init__(self):
        pass

class CombatSolver(object):
    def __init__(self, army_config):
        self.army_config = army_config
        
army = Army({'Light Infantry':500,'Heavy Infantry':300})
print(army.morale())
print(army.melee_attack())
print(ArmyTypeVector({'Archers':500}) + ArmyTypeVector({'Archers':600}))