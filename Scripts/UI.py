import pygame
from pygame.locals import *

class bouton():
    """Objet définisant un bouton de l'interface graphique Pygame."""
    def __init__(self,sprite, Oversprite, x, y):
        self.sprite=sprite
        self.Oversprite = Oversprite
        self.x=x
        self.y=y
        
    def draw(self,surface):
        """Afficher le bouton sur la surface souhaité."""
        surface.blit(self.sprite,(self.x,self.y))
    
    def drawOver(self,surface):
        surface.blit(self.Oversprite,(self.x,self.y))
    
    def isOver(self,pos):
        """Méthode permettant de savoir si une position est par dessus le bouton.
        Retourne TRUE si elle l'est et FALSE si elle ne l'est pas"""
        if pos[0]> self.x and pos[0] < self.x+self.sprite.get_width():
            if pos[1]>self.y and pos[1]< self.y + self.sprite.get_height():
                return True
        return False
