import pygame
from functions import *

#class that displays color and then fades out
class fadeEffect(pygame.sprite.Sprite):
    def __init__(self,color):
        pygame.sprite.Sprite.__init__(self)
        #create a surface matching the display size
        self.image = pygame.Surface(pygame.display.get_surface().get_size())
        #fill
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.alpha = 96 #match this with the flash count of the runner
    def update(self):
        self.image.set_alpha(self.alpha)
        #update alpha and decrease every frame
        self.alpha -= 1
        if self.alpha == 0:
            self.kill()
    def kill(self):
        debug("KILLED ME")
        pygame.sprite.Sprite.kill(self)
