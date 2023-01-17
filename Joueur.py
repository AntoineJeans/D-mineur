class Joueur():
    def __init__(self, tableau, index):
        self.index = index
        self.tableau = tableau
        self.elimine = False
        self.cases = {}
    
    def jouer(self):
        
        if self.tableau.verifier_victoire():
                print("Bravo! Tu as Réussi!")
        elif self.tableau.en_cours:
            self.print_tableau()
            self.executer_action(self.choisir_action())
            self.jouer()
            
            
    def choisir_action(self):
        pass

         
        
    def executer_action(self, choix):
        x,y,action = choix
        if action.lower() == "f":
            self.tableau.cases[(x,y)].flag_case()
        elif action.lower() == "t":
            self.tableau.cases[(x,y)].tourner_case()
        else: print("erreur choix") 
        
class JoueurHumain(Joueur):
    def __init__(self, tableau, index):
        super().__init__(tableau, index)
        
        self.cases_oubliees = []
        self.cases_information = []
        self.cases_a_tourner = []
        self.cases_cachees = self.cases.keys()
        
        
    def choisir_action(self):
        super().choisir_action()
        while True:
            case_x = int(input("Quel case voulez-vous tourner? position en x:"))
            case_y = int(input("Quel case voulez-vous tourner? position en y:"))
            if (case_x,case_y) in self.cases:
                if not self.cases[(case_x,case_y)].tournee:
                    action = input("Tourner un case 't' ou Flagger un case 'f'?")
                    if action.lower() == "t" or action.lower() == "f":
                        return case_x, case_y, action
            else: print("Entrée invalide: (La case donnée n'est pas dans le tableau, ou est déjà tournée)")
                    
       
class JoueurOrdinateur(Joueur):
    def __init__(self, tableau, index):
        super().__init__(tableau, index)
        
    def choisir_action(self):
        super().choisir_action()
        self.classer_cases()
        if not self.tourner_simple():
            if not self.flag_simple():
                self.lancer_simulation()
        
    
    def classer_cases(self):
        """Classe les cases dans leurs sous-groupes respectifs: 
            Groupe 1 - (Tournées ou flag: oubliées | information) : 
             Sous-Groupe 1.1 - oubliées (Toutes cases tournées qui ne touchent aucune case non-tournée, non-flag)
             Sous-Groupe 1.2 - information (Toutes cases tournées qui touchent une case non tournée non flag)
            Groupe 2 - (non-tournées: a_tourner | oubliées):
             Sous-Groupe 2.1 - a_tourner (Toutes cases non-tournees, non-flag, qui touchent une case tournée, à prioriser pour tourner)
             Sous-Groupe 2.2 - cachées (Toutes cases non-tournées, non-flag, qui ne touchent aucune case tournée))
             *Suivant cet ordre, toute case commence au bas, er les cases peuvent seulement se déplacer 
             du bas vers le haut.Tout déplacement bas - > haut est possible directement (ex. cachées - > information, a_tourner -> oubliées)
            """
        
        # L'ordre du classement ne peut pas être changé
        
        obtenir_cases()
        classer_cases_tournees()
        classer_reste()
        
        
        def obtenir_cases(self):
            """Le Joueur obtient la valeur des cases tournées à partir du tableau. 
            Les input du tableau sont ici pour le joueur (Sauf au __init__).
            """
            for case in self.tableau.cases:
                if self.tableau.cases[case].tournee:
                    self.cases[case] = self.tableau.cases[case].valeur
                elif self.tableau.cases[case].flag:
                    self.cases[case] = "F"
                else:
                    self.cases[case] = "X"
                    
                
        def classer_cases_tournees(self):
            "Déplace toutes les cases appropriées Groupe 2 -> Groupe 1. Toutes les cases déplacées se retrouvent dans sous-groupe 1.2"

            for case in self.cases_cachees:
                case_analysee = self.cases[case]
                if self.cases[case_analysee] != "X":
                    self.cases_cachees.pop(case_analysee)
                    self.cases_information.append(case_analysee)
            for case in self.cases_a_tourner:
                case_analysee = self.tableau.cases[case]
                if self.cases[case_analysee] != "X":
                    self.cases_a_tourner.pop(case_analysee)
                    self.cases_information.append(case_analysee)
                    
        def classer_reste(self):
            """Déplace toutes les cases appropriées du sous-groupe 1.2 -> sous-groupe 1.1, et sous-groupe 2.2 -> sous-groupe 2.1
            """
            
            for case in self.case_information:
                case_analysee = self.tableau.cases[case]
                if case_analysee.flag or case_analysee.valeur == 0:
                    self.cases_information.pop(case_analysee)
                    self.cases_oubliees.append(case_analysee)
                    
                else:
                    a_transferer = True
                    operations_tuiles_adjacentes = \
                    [(-1,-1),(-1,0),(0,-1),(0,1),(1,0),(1,1),(1,-1),(-1,1)]
                    
                    for operation in operations_tuiles_adjacentes:
                        x = operation[0] + self.position[0]
                        y = operation[1] + self.position[1]
                        
                        if not self.tableau.cases[(x,y)].tournee and not self.tableau.cases[(x,y)].flag:
                            a_transferer = False
                            
                            if (x,y) in self.cases_cachees:
                                self.cases_cachees.pop((x,y))
                                self.cases_a_tourner.append((x,y))              
                if a_transferer:
                    self.cases_information.pop(case_analysee)
                    self.cases_oubliees.append(case_analysee)
              
    def tourner_simple(self):
        pass
    
    def flag_simple(self):
        pass
    
    def lancer_simulation(self):
        pass
        
   
         
    
    
        