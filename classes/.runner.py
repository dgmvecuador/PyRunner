class runner(pygame.sprite.Sprite):
    def __init__(self, screen):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(os.path.join(\
            "Resources","runner.bmp"))
        self.image = self.image.convert()
        self.rect = self.image.get_rect()
        self.rect.centerx = 70
        if not _debug:
            self.rect.centerx = 120
        self.rect.centery = screen.get_rect().centery
        self.dy = 4
        self.flash = False #are we flashing (invunrable after collision)
        self.shield = 3 #how much is left in our shield
        self.count = 0 #this is the count for the flashing
        self.visible = True #do we want to be visible (next update)
        self.isvisible = True #are we actually visible
        self.flashRate = 8 #number of frames it will take to toggle the flash
        self.inv = False
        self.gun = 0
        self.last_shot = 10
        self.shots = 0
        self.invCount = 800
        self.ammo = 0

        # Load the sound
        self.punch_sound = load_sound("punch.wav")
        self.explosion_sound = load_sound("explosion.wav")
    self.gun_sound = load_sound("gunshot.wav")

    def hit(self):
        if not self.inv:
            if not self.flash: #if not already flasshing from a collision
                self.shield -= 1
                self.punch_sound.play()
                if not self.shield == 0:

                    debug("play")
                    self.flash = True #start flashing
                    self.count = 96 #for 96 frames
                    effectsGroup.add(fadeEffect((255,0,0)))
                    mainLevelManager.fallback(400)
                else:
                    # Explosion when you lose.
                    for x in xrange(6):
                        self.gun_sound.play()

    def update(self):
        #set our own dy to scroller.dx minus 2
        self.dy = scroller.dx - 2
        key = pygame.key.get_pressed()
        #key up and down events
        if key[K_UP]:
            self.rect.centery += -self.dy
        if key[K_DOWN]:
            self.rect.centery += self.dy
        if key[K_SPACE]:
            if self.gun > 1:
                debug("reload")
                self.shots = 0
                self.gun = 1
                self.ammo = 10
            elif self.gun == 1:
                debug(self.gun)
                if self.shots > 9:
                    self.shots = 0
                    self.gun = 0
                    self.ammo = 0
                else:
                    self.last_shot +=1
                    if self.last_shot >= 10:
                        self.shots +=1
                        gunnerGroup.add(gun(self.rect.centery,self.rect.centerx))
                        self.last_shot = 0
                        debug("gunnerGroup" + str(gunnerGroup))
                        self.ammo -= 1
            self.gun_sound.play()
        #clip to our max and min heights created when we make borders
        if self.rect.top < max_height+1:
            self.rect.top = max_height+1
        if self.rect.bottom > min_height-1:
            self.rect.bottom = min_height-1
        if self.flash:
            self.count -= 1
            self.flashRate -= 1
            if self.flashRate == 0: #if the flash rate is 0 we toggle visiblity
                if self.visible:
                    self.visible = False
                else:
                    self.visible = True
                self.flashRate = 8
        if self.visible != self.isvisible: #if the wanted visible is different
            self.image.set_alpha(255*self.visible)
            self.isvisible = self.visible
        if self.count == 0:
            self.flash = False #stop flashing when we are finished
        if self.inv:
            self.invCount -= 1
        if self.invCount == 0:
            self.inv = False
            self.invCount = 800
        if self.shield == 0:
            self.kill()
    def invinc(self):
        self.inv = True
        if self.invCount < 700:
            self.invCount = 800

