from random import *
from cases import CaseVide, CaseBombe

class Tableau():
    """Classe du tableau, L'objet contient toute l'information de la partie Minesweeper en cours, 
    et toutes les méthodes concernant la mise en place des paramètres du jeu
    """
    def __init__(self):
        self.en_cours = True
        self.dimension_x, self.dimension_y, self.nbr_bombes = self.choisir_mode()
        self.bombes = self.creer_bombes()
        self.cases = self.creer_cases()

    
    def choisir_mode(self):
        """Les paramètres du jeu sont déterminées ici par la console et retournés. Les modes de jeu par défaut sont aussi inclus.

        Returns:
            (int,int,int): x: La largeur du tableau 
                           y: La hauteur du tableau
                           bombes: quantité de bombes dans la partie
        """
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
        """Une liste de position (une pour chaque bombe), est crée. Les positions sont nécéssairement contenues dans les cases possibles
        ** L'algorithme risque d'être plus lent avec un ratio (nombre bombres / nombre cases) près de 1.
        Returns:
            list: liste de position utilisée plus tard pour créer les bombes
        """
        liste_bombes = []
        while len(liste_bombes) < self.nbr_bombes:
            x = randint(1,self.dimension_x)
            y = randint(1,self.dimension_y)
            if (x,y) not in liste_bombes:
                liste_bombes.append((x,y))
        return liste_bombes
    
    def creer_cases(self):
        """L'inventaire des cases est créé, par un dictionnaire, self.cases. 
        Un objet est initié pour chaque position, (CaseBombe si position est dans la liste_bombes créée auparavant, CaseVide sinon)
        L'objet est ensuite ajouté au dictionnaire par la clé (x,y) représentant sa position. 

        Returns:
            dict: Le dictionnaire contenant toutes les cases du tableau 
        """
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
    
    #def jouer(self):
    #    
    #    if self.verifier_victoire():
    #            print("Bravo! Tu as Réussi!")
    #    elif self.en_cours:
    #        self.print_tableau()
    #        self.executer_action(self.choisir_action())
    #        self.jouer()
    #        
    #        
    #def choisir_action(self):
#
    #    while True:
    #        case_x = int(input("Quel case voulez-vous tourner? position en x:"))
    #        case_y = int(input("Quel case voulez-vous tourner? position en y:"))
    #        if (case_x,case_y) in self.cases:
    #            if not self.cases[(case_x,case_y)].tournee:
    #                action = input("Tourner un case 't' ou Flagger un case 'f'?")
    #                if action.lower() == "t" or action.lower() == "f":
    #                    return case_x, case_y, action
    #        else: print("Entrée invalide: (La case donnée n'est pas dans le tableau, ou est déjà tournée)")
    #                
    #    
    #    
    #def executer_action(self, choix):
    #    x,y,action = choix
#
    #    if action.lower() == "f":
    #        self.cases[(x,y)].flag_case()
    #    elif action.lower() == "t":
    #        self.cases[(x,y)].tourner_case()
    #    else: print("erreur choix") 
    
    # Vestiges de l'ancien système, tester avant de supprimer
    
    
          
    def executer_action(self, choix):
        """Le choix passé en argument est exécuté sur les cases du tableau

        Args:
            choix (int, int, str): 3 objets en une variable:
                                   x: position en x de la case à modifier
                                   y: position en y de la case à modifier
                                   action: tourner, flagger ou chorder (https://en.wikipedia.org/wiki/Chording)
        """

        x,y,action = choix
        if action.lower() == "f":
            self.cases[(x,y)].flag_case()
        elif action.lower() == "t":
            self.cases[(x,y)].tourner_case()
        elif action.lower() == "c":
            self.cases[(x,y)].chord_case()
        else: print("erreur choix") 
        
            
    def executer_premier_tour(self, choix, rayon=0):
        """Généralement, au démineur, une bombe ne peut pas être trouvée au premier tour. Le premier tour doit donc être différent, sans affecter le hasard des bombes.
        Si le premier choix touche une bombe, la bombe est déplacée à une case aléatoire, et les cases adjacentes sont recalculées.
        Le rayon représente le nombre de cases à "vider". Un rayon de 0 s'assure que seulement la case touchée ne contient pas de bombe, un rayon de 1 s'assure que le carré
        3x3 autour de la case touchée ne contient pas de bombe (autrement dit, la première case touchée est un 0). Plus le rayon est haut, plus le départ est facile.


        Args:
            choix (tuple): voir executer_action
            rayon (int): Le nombre de couches autour de la case touchée à vider.
            """
            
        x,y,action = choix
        # S'il y a une bombe, on la déplace de façon aléatoire
        cases_a_vider = self.cases[(x,y)].selectionner_cases_adjacentes(rayon)
        case_a_modifier = []
        
        for case in case_a_vider:
            
            if case in self.bombes:
                self.bombes.pop(case)
                del self.cases[case]
                self.cases[case] = CaseVide(case, self)

                while len(self.bombes) < self.nbr_bombes:
                    x_bombe = randint(1,self.dimension_x)
                    y_bombe = randint(1,self.dimension_y)
                    if (x_bombe,y_bombe) not in self.bombes:
                        if (x_bombe,y_bombe) not in cases_a_vider: 
                        self.bombes.append((x_bombe, y_bombe))
                        del self.cases[(x_bombe,y_bombe)]
                        self.cases[(x_bombe,y_bombe)] = CaseBombe((x_bombe,y_bombe), self)

                        case_a_modifier += self.cases[x_bombe,y_bombe].selectionner_cases_adjacentes()
        
        for case in case_a_modifier:
            self.cases[case].calculer_valeur()
        # Ne pas oublier cette parti
        self.executer_action(choix)


    
    def print_tableau(self, tour):
        
        """Fonction qui imprime le tableau dans la console (éventuellement remplacé par une interface potentiellement)
        """
        print("Vous avez fait", tour, "actions.")
               
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
        """Fonction qui imprime le tableau dans la console, mais avec toutes les valeurs des cases 
        """
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
        """Vérifie si toutes les cases vides sont tournées. Dans ce cas, la partie est gagnée.

        Returns:
            bool: True si toutes les cases vides sont tournées, False sinon.
        """
        if self.en_cours:
            nbr_cases_non_tournees = 0
            for case in self.cases.values():
                if not case.tournee: 
                    nbr_cases_non_tournees += 1

            if nbr_cases_non_tournees == len(self.bombes):
                self.terminer_partie(True)
            return False
        else: self.terminer_partie(False) 
                           
    def terminer_partie(self, reussite):
        """Fonction appelée en cas de réussite ou d'échec. Elle annonce le résultat et change le statut de la partie.

        Args:
            reussite (bool): True si réussite, False si échec
        """
        if reussite:
            print("Bravo! Vous avez trouvé toutes les mines!")
        else:
            print("Échec :(")
            self.print_tableau_triche()
        self.en_cours = False
        
        
                    
        
        
            
            
            
        
        