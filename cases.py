class Case():
    def __init__(self, position, tableau):
        self.tableau = tableau
        self.position = position
        self.tournee = False
        self.flag = False
        
    def tourner_case(self):
        """La case est tournée
        """
        self.tournee = True
        
    def flag_case(self):
        """La case est flaggée
        """
        self.flag = not self.flag
    
    def chord_case(self):
        """Si la case est tournée, on vérifie si la valeur de cette case est égale au nombre de case adjacentes à celle-ci qui sont flag. 
        Si c'est le cas, toutes les cases adjacentes non-flag sont tournées, même s'il y a une bombe. (Si les conditions ne sont pas remplies, rien se passe)
        """
        if self.tournee:
            operations_tuiles_adjacentes = \
            [(-1,-1),(-1,0),(0,-1),(0,1),(1,0),(1,1),(1,-1),(-1,1)]
            compte = 0

            for operation in operations_tuiles_adjacentes:
                x = operation[0] + self.position[0]
                y = operation[1] + self.position[1]

                if self.tableau.cases[(x,y)].flag:
                    compte += 1

            if compte == self.valeur:
                for operation in operations_tuiles_adjacentes:
                    x = operation[0] + self.position[0]
                    y = operation[1] + self.position[1]
                if not self.tableau.cases[(x,y)].flag:
                    self.tableau.cases[(x,y)].tourner_case()

        
    
    
class CaseVide(Case):
    """Case à tourner, contient une valeur représentant le nombre de case adjacentes à celle-ci contenant une bombe
    """
    def __init__(self, position, tableau):
        super().__init__(position, tableau)
        self.valeur = 0
        
    
    def calculer_valeur(self):
        """Une fois la position des bombes déterminées, la valeur de la case est calculée en vérifiant si les cases qui lui seront adjacentes seront des cases bombes.
        """
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

    
class CaseBombe(Case):
    """Case contenant une bombe, si tournée, la partie se termine

    """
    def __init__(self, position, tableau):
        super().__init__(position, tableau)
    def tourner_case(self):
        """Termine la partie, échec
        """
        super().tourner_case()
        self.tableau.terminer_partie()