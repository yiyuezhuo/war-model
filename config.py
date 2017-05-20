# -*- coding: utf-8 -*-
"""
Created on Sat May 20 16:08:03 2017

@author: yiyuezhuo
"""

class ArmyConfig(object):
    def __init__(self, path, load_lazy = False):
        self.path = path
        self.header = None
        self.body = None
        self.map = None
        self.type = None
        if not load_lazy:
            self.load()
    def load(self):
        path = self.path
        with open(path,'r',encoding='utf8') as f:
            s = f.read()
        lines = [line.split(',') for line in s.split('\n')]
        if len(lines[-1]) == 1:
            lines.pop() # remove additional null line
        
        header = lines[0]
        body = [[item if i == 0 else float(item) for i,item in enumerate(line)] for line in lines[1:]]
        self.header, self.body = header, body
        
        rd = {}
        for line in body:
            rd[line[0]] = {}
            for key,value in zip(header[1:],line[1:]):
                rd[line[0]][key] = value
        self.map = rd
        
        self.type = list(zip(*self.body))[0]
        
morale_loss_constant = 3
casualty_constant = 0.015