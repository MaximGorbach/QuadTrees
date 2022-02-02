from QuadTree import *;
import pygame as p;
import random;

#insert a 'num' amount of random points with 'max' as the greatest x and y coord
def insertRand(tree,num,max):
    for i in range(0,num):
        randx = random.randint(0,max)
        randy = random.randint(0,max)
        tree.insert(Point(randx,randy))

def randRegion(max):
    randX = random.randint(0,max)
    randY = random.randint(0,max)
    regType = random.randint(0,1)
    if regType == 1:
        rad = random.randint(0,max/2)
        return Circle(randX,randY,rad)
    else:
        randW = random.randint(0,max)
        randH = random.randint(0,max)
        return Rectangle(randX,randY,randW,randH)

#draws the borders and points of the quadtree
def drawTree(tree,disp):
    if tree is None:
        return
    p.draw.rect(disp,(0,0,0),p.Rect(tree.area.x,tree.area.y,tree.area.w,tree.area.h),2)
    for point in tree.points:
        p.draw.rect(disp,(0,0,0),p.Rect(point.x,point.y,3,3))
    drawTree(tree.nw,disp)
    drawTree(tree.ne,disp)
    drawTree(tree.sw,disp)
    drawTree(tree.se,disp)

def drawQuery(tree,reg,disp):
    points = tree.regionQuery(reg)
    if isinstance(reg,Rectangle):
        p.draw.rect(disp,(0,255,0),p.Rect(reg.x,reg.y,reg.w,reg.h),2)
    else:
        p.draw.circle(disp,(0,255,0),(reg.x,reg.y),reg.r,2)
    for point in points:
        p.draw.rect(disp,(255,0,0),p.Rect(point.x,point.y,3,3))

size = 600
capacity = 1
pointNum = 100
qtree = QuadTree(Rectangle(0,0,size,size),capacity)
insertRand(qtree,pointNum,size)
reg = randRegion(size)

p.init()
gameDisplay = p.display.set_mode((size,size))
gameDisplay.fill((255,255,255))
drawTree(qtree,gameDisplay)
drawQuery(qtree,reg,gameDisplay)
p.display.update()

running = True
while running:
    for event in p.event.get():
        if event.type == p.QUIT:
            running = False

p.quit()
quit