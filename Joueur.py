from cases import CaseBombe, CaseVide
from random import randint

class Joueur():
    """Classe de base des joueurs humains et ordinateurs
    """
    def __init__(self, tableau, index):
        self.index = index
        self.tableau = tableau
        self.elimine = False
        self.cases = {}
    
    def jouer(self, tour):
        """Initialise un tour pour toute classe de joueur

        Args:
            tour (int): indique le nombre de fois où jouer s'est fait appeler récursivement.
        """
      
        self.tableau.verifier_victoire()
        if self.tableau.en_cours:
            self.tableau.print_tableau(tour)
            
            
    def choisir_action(self):
        """Précisée dans les sous-classes
        """
        pass

         
        
    #def executer_action(self, choix):
    #    """Le choix passé en argument est exécuté sur les cases du tableau
#
    #    Args:
    #        choix (int, int, str): 3 objets en une variable:
    #                               x: position en x de la case à modifier
    #                               y: position en y de la case à modifier
    #                               action: tourner, flagger ou chorder (https://en.wikipedia.org/wiki/Chording)
    #    """
#
    #    x,y,action = choix
    #    if action.lower() == "f":
    #        self.tableau.cases[(x,y)].flag_case()
    #    elif action.lower() == "t":
    #        self.tableau.cases[(x,y)].tourner_case()
    #    elif action.lower() == "c":
    #        self.tableau.cases[(x,y)].chord_case()
    #    else: print("erreur choix") 
    #    
    #        
    #def executer_premier_tour(self, choix):
    #    """Généralement, au démineur, une bombe ne peut pas être trouvée au premier tour. Le premier tour doit donc être différent, sans affecter le hasard des bombes.
    #    """
#
    #    x,y,action = choix
    #    # S'il y a une bombe, on la déplace de façon aléatoire
    #    if (x,y) in self.tableau.bombes:
    #        self.tableau.bombes.append((x,y))
    #        self.tableau.cases[(x,y)] = CaseVide((x,y), self.tableau)
    #        
    #        while len(self.tableau.bombes) < self.tableau.nbr_bombes:
    #            x_bombe = randint(1,self.tableau.dimension_x)
    #            y_bombe = randint(1,self.tableau.dimension_y)
    #            if (x_bombe,y_bombe) not in self.tableau.bombes:
    #                self.tableau.bombes.append((x,y))
    #                self.tableau.cases[(x_bombe,y_bombe)] = CaseBombe((x_bombe,y_bombe), self.tableau)
    #    
    #    self.executer_action(choix)
        
class JoueurHumain(Joueur):
    """Classe du joueur humain, représente toutes les méthodes avec lesquelles un joueur humain peut faire un choix

    """
    def __init__(self, tableau, index):
        super().__init__(tableau, index)
    
    
    def jouer(self, tour):
        """Déroulement du jeu pour l'humain:
        1 - Vérification victoire (via verifier_victoire) ou défaite (via self.tableau.en_cours) - hérité
        2 - Le tableau est imprimé - hérité
        3 - Le joueur prend une décision
        4 - La décision est exécutée
        5 - L'étape 1 est reprise 
        """
        super().jouer(tour)
                    
        if self.tableau.en_cours:
            if tour == 1:
                self.tableau.executer_premier_tour(self.choisir_action())
            else:
                self.tableau.executer_action(self.choisir_action())
            self.jouer(tour+1)


        

        
        
    def choisir_action(self):
        """le joueur est invité à entrer 3 valeurs dans la console pour modifier une case

        Returns:
            (int, int, str): 3 objets en une variable:
                x: position en x de la case à modifier
                y: position en y de la case à modifier
                action: tourner, flagger ou chorder
 
        """
        super().choisir_action()
        while True:
            case_x = int(input("Quel case voulez-vous tourner? position en x:"))
            case_y = int(input("Quel case voulez-vous tourner? position en y:"))
            if (case_x,case_y) in self.tableau.cases:
                if not self.tableau.cases[(case_x,case_y)].tournee:
                    action = input("Tourner un case 't', Flagger un case 'f', Chorder une case avec 'c'?")
                    if action.lower() == "t" or action.lower() == "f" or action.lower() == "c":
                        return case_x, case_y, action
            else: print("Entrée invalide: (La case donnée n'est pas dans le tableau, ou est déjà tournée)")
                    
       
class JoueurOrdinateur(Joueur):
    """Classe d'un joueur ordinateur, algorithme de prise de décisions intelligentes
    """
    def __init__(self, tableau, index):
        super().__init__(tableau, index)
        self.cases_oubliees = []
        self.cases_information = []
        self.cases_a_tourner = []
        self.cases_cachees = self.tableau.cases.keys()
        
                
    def jouer(self, tour):
        super().jouer(tour)
        if tour == 1:
            self.jouer_premier_tour()
        
        if self.tableau.en_cours:        
            self.classer_cases()
            self.decisions_simple()
            if self.tableau.en_cours:
                self.decision_complexe()
        self.joueur(self, tour + 1)

    
    def jouer_premier_tour(self):
        case_random = randint(0, len(self.cases_cachees))
        self.tableau.cases[case_random].tourner_case
    
    def classer_cases(self):
        """Classe les cases dans leurs sous-groupes respectifs: 
            Groupe 1 - (Tournées ou flag: oubliées | information) : 
             Sous-Groupe 1.1 - oubliées (Toutes cases tournées qui ne touchent aucune case non-tournée, non-flag)
             Sous-Groupe 1.2 - information (Toutes cases tournées qui touchent une case non tournée non flag)
            Groupe 2 - (non-tournées: a_tourner | oubliées):
             Sous-Groupe 2.1 - a_tourner (Toutes cases non-tournees, non-flag, qui touchent une case tournée, à prioriser pour tourner)
             Sous-Groupe 2.2 - cachées (Toutes cases non-tournées, non-flag, qui ne touchent aucune case tournée))
             *Suivant cet ordre, toute case commence au bas, et les cases peuvent seulement se déplacer 
             du bas vers le haut.Tout déplacement bas - > haut est possible directement (ex. cachées - > information, a_tourner -> oubliées)
           *L'ordre du classement ci-dessous ne peut pas être changé.
            """
        obtenir_cases()
        classer_cases_tournees()
        classer_reste()
    
    
        
        
        def obtenir_cases(self):
            """Le Joueur obtient la valeur des cases tournées à partir du tableau. 
            Les input du tableau sont seulement ici pour le joueur ordinateur, permet de s'assurer qu'il n'y a pas de trichage!
            """
            for case in self.tableau.cases:
                if self.tableau.cases[case].tournee:
                    self.cases[case] = self.tableau.cases[case].valeur
                elif self.tableau.cases[case].flag:
                    self.cases[case] = "F"
                else:
                    self.cases[case] = "X"
                    
                
        def classer_cases_tournees(self):
            "Déplace toutes les cases appropriées (tournées) Groupe 2 -> Groupe 1. Toutes les cases déplacées se retrouvent dans sous-groupe 1.2"

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
                    
         
    def decisions_simple(self):
        """La majorité des décisions "simples" devraient se faire ici. 
        Simple: Décision qui ne nécéssitent pas de prendre en compte plusieurs cases information pour modifier une case a modifier
        ex1: Une case 2 touche déjà 2 drapeaux, on tourne alors toute case adjacentes au 2, sauf les cases flaggées.
        ex2: Une case 1 touche seulement une case non tournée. On met donc un drapeau sur cette case.
        mauvais exemple: pattern 1-2-1 est par dessus 3 cases non-tournées en parralèle, les 3 cases ne touchent aucune autre case non-tournées. 
        La seule possibilité est que les cases sous 1-2-1 soient respectivement Bombe-Vide-Bombe.
        
        """
        # Cette étape est généralement inutile, mais pas tout le temps 
        self.analyse_integrale_chord()
        
        # Étape plus importante, elle fonctionne en plusieurs vagues de type 1-flag 2-chord cases adjacentes au flag.
        self.analyse_integrale_flag()
        
    def decision_complexe(self):
        """Cette méthode est appelée quand l'ordinateur ne trouve plus de modification simple à apporter au tableau. Sans aucun doute la partie la plus complexe du jeu.
        """
        
        self.creer_groupes_superposes()
        modification_apportee = self.comparer_groupes_superposes()
        if not modification_apportee:
            self.simplifier_groupes_superposes()
            nouvelle_modification_apportee = self.comparer_groupes_superposes()
            if not modification_apportee:
                self.deviner_une_case()
    
    def creer_groupes_superposes(self):
        liste_groupes = []
        for case_tournee in self.cases_information:
            compte = 0
            valeur = self.tableau.cases[case_tournee].valeur
            groupe_case = []
            cases_adjacentes = self.tableau.cases[case_tournee].selectionner_cases_adjacentes()
            for case in cases_adjacentes:
                if self.tableau.cases[case].flag: 
                    valeur = valeur - 1
                elif self.tableau.cases[case].tournee:
                    groupe_case.append(case)
            liste_groupes.append((valeur), groupe_case)
                    
        self.groupe_superposes = liste_groupes
        
    def comparer_groupes_superposes(self):
        pass

    
    def simplifier_groupes_superposes(self):
        pass
    
    def deviner_une_case(self):
        for case in self.cases_cachees:
            index_case_random = randint(0, len(self.cases_cachees))
            case_random_a_tourner = self.cases_cachees
            self.tableau.cases[case_random_a_tourner].tourner_case()
    
                   
    def analyse_integrale_chord(self):
        """Toutes les cases "information" sont chordées en boucle jusqu'à ce qu'une boucle tourne aucune case.
        """
        boucle_chord_utile = True
        while boucle_chord_utile:
            boucle_chord_utile = False
            for case in self.cases_information:
                case_tournee = self.tableau.cases[case].chord_case()
                if case_tournee:
                    boucle_chord_utile = True
            if boucle_chord_utile:
                self.classer_cases()
                    
    def analyse_integrale_flag(self):
        """Toutes les cases "information" sont flaggées selon l'algorithme verifier_flag_simple(case), en boucle,
        jusqu'à ce qu'une boucle ne flag aucune case. Une boucle est plus efficace, puisque l'algorithme de flagging 
        intelligent chorde les cases adjacentes, ouvrant de nouvelles opportunités de flagging.
        """
        boucle_flag_utile = True
        while boucle_flag_utile:
            boucle_flag_utile = False
            for case in self.cases_information:
                case_flaggée = self.verifier_flag_simple(case)
                if case_flaggée:
                    boucle_flag_utile = True
            if boucle_flag_utile:
                self.classer_cases()
        

    
    def tourner_case(self,position):
        """Tourne simplement la case selectionnée

        Args:
            position (tuple): forme (xmy)
        """
        self.tableau.cases[position].tourner_case()
            
        

    def verifier_flag_simple(self, position):
        """La fonction vérifie si la case "information" en argument touche le même nombre de cases non-tournées que sa valeur, si c'est le case, flag_intellgient_case est appelé
        Args:
            position (tuple): position de la case en forme (x,y) de la position de la case à tourner. 
        """
        compte = 0
        cases_adjacentes = self.tableau.cases[position].selectionner_cases_adjacentes()
        for case in cases_adjacentes:
            if not self.tableau.cases[case].tournee:
                compte += 1
        if compte == self.tableau.cases[position].valeur:
            self.flag_intelligent_case(position)
            return True
        return False
            
        
    
    def flag_intelligent_case(self, position):
        """Fonction utliisée quand une case doit être flag, on modifie la valeur flag de la case dans le tableau, 
        et on chord automatiquement toute cases tournée adjacentes à la case flaggée.

        Args:
            position (tuple): position de la case en forme (x,y)
        """
        
        self.tableau.cases[position].flag_case()
        cases_adjacentes = self.tableau.cases[position].selectionner_cases_adjacentes()
        
        # On passe 2 fois, si chorder un case asjacentes tourne une case adjacente déjà passée, non-chordée, on a une perte d'efficacité. 
        loop_a_faire = True
        while loop_a_faire:
            loop_a_faire = False
            for case in cases_adjacentes:
                if self.tableau.cases[case].tournee:
                    if self.tableau.cases[case].chord_case():
                        loop_a_faire = True

        
   
         
    
    
        