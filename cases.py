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
        Il est possible d'obtenir un output si le chord était utile (surtout pour l'ordinateur)
        """
        case_tournee = False
        if self.tournee:
            cases_adjacentes = self.selectionner_case_adjacentes()
            nombre_flags_adjacents = self.compter_flags_adjacents()
            if nombre_flags_adjacents == self.valeur:
                for case in cases_adjacentes:
                    if not self.tableau.cases[case].flag:
                        self.tableau.cases[case].tourner_case()
                        case_tournee = True
        return case_tournee
                        
    
    def obtenir_combinaison(liste_valeurs, longueur,liste):

        """
        (fonction que j'ai fait il y a longtemps) Prépare une liste dont tous les élément représentent une combinaison de 
        valeurs d'une longueur déterminée. Attaque le problème couche par couche, recursivement. 

        Args:
            listes_valeurs (list): Listes des valeurs possibles dans les éléments de la liste retournée
            hauteur_actuelle (int): Permet de se situer dans la fonction recursive (doit être posée à 0 à l'appel)
            degre (int): Indique la longueur des éléments de la liste retournées
            liste (list): Liste de format [] dans laquelle tous les  éléments seront déposés

        Returns:
            liste: La liste de toutes les combinaisons de la liste_valeurs
        """

        quantite_combinaisons = int(len(liste_valeurs)**longueur)
        quantite_addition_chaque_valeur = int(quantite_combinaisons/len(liste_valeurs))

        if liste == []:
            for i in range(quantite_combinaisons):
                liste.append([])

        if longueur != 0:
            for case in range(len(liste)):
                liste[case].append(liste_valeurs[(case//quantite_addition_chaque_valeur) % len(liste_valeurs)])

            obtenir_combinaison(liste_valeurs, longueur - 1, liste)

        return liste  


    def selectionner_case_adjacentes(self, rayon=1):
        """permet d'obtenir une liste de positions des cases adjacentes (diagonales incluses), 
        incluse dans le carré centré sur la position de la case courante, au rayon détérminé. 
        Appeler cette méthode avec rayon 0 serait un peu stupide. Le rayon == 1 est fréquent on retourne simplement une liste préconcue.
        La longueur de la liste = (2rayon + 1)^2, donc si le rayon est plus grand que 2 on calcule par algorithme.
        Args:
            rayon (int): Le nombre de couches à sélectionner, la sélection finale sera un carré centré autour de la case touchée.
            
        Returns:
            list: liste de positions sous la forme de tuples (x,y). Selon la position de la case, cette liste aura 3, 5 ou 8 elements.

        """
        if rayon == 0:
            return self.position
        elif rayon == 1: 
            return [(-1,-1),(-1,0),(0,-1),(0,1),(1,0),(1,1),(1,-1),(-1,1)]
        else:       
            valeurs_operation = list[range(0,rayon)] + [rayon]           
            operations_tuiles_adjacentes = self.obtenir_combinaisons(valeurs_operation, 2, [])
            
        cases_adjacentes = []
           
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