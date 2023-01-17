class Joueur():
    def __init__(self, tableau, index):
        self.index = index
        self.tableau = tableau
        self.elimine = False
    
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
            self.cases[(x,y)].flag_case()
        elif action.lower() == "t":
            self.cases[(x,y)].tourner_case()
        else: print("erreur choix") 
        
class JoueurHumain(Joueur):
    def __init__(self, tableau, index):
        super().__init__(tableau, index)
        
        self.cases_oubliees = []
        self.cases_information = []
        self.cases_a_tourner = []
        self.cases_cachees = self.tableau.cases.keys()
        
        
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
        self.refresh_cases()
        if not self.tourner_simple():
            if not self.flag_simple():
                self.lancer_simulation()
        
    
    def refresh_cases(self):
        
        #L'ordre du classement ne peut pas être changé
        
        classer_cases_tournees()
        classer_reste()
                
        def classer_cases_tournees(self):
            
            for case in self.cases_cachees:
                case_analysee = self.tableau.cases[case]
                if case_analysee.tournee or case_analysee.flag:
                    self.cases_cachees.pop(case_analysee)
                    self.cases_information.append(case_analysee)
            for case in self.cases_a_tourner:
                case_analysee = self.tableau.cases[case]
                if case_analysee.tournee or case_analysee.flag:
                    self.cases_a_tourner.pop(case_analysee)
                    self.cases_information.append(case_analysee)
                    
        def classer_reste(self):
            
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
        
   
         
    
    
        