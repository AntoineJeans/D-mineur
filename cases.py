class Case():
    def __init__(self, position, tableau):
        self.tableau = tableau
        self.position = position
        self.tournee = False
        self.flag = False
        
    def tourner_case(self):
        self.tournee = True
        
    def flag_case(self):
        self.flag = not self.flag
    
    
class CaseVide(Case):
    def __init__(self, position, tableau):
        super().__init__(position, tableau)
        self.valeur = 0
        
    
    def calculer_valeur(self):
        operations_tuiles_adjacentes = \
        [(-1,-1),(-1,0),(0,-1),(0,1),(1,0),(1,1),(1,-1),(-1,1)]
        compte = 0
        
        for operation in operations_tuiles_adjacentes:
            x = operation[0] + self.position[0]
            y = operation[1] + self.position[1]
            
            if (x,y) in self.tableau.bombes:
                compte += 1
        
        self.valeur = compte
    
    def tourner_case(self):
        super().tourner_case()
       
        if self.valeur == 0:

            operations_tuiles_adjacentes = \
            [(-1,-1),(-1,0),(0,-1),(0,0),(0,1),(1,0),(1,1),(1,-1),(-1,1)]
            for operation in operations_tuiles_adjacentes:
                case_tempo = (operation[0] + self.position[0], operation[1] + self.position[1])
                if case_tempo in self.tableau.cases and not self.tableau.cases[case_tempo].tournee:
                    self.tableau.cases[case_tempo].tourner_case()
            
            

    
    
        
            #
            # if x >= 1 and x < self.tableau.dimension_x:
            #    if y >= 1 and y < self.tableau.dimension_y:
                    
                    
        
    
class CaseBombe(Case):
    def __init__(self, position, tableau):
        super().__init__(position, tableau)
    def tourner_case(self):
        super().tourner_case()
        self.tableau.terminer_partie()