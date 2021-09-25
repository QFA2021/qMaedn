# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 14:07:06 2021

@author: elisa
"""
    
def validation(x,y,a,player): #x Ursprungsfeld, y Zielfeld, a Augenzahl, player Spieler
    """
    Checks wether a move chosen by a player is valid
    Arguments: initial position x, aim position y, diced number a, player choosing the move 
    Procedure
    1)The player throws the dice
    2)The player chooses a piece of his colour at initial position x, which he wants to move
    3)The player chooses the position y he wants to move the selected piece to
    4)Validation checks wether the player's choice of (x,y,a) yields an allowed move
    """
    value1 #Überprüft die korrekte Position des Zielfeldes
    value2 #Überprüft die Besetzungs-Bedingung (max 1 Spielstein je Farbe pro Feld)
    value3 #Überprüft, ob der Spieler eine Figur vom Start auf das Startfeld bewegen darf
    value #Überprüft Korrektheit des gesamten Zuges
    if player == A: #House(A) = {40,41,42,43}
        if x >= 34 && x+a-39 > 0: #Fall, dass A in sein Haus laufen muss
            if y == 40 + (x+a-40): #Prüfen, ob A auf das richtige Feld im Haus gelaufen ist
                value1 = True
            else:
                value1 = False
        else: #Falls A nicht in sein Haus laufen muss
            if x+a <= 39 && y-x == a:
                value1 = True
            elif x+a > 39 && 40-x+y == a: #Fall wird hier gar nicht benötigt -> bleibt der Code richtig, wenn der Fall hier trotzdem aufgeführt wird?
                value1 = True
            else:
                value1 = False                
            
    elif player == B: #House(B) = {44,45,46,47}
        if x >= 4 &&  x+a-9 > 0:
            if y == 44 + (x+a-10):
                value1 = True
            else:
                value1 = False
        else: #Falls B nicht in sein Haus laufen muss
            if x+a <= 39 && y-x == a:
                value1 = True
            elif x+a > 39 && 40-x+y == a:
                value1 = True
            else:
                value1 = False
    elif player == C: #House(B) = {48,49,50,51}
        if x >= 14 &&  x+a-19 > 0:
            if y == 48 + (x+a-20):
                value1 = True
            else:
                value1 = False
        else: #Falls A nicht in sein Haus laufen muss
            if x+a <= 39 && y-x == a:
                value1 = True
            elif x+a > 39 && 40-x+y == a:
                value1 = True
            else:
                value1 = False
    elif player == D: #House(B) = {52,53,54,55}; letzte Möglichkeit player == D durch "else" berücksichtigt?
        if x >= 24 &&  x+a-29 > 0:
            if y == 52 + (x+a-30):
                value1 = True
            else:
                value1 = False
        else: #Falls A nicht in sein Haus laufen muss
            if x+a <= 39 && y-x == a:
                value1 = True
            elif x+a > 39 && 40-x+y == a:
                value1 = True
            else:
                value1 = False
                
    if occupation(y, player) == True: #Überprüfen, ob Zielfeld y vom selben Spieler (player) besetzt ist
        value2 = False
    else:
        value2 = True 

    #if player == A: #Überprüfen, ob ein Spieler einen Stein von Start auf das Startfeld bewegen darf
    #    if 56 <= x <= 59: #Keine Berücksichtigung des "Rausgeh-Zwangs"
    #        if a == 6 && y == 0:
    #            value3 = True
    #        else:
    #            value3 = False            
    #    else:
    #        value3 = True
            
    if player == A: #Überprüfen, ob ein Spieler einen Stein von Start auf das Startfeld bewegen muss. Sonderregel mit Entanglement-Auflösung noch nicht berücksichtigt
        if occupation(56, A) == True or occupation(57, A) == True or occupation(58, A) == True or occupation(59, A) == True:
            if a == 6:
                if 56 <= x <= 59 && y == 0:
                    value3 = True
                else:
                    value3 = False
            else:
                value3 = True
        else:
            value3 = True
     elif player == B:
        if occupation(60, A) == True or occupation(61, A) == True or occupation(62, A) == True or occupation(63, A) == True:
            if a == 6:
                if 60 <= x <= 63 && y == 10:
                    value3 = True
                else:
                    value3 = False
            else:
                value3 = True
        else:
            value3 = True
    elif player == C:
        if occupation(64, A) == True or occupation(65, A) == True or occupation(66, A) == True or occupation(67, A) == True:
            if a == 6:
                if 64 <= x <= 67 && y == 20:
                    value3 = True
                else:
                    value3 = False
            else:
                value3 = True
        else:
            value3 = True
    elif player == C:
        if occupation(68, A) == True or occupation(69, A) == True or occupation(70, A) == True or occupation(71, A) == True:
            if a == 6:
                if 68 <= x <= 71 && y == 30:
                    value3 = True
                else:
                    value3 = False
            else:
                value3 = True
        else:
            value3 = True
            
            
            
        
                       
    
    
    if value1 == True && value2 == True && value3 == True: #Überprüfen, ob beide Bedingungen erfüllt sind -> Zug erlaubt!
        value = True #Zug erlaubt
    else:
        value = False #Zug verboten
    
    return value
    