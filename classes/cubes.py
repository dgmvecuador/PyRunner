class cube(scroller):
    def __init__(self,y):
        scroller.__init__(self)
        self.image = pygame.Surface((20,20))
        self.rect = self.image.get_rect()
        pygame.draw.rect(self.image, self.color,self.rect,3)
        self.y = y
        self.rect.right = pygame.display.get_surface().get_width()
        self.rect.centery = self.y
    def update(self):
        scroller.update(self)
        if self.rect.right < 0: #same code to delete self if off screen as block
            self.kill()
            del self
    def y(self): #y accessor
        return self.y
    def hit(self):
        effectsGroup.add(fadeEffect(self.color))

class scoreCube(cube):
    scoreProbabilites = [500,500,500,500,1000,1000,2000] #define probablility list for scores
    def __init__(self,y):
        #choose a random score
        self.score = random.choice(self.scoreProbabilites)
        #define the image options
        self.colors = {500: (0,0,255),1000:(0,255,0),2000:(255,0,255)}
        #choose a image corresponding with the score
        self.color = self.colors[self.score]
        #debug("scoreCube with y: "+str(y))
        cube.__init__(self,y) #call the initializer after these two commands
    def score(self): #score accessor
        return self.score
class gunCube(cube):
    def __init__(self,y):
        self.color=(255,0,0)
        cube.__init__(self,y)
    def hit(self):
        rungroup.sprite.gun += 1
        debug(str(rungroup.sprite.gun))

class invCube(cube):
    def __init__(self,y):
        self.color = (255,255,255)
        cube.__init__(self,y)

class shieldCube(cube):