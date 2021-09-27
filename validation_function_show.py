# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 17:49:20 2021

@author: elisa
"""

#O = occupied(x,player)
import numpy as np

def start_field(player): #return the start field for a given player
    sf = []
    for player in range(4):
        field = player * 10
        sf = np.append(sf, field)
    return sf

def start_positions(player): #return all start positions for a given player
    s = []
    i = 0
    for i in range(4):
        sp = 56 + player*4 + i
        s = np.append(s, sp)
        i = i+1
    return s

def house_field(player):
    hf = (39 + player*10) % 40
    return hf

def house(player):
    h = []
    i = 0
    for i in range(4):
        hp = 40 + player*4 + i
        h = np.append(h, hp)
        i = i+1
    return h

def occupied_fields(player):
    i = 0
    o = []
    for i in range(72):
        if occupied(i, player) == True:
            o = np.append(o, i)
        else:
            o = o
        i = i+1
    return o

def forbidden_fields(player, a): #Returns all fields, on which a player can't move with a selected piece, since it would land on a field occupied by himself 
    y = []
    o = occupied_fields(player)
    hf = house_field(player)
    h = house(player)
    i = 0
    for i in range(72):
        if i in o == True:
            if i <= hf && i+a <= hf: #Fall, dass player nicht ins Haus kommt
                if i+a in o == True:
                    y = np.append(y, i)
                else:
            elif i<= hf && i+a > hf: #Fall, dass player ins Haus kommt
                d = i+a-hf
                m = np.min(h)
                if m+d-1 in o == True:
                    y = np.append(y, i)
                else:
            else: #(39>=)i>hf, d.h. Fall, dass i im Bereich zwischen Startfeld und Feld 39 ist
                if i+a <= 39:
                    if i+a in o == True:
                        y = np.append(y, i)
                    else:
                elif: #i+a>39
                    if i+a-40 in o == True:
                        y = np.append(y, i)
                    else:    
        else:
        i = i+1
    return y
            
        
        

def validation_show(player, a):
     """
    Shows the player all valid moves for all his pieces, given the diced number
    Arguments: diced number a, player choosing the move 
    Return: List of allowed x_i
    Procedure
    1)The player throws the dice
    2)Validation_show shows the player all his pieces at positions x, which he is allowed to move to y = x+a
    """
    sf = start_field(player)
    s = start_positions(player)
    hf = home_field(player)
    o = occupied_fields(player)
    y = forbidden_fields(player, a)
    x = [] #List of pieces at positions x allowed to move
    
    owy = [i for i in o == True && i in y == False] #o without y - funktioniert das???
    
    if a == 6:
        if ET == True: #ET liefert, ob player ein entangletes Paar Steine hat oder nicht
            if occupied(sf, player) == True:
                if occupied(s, player) == True:
                    x = np.append(x, sf)
                else:
                    x = np.append(x, owy)
    else:
        