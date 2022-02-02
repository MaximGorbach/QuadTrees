from QuadTree import *;
import pygame as p;
import random;
import time;
from Vectors import *;

class Particle:
    def __init__(self,pos,vel,mass=30):
        self.pos = pos
        self.vel = vel
        self.accel = Vector(0,0)
        self.mass = mass
        self.size = (mass/10)**2
        self.col = (0,0,0)

    def move(self):
        self.vel += self.accel
        self.pos += self.vel

    def distToSqrd(self,other):
        return (self.pos.x - other.pos.x)**2 + (self.pos.y - other.pos.y)**2

    def isTouching(self,other):
        if(self.pos.x >= other.pos.x +other.size or other.pos.x >= self.pos.x + self.size):
            return False
        
        if(self.pos.y >= other.pos.y +other.size or other.pos.y >= self.pos.y + self.size):
            return False
        return True
    
    def __repr__(self):
        return "Particle at %s vel: %s acc: %s" \
            %(str(self.pos),str(self.vel),str(self.accel))

    def __eq__(self,other):
        return(self.pos == other.pos and self.vel and other.vel and self.accel == other.accel and self.mass == other.mass)

#draws all particles from array onto screen
def drawParticles(ps,display):
    for particle in ps:
        p.draw.rect(display,(0,0,0),p.Rect(particle.pos.x,particle.pos.y,particle.size,particle.size))

#check if a particle have gone over the edge of the screen
def checkEdges(part,size):
    if part.pos.x > size.x:
        part.pos.x = 0
    if part.pos.x < 0:
        part.pos.x = size.x
    if part.pos.y > size.y:
        part.pos.y = 0
    if part.pos.y < 0:
        part.pos.y = size.y
        
#updates positions of all particles in array
def moveParticles(ps,size):
    for particle in ps:
        particle.move()
        checkEdges(particle,size)
        
#generates a random vector
def randVector(max,neg=False):
    if neg == False:
        randx = random.randint(0,max.x)
        randy = random.randint(0,max.y)
    else:
        randx = random.randint(-(max.x),max.x)
        randy = random.randint(-(max.y),max.y)
    return Vector(randx,randy)

#generates a 'num' amount of random particles
def genRandParts(num, size):
    ps = []
    for i in range(0,num):
        pos = randVector(size)
        vel = randVector(Vector(7,7),True)
        particle = Particle(pos,vel)
        ps.append(particle)
    return ps

#returns a new quadtree containing all particles in array
def updateTree(ps,size,capacity):
    tree = QuadTree(Rectangle(0,0,size.x,size.y),capacity)
    for part in ps:
         tree.insert(Point(part.pos.x,part.pos.y,part))
    return tree

#check if any particles are touching
def checkIsTouching(ps,tree,display):
    for particle in ps:
        closeParts = tree.regionQuery(Circle(particle.pos.x,particle.pos.y,particle.size))
        for part in closeParts:
            if part.data != particle:
                p.draw.rect(display,(255,0,0),p.Rect(part.data.pos.x,part.data.pos.y,part.data.size,part.data.size))
        
#the supposedly slower version
def checkIsTouching2(ps,display):
    for particle in ps:
        for other in ps:
            if particle != other:
                if particle.isTouching(other):
                    p.draw.rect(display,(255,0,0),p.Rect(particle.pos.x,particle.pos.y,particle.size,particle.size))

#declaring constants
size = Vector(1200,700)
capacity = 1
partNum = 500

p.init()
gameDisplay = p.display.set_mode((size.x,size.y))
clock = p.time.Clock()

particles = genRandParts(partNum,size)

running = True
while running:

    for event in p.event.get():
        if event.type == p.QUIT:
            running = False
    
    gameDisplay.fill((255,255,255))

    moveParticles(particles,size)
    qtree = updateTree(particles,size,capacity)
    drawParticles(particles,gameDisplay)
    checkIsTouching(particles,qtree,gameDisplay)
    
    p.display.update()
    clock.tick(30)

p.quit()
quit
