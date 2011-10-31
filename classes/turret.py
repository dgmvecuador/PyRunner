class turret(scroller):
    def __init__(self,y):
        self.image = pygame.Surface((55,32))
        self.angle = random.randint(-45,45)
        self.top = random.randint(0,1)
        global top
        top = self.top
        self.rect = self.image.get_rect()
        debug(str(self.rect.centerx))
        scroller.__init__(self)
        self.count = 0
        self.x = self.rect.centerx
        if self.top == 1:
            self.rect.top = max_height+1
            self.image.blit(pygame.transform.rotate(gunner,self.angle),(self.rect.centerx-15,-15,0,0))
        else:
            self.rect.bottom = min_height-1
            self.angle += 180
            self.image.blit(pygame.transform.rotate(gunner,self.angle),(self.rect.centerx-15,0,0,0))
        self.rect.right = pygame.display.get_surface().get_width()
        debug(str(self.angle))
    def y(self): #y accessor
        return self.y
    def update(self):
        scroller.update(self)
        self.count += 1
        if self.count == 25:
            bulletGroup.add(bullet(self.rect.centerx,self.rect.centery,self.angle))
        self.gun_sound = load_sound("gunshot.wav")
        self.gun_sound.play()
            debug(str(bulletGroup))
            self.count = 0
        if self.rect.right < 0: #same code to delete self if off screen as block
            self.kill()
            del self
