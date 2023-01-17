from random import *
from cases import CaseVide, CaseBombe

class Tableau():
    def __init__(self):
        self.en_cours = True
        self.dimension_x, self.dimension_y, self.nbr_bombes = self.choisir_mode()
        self.bombes = self.creer_bombes()
        self.cases = self.creer_cases()

    
    def choisir_mode(self):
        while True:
            choix = input("Choisissez un mode ('f' pour facile,'i' pour intermédiaire,'e' pour expert, 'p' pour personnalisé)")
            if choix.lower() == "f":
                return 8,8,10
            if choix.lower() == "i":
                return 16,16,40
            if choix.lower() == "e": 
                return 30,16,99
            if choix.lower() == "p":
                x = int(input("Choisissez une dimension en x: "))
                y = int(input("Choisissez une dimension en y: "))
                bombes = int(input("Choisissez un nombre de bombes: "))
                return x,y,bombes
    
    def creer_bombes(self):
        liste_bombes = []
        while len(liste_bombes) < self.nbr_bombes:
            x = randint(1,self.dimension_x)
            y = randint(1,self.dimension_y)
            if (x,y) not in liste_bombes:
                liste_bombes.append((x,y))
        return liste_bombes
    
    def creer_cases(self):
        cases = {}
        for x in range(1,self.dimension_x+1):
            for y in range(1,self.dimension_y+1):
                if (x,y) in self.bombes:
                    cases[(x,y)] = CaseBombe((x,y), self)
                else:
                    cases[(x,y)] = CaseVide((x,y), self)
        for case in cases:
            if case not in self.bombes:
                cases[case].calculer_valeur()             
        return cases
    
    def jouer(self):
        
        if self.verifier_victoire():
                print("Bravo! Tu as Réussi!")
        elif self.en_cours:
            self.print_tableau()
            self.executer_action(self.choisir_action())
            self.jouer()
            
            
    def choisir_action(self):

        while True:
            case_x = int(input("Quel case voulez-vous tourner? position en x:"))
            case_y = int(input("Quel case voulez-vous tourner? position en y:"))
            if (case_x,case_y) in self.cases:
                if not self.cases[(case_x,case_y)].tournee:
                    action = input("Tourner un case 't' ou Flagger un case 'f'?")
                    if action.lower() == "t" or action.lower() == "f":
                        return case_x, case_y, action
            else: print("Entrée invalide: (La case donnée n'est pas dans le tableau, ou est déjà tournée)")
                    
        
        
    def executer_action(self, choix):
        x,y,action = choix

        if action.lower() == "f":
            self.cases[(x,y)].flag_case()
        elif action.lower() == "t":
            self.cases[(x,y)].tourner_case()
        else: print("erreur choix") 
        
    
    def print_tableau(self):
        
               
        ligne = "   ||"
        for x_adresse in range(1, self.dimension_x+1):
            ligne += "{:^3s}".format(str(x_adresse))
            ligne += "|"
        
        print(ligne)
            
        for y in range(1, self.dimension_y+1):

            ligne = "{:^3s}".format(str(y))
            ligne += "||"
            for x in range(1, self.dimension_x+1):
                if self.cases[(x,y)].flag:
                    ligne += "{:^3s}".format("X")
                elif self.cases[(x,y)].tournee:
                    ligne += "{:^3s}".format(str(self.cases[(x,y)].valeur))
                else:
                    ligne += "{:^3s}".format("-")
                    
                ligne += "|"
            print(ligne)
                
    def print_tableau_triche(self):
        ligne = "   ||"
        for x_adresse in range(1, self.dimension_x+1):
            ligne += "{:^3s}".format(str(x_adresse))
            ligne += "|"
        
        print(ligne)
            
        for y in range(1, self.dimension_y+1):

            ligne = "{:^3s}".format(str(y))
            ligne += "||"
            for x in range(1, self.dimension_x+1):
                if (x,y) in self.bombes:
                    ligne += "{:^3s}".format("X")
                else:
                    ligne += "{:^3s}".format(str(self.cases[(x,y)].valeur))
                    
                ligne += "|"
            print(ligne)
                
    def verifier_victoire(self):
        nbr_cases_non_tournees = 0
        for case in self.cases.values():
            if not case.tournee: 
                nbr_cases_non_tournees += 1
        
        if nbr_cases_non_tournees == len(self.bombes):
            return True
        return False
                           
    def terminer_partie(self):
        print("Échec")
        self.print_tableau_triche()
        self.en_cours = False
        
        
                    
        
        
            
            
            
        
        