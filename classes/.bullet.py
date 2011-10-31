class bullet(scroller):
    def __init__(self,x,y,angle):
        self.image = pygame.Surface((10,10))
        pygame.draw.circle(self.image, (255,145,35), (5,5), 5)
        self.color = ((255,145,35))
        self.angle = angle
        scroller.__init__(self)
        self.y = y+5
        self.x = x+8
        self.mag = 15
        self.rect = self.image.get_rect()
        self.rect.centery = self.y
        self.rect.centerx = self.x
        pygame.draw.rect(self.image, self.color,self.rect,3)
        self._dy = math.cos(math.radians(self.angle))*self.mag
        self._dx = math.sin(math.radians(self.angle))*self.mag
    def update(self):
        scroller.update(self)
        self.rect.centery += self._dy
        self.rect.centerx += self._dx
        if top == 1:
            if self.rect.centery > min_height:
                self.kill()
        if top == 0:
            if self.rect.centery < max_height:
                self.kill()
        if not screen.get_rect().contains(self.image.get_rect()):
            self.kill()
