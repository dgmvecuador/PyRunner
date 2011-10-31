#special group class to manage rezzing of objects that are randomly created, objects in the group must have a initialalizer of (self,y)
class randomRezGroup(pygame.sprite.RenderUpdates):
    def __init__(self,templateClass,maxRezHeight,minRezHeight,maxInRow=3,minDistance=75,minRowDistance=100,\
                 maxRowDistance=200,active=True):
        pygame.sprite.RenderUpdates.__init__(self)
        #initialize this
        self.nextRowPosition = 0
        #this signals the draw method to create its first row
        self.lastRowPosition = -1
        #assign some instance variables
        self.templateClass = templateClass
        self.minDistance = minDistance
        self.minRowDistance = minRowDistance
        self.maxRowDistance = maxRowDistance
        self.maxRezHeight = maxRezHeight
        self.minRezHeight = minRezHeight
        self.maxInRow = maxInRow
        self.active = active
        debug("self.templateClass "+str(self.templateClass)+"\nself.minDistance "+str(self.minDistance)+"\nself.minRowDistance "+str(self.minRowDistance)+\
              "\nself.maxRowDistance "+str(self.maxRowDistance)+"\nself.maxRezHeight "+str(self.maxRezHeight)+"\nself.minRezHeight "+str(self.minRezHeight)+\
              "\nself.maxInRow "+str(self.maxInRow))
    def update(self):
        #override update method to handle drawing of new rows if needed
        if (self.lastRowPosition == -1 or self.lastRowPosition >=self.nextRowPosition) and self.active:
            #choose random locations for blocks based on maxBlockInRow
            spritesInRow = []
            for x in xrange(random.randint(1,self.maxInRow)):
                #randomly choose how many blocks to create
                #randomly select block positions and add to group
                spritesInRow.append(self.templateClass(random.randint(\
                                                    self.maxRezHeight,\
                                                      self.minRezHeight)))

            self.add(spritesInRow)
            #check for minBlockDistance compliance
            orderedSprites = sorted(spritesInRow,key=self.templateClass.y)
            #go through ordered sprites and check for distance compliance
            i = -1 #counter variable
            for x in orderedSprites:
                if i >= 0: #ignore first one
                    topSprite = orderedSprites[i].rect.bottom #list is ordered
                    #in top to bottom order by position, this is the higher up
                    #one. we get its bottom x position
                    bottomSprite = x.rect.top #get the top position of the lower
                    #sprite
                    #debug("topSprite: {0:n}\nbottomSprite: {1:n}".format(\
                        #topSprite,bottomSprite))
                    if (bottomSprite - topSprite) < self.minDistance: #check
                        #for correct distance and if nessecary delete the sprite
                        x.kill()
                        #debug("sprite distance kill")
                i += 1
            #randomly choose our next row position
            self.nextRowPosition = random.randint(self.minRowDistance,\
                                             self.maxRowDistance)
            #track our just created last row
            self.lastRowPosition = 0
        #last row position increases by scroller.dx every frame
        self.lastRowPosition += scroller.dx
        return pygame.sprite.RenderUpdates.update(self)