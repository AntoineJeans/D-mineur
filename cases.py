class Case():
    def __init__(self, position, tableau):
        self.tableau = tableau
        self.position = position
        self.tournee = False
        self.flag = False
        
    def tourner_case(self):
        """La case est tournée, cette méthode n'affecte pas les cases déjà tournées
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
            cases_adjacentes = self.selectionner_case_adjacentes()
            nombre_flags_adjacents = self.compter_flags_adjacents()
            if nombre_flags_adjacents == self.valeur:
                for case in cases_adjacentes:
                    if not self.tableau.cases[case].flag:
                        self.tableau.cases[case].tourner_case()
                    
    def selectionner_case_adjacentes(self):
        """permet d'obtenir une liste de positions des cases adjacentes (diagonales incluses).

        Returns:
            list: liste de positions sous la forme de tuples (x,y). Selon la position de la case, cette liste aura 3, 5 ou 8 elements.

        """

        operations_tuiles_adjacentes = \
            [(-1,-1),(-1,0),(0,-1),(0,1),(1,0),(1,1),(1,-1),(-1,1)]
        cases_adjacentes = []
        compte_flag = 0
        
        for operation in operations_tuiles_adjacentes:
                x = operation[0] + self.position[0]
                y = operation[1] + self.position[1]
                
                if (x,y) in self.tableau.cases.keys():
                    cases_adjacentes.append((x,y))

        return cases_adjacentes
            
    def compter_bombes_adjacentes(self):
        compte_bombes = 0
        cases_adjacentes = self.selectionner_case_adjacentes()
        for case in cases_adjacentes:
            if case in self.tableau.bombes:
                compte_bombes += 1
        return compte_bombes
        
    
    def compter_flags_adjacents(self):
        compte_flags = 0
        cases_adjacentes = self.selectionner_case_adjacentes()
        for case in cases_adjacentes:
            if self.tableau.cases[case].flag:
                compte_flags += 1
        return compte_flags
    
class CaseVide(Case):
    """Case à tourner, contient une valeur représentant le nombre de case adjacentes à celle-ci contenant une bombe
    """
    def __init__(self, position, tableau):
        super().__init__(position, tableau)
        self.valeur = 0
        
    
    def calculer_valeur(self):
        """Une fois la position des bombes déterminées, la valeur de la case est calculée en vérifiant si les cases qui lui seront adjacentes seront des cases bombes.
        """

        self.valeur = self.compter_bombes_adjacentes()
    
    def tourner_case(self):
        super().tourner_case()
       
        if self.valeur == 0:

            cases_adjacentes = self.selectionner_case_adjacentes()
            
            for case in cases_adjacentes:
                if not self.tableau.cases[case].tournee:
                    self.tableau.cases[case].tourner_case()

class CaseBombe(Case):
    """Case contenant une bombe, si tournée, la partie se termine

    """
    def __init__(self, position, tableau):
        super().__init__(position, tableau)
    def calculer_valeur():
        """Fonction inutile bug fix
        """
        pass
    def tourner_case(self):
        """Termine la partie, échec
        """
        super().tourner_case()
        self.tableau.terminer_partie()