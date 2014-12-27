from scroller import *

class gun(scroller):
    def __init__(self,y,x):
        self.image = pygame.Surface((10,10))
        self.color = (255,100,0)
        self.y = y
        self.x = x
        pygame.draw.circle(self.image, self.color, (5,5), 5)
        self.rect = self.image.get_rect()
        self.rect.centerx = self.x
        self.rect.centery = self.y
        scroller.__init__(self)
        self._dx = 15
        pygame.draw.rect(self.image, self.color,self.rect,3)
        self.shots = 10
    def update(self):
        global screen
        scroller.update(self)
        self.rect.centerx += self._dx
        if self.rect.centerx > pygame.display.get_surface().get_width():
            self.kill()
        if not screen.get_rect().contains(self.image.get_rect()):
            self.kill()
