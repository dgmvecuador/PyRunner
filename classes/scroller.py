#super class for all scrolling objects
class scroller(pygame.sprite.Sprite):
    dx = 6
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
    def update(self):
        self.rect.centerx -= self.dx
    screen = None
