"""Module génération Labyrinth récursif"""
import random

class NoeudCellule() :
    def __init__(self, pos, murs):
        self.pos=pos
        self.gauche=None
        self.droit=None
        self.murs=murs
        
    def __repr__(self):
        """permet d'afficher un arbre sous forme d'une liste"""
        if self==None:
            return None
        else :
            return str([self.pos, self.gauche, self.droit, self.murs])
        
    def creerfd(self, pos, murs):
        """crée et retourne un noeud fils droit ayant pour valeur le paramètre cle"""
        assert self.droit is None,"Le Noeud possède déjà un fils droit"
        self.droit=NoeudCellule(pos, murs)
        return self.droit
        
    def creerfg(self, pos, murs):
        """crée et retourne un noeud fils gauche ayant pour valeur le paramètre cle"""
        assert self.gauche is None,"Le Noeud possède déjà un fils gauche"
        self.gauche=NoeudCellule(pos, murs)
        return self.gauche
		
########      
class Grille :
    
    """Classe permettant de générer un labyrinthe avec la méthode 'arbre binaire'"""
    
    def __init__(self, nx, ny):
        
        """construction d'une grille labyrinthique de dimension (nx - largeur, ny - hauteur)"""
        
        self.nx = nx
        self.ny = ny
        CoorList=[]
        for x in range(nx): 
            for y in range(ny):
                CoorList.append((x, y))
        item=NoeudCellule(CoorList[0], {'N' : True, 'O' : True})
        Recurs(item, CoorList)
        self.grille = item
    
    def GetMurs(self, x, y, arbre):
        
        coordo=(x, y)
        
        def parcours(coord, arbre):
            if arbre.pos==coord:
                global resu
                resu=arbre.murs
            if arbre.gauche!=None:
                parcours(coord, arbre.gauche)
            if arbre.droit!=None:
                parcours(coord, arbre.droit)
        parcours(coordo, arbre)
        return resu
		
"""algorithme récursif, construit un arbre aléatoirement à partir d'un noeud et dictionnaire de coordonnées
   chaque noeud possède un attribut position, et murs, qui varie selon le chemin emprunté"""
def Recurs(noeud, dic):
    posx, posy=noeud.pos[0], noeud.pos[1]
    #si le noeud n'a pas été parcouru, le supprime du dictionnaire
    if noeud.pos in dic:
        del dic[dic.index(noeud.pos)]
    chx=random.choice([1, 2])
    #si le choix=1, créer une cellule sur l'axe x, puis l'axe y
    if chx==1:
        RecursXY(noeud, dic, 1, 0)
        #même procédé mais pour l'axe des ordonnées
        RecursXY(noeud, dic, 0, 1)
    #si le choix=2, créer une cellule sur l'axe y, puis l'axe x, même procédé que si chx==1
    else :
        RecursXY(noeud, dic, 0, 1)
        RecursXY(noeud, dic, 1, 0)
		
def RecursXY(noeud, dic, x, y):
    posx, posy=noeud.pos[0], noeud.pos[1]
    chx2=random.choice([1, 2])
    #si 2ème choix=1, recule d'une cellule sur l'axe des abcisses
    if noeud.gauche==None:
        if (posx-x, posy-y) in dic and chx2==1:
            noeud.murs={'N' : x*noeud.murs['N'], 'O' : y*noeud.murs['O']}
            Recurs(noeud.creerfg((posx-x, posy-y), {'N' : 1, 'O' : 1}), dic)
            #si le fils gauche est occupé, vérifie le fils droit
        elif (posx+x, posy+y) in dic:
            Recurs(noeud.creerfg((posx+x, posy+y), {'N' : x, 'O' : y}), dic)
        #au cas où une incrémentation serait impossible sur le fils gauche, décrémenter
        elif (posx-x, posy-y) in dic:
            noeud.murs={'N' : x*noeud.murs['N'], 'O' : y*noeud.murs['O']}
            Recurs(noeud.creerfg((posx-x, posy-y), {'N' : 1, 'O' : 1}), dic)
    if noeud.droit==None:
        if (posx-x, posy-y) in dic and chx2==1:
            #si le fils droit est libre, y assigne une position
            noeud.murs={'N' : x*noeud.murs['N'], 'O' : y*noeud.murs['O']}
            Recurs(noeud.creerfd((posx-x, posy-y), {'N' : 1, 'O' : 1}), dic)
        elif (posx+x, posy+y) in dic:
            Recurs(noeud.creerfd((posx+x, posy+y), {'N' : x, 'O' : y}), dic)
        elif (posx-x, posy-y) in dic:
            noeud.murs={'N' : x*noeud.murs['N'], 'O' : y*noeud.murs['O']}
            Recurs(noeud.creerfd((posx-x, posy-y), {'N' : 1, 'O' : 1}), dic)