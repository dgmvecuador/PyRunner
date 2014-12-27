from scroller import *

class block(scroller):
    def __init__(self, y):
        scroller.__init__(self)
        self.image = pygame.Surface((20, 90))
        self.rect = self.image.get_rect()
        self.y = y

        colors = [(155, 155, 155), (55, 55, 55), (0, 255, 0), (91, 81, 61)]
        # a color is chosen at random
        color = random.choice(colors)

        pygame.draw.rect(self.image, color, self.rect)
        self.rect.right = pygame.display.get_surface().get_width()
        self.rect.centery = y
        #make sure the block is on the screen
        #debug("block with center y of {0:n}".format(self.rect.centery))
    def update(self):
        scroller.update(self)
        if self.rect.right < 0:
            self.kill()
            del self
    def y(self):
        return self.y
    def __str__(self):
        return "block: ",self.y
