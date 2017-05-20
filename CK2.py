# -*- coding: utf-8 -*-
"""
Created on Sat May 20 15:34:41 2017

@author: yiyuezhuo
"""

from config import ArmyConfig,morale_loss_constant, casualty_constant
import config
from dict_vector import DictVector


army_config = ArmyConfig('army.csv') # it is seen as global variable in this module


class ArmyTypeVector(DictVector):
    def __init__(self, values = None):
        if values is None:
            values = [0 for i in range(len(army_config.type))]
        elif isinstance(values, (int, float)):
            values = [values for i in range(len(army_config.type))]
        if isinstance(values, (list, tuple)):
            values = dict(zip(army_config.type, values))
        assert isinstance(values, dict) # but strength may be not suffice
        
        for typ in army_config.type:
            self[typ] = values.get(typ,0)
        
army_config.vector = {}
for h,v in zip(army_config.header[1:], list(zip(*army_config.body))[1:]):
    army_config.vector[h] = ArmyTypeVector(v)

class Army(object):
    def __init__(self, strength=None, technology_modify = None,
                 building_modify = None, tactic_unit_modify = None,
                 leader_modify = None, tactic_tactic_modify = None,
                 defense_modify = None,
                 time = 1):
        '''
        strength: ArmyTypeVector: Every item take 500~1000 value
        technology_modify: ArmyTypeVector: Every item take 0.0~5.0(500%) value
        building_modify: ArmyTypeVector 
        tactic_unit_modify: ArmyTypeVector
        leader_modify: ArmyTypeVector
        tactic_tactic_modify: ArmyTypeVector
        defense_modify: ArmyTypeVector
        time: time multiplier
        '''
        self.init_strength = ArmyTypeVector(strength)
        self.last_strength = self.init_strength.copy()
        
        self.technology_modify    = ArmyTypeVector() if technology_modify    is None else technology_modify
        self.building_modify      = ArmyTypeVector() if building_modify      is None else building_modify
        self.tactic_unit_modify   = ArmyTypeVector() if tactic_unit_modify   is None else tactic_unit_modify
        self.leader_modify        = ArmyTypeVector() if leader_modify        is None else leader_modify
        self.tactic_tactic_modify = ArmyTypeVector() if tactic_tactic_modify is None else tactic_tactic_modify
        self.defense_modify       = ArmyTypeVector() if defense_modify       is None else defense_modify
        # Although leader_modify and tactic_tactic_modify are not unit-elementwise but army-wise modify.
        
        self.time = time
    '''
    def add_strength(self, strength):
        for army_type,value in strength.items():
            self.last_strength[army_type] += value
    '''
    @property
    def loss_strength(self):
        '''
        rd = {}
        for army_type, value in self.init_strength.items():
            rd[army_type] = value - self.last_strength[army_type]
        return rd
        '''
        return self.init_strength - self.last_strength
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
        morale_loss = self.loss_strength.sum() * morale_loss_constant
        last_morale = self.last_morale()
        return (last_morale - morale_loss) / last_morale
    #def _dot2(self, dot_key):
    #    return sum([army_config.map[army_type][dot_key] * value for army_type,value in self.last_strength.items()])
    def _dot(self, dot_key, detail = False):
        base = army_config.vector[dot_key]
        # ugly old MatLab style hack
        one = ArmyTypeVector(1)
        time = ArmyTypeVector(self.time)
        constant = ArmyTypeVector(casualty_constant)
        
        strength = self.last_strength
        tech = self.technology_modify
        building = self.building_modify
        tactic_unit = self.tactic_unit_modify
        leader = self.leader_modify
        tactic_tactic = self.tactic_tactic_modify
        
        point = base * (one + tech + building + tactic_unit) * \
                       (one + leader + tactic_tactic) * \
                        strength * time * constant
        if detail:
            return point
        return point.sum()
    def melee_attack(self, detail = False):
        return self._dot('Melee Attack', detail = detail)
    def skirmish_attack(self, detail = False):
        return self._dot('Skirmish Attack', detail = detail)
    def pursue_attack(self, detail = False):
        return self._dot('Pursue Attack', detail = detail)
    def melee_defense(self, detail = False):
        return self._dot('Melee Defense', detail = detail)
    def skirmish_defense(self, detail = False):
        return self._dot('Skirmish Defense', detail = detail)
    def pursue_defense(self, detail = False):
        return self._dot('Pursue Defense', detail = detail)
    def loss_weight(self):
        dic = {}
        s = self.last_strength.sum()
        for typ,value in self.last_strength.items():
            dic[typ] = value/s if value > 0 else 0
        return ArmyTypeVector(dic)
    def _loss(self, point, dot_key):
        weight = self.loss_weight()
        
        #one = ArmyTypeVector(1)
        point = ArmyTypeVector(point)
        unit = army_config.vector[dot_key]
        leader = self.leader_modify
        defense = self.defense_modify
        #print(weight)
        #print(point * weight / (unit + leader + defense))
        #print(self.last_strength - point * weight / (unit + leader + defense))
        self.last_strength = (self.last_strength - point * weight / (unit + leader + defense)).max0()

    def melee_loss(self, point):
        self._loss(point, 'Melee Defense')
    def skirmish_loss(self, point):
        self._loss(point, 'Skirmish Defense')
    def pursue_loss(self, point):
        self._loss(point, 'Pursue Defense')
            
    
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
army.last_strength -= {'Light Infantry':300}
print(army.morale())
print(army.melee_attack())
army2 = Army({'Light Infantry':500,'Heavy Infantry':300})
army2.melee_loss(100)
print(army2.last_strength)

army3 = Army({'Heavy Cavalry': 100})
army4 = Army({'Light Infantry': 1000})
atk3 = army3.melee_attack()
atk4 = army4.melee_attack()
army3.melee_loss(atk4)
army4.melee_loss(atk3)
print(army3.last_strength, army3.morale())
print(army4.last_strength, army4.morale())

#army3 = Army({'Archers': 500, 'Pikemen': 500})
# This example come from http://bbs.3dmgame.com/thread-3812763-1-1.html
army3 = Army({'Archers': 500, 'Pikemen': 500})
army4 = Army({'Heavy Cavalry': 600, 'Light Cavalry': 400})
army3.building_modify = ArmyTypeVector(0.6)
army3.tactic_unit_modify = ArmyTypeVector(4.2)
army3.leader_modify = ArmyTypeVector(0.32)
army3.tactic_tactic_modify = ArmyTypeVector(1)
army4.leader_modify = ArmyTypeVector(0.32)
for i in range(10):
    army4.skirmish_loss(army3.skirmish_attack())
#print(army3.last_strength, army3.morale())
print(army4.last_strength, army4.morale())

