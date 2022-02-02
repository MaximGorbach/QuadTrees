import time;

class QuadTree:
    def __init__(self,area,capacity):
        self.area = area
        if capacity < 1:
            capacity = 1
        self.capacity = capacity
        self.points = []
        self.divided = False
        self.nw = None
        self.ne = None
        self.sw = None
        self.se = None

    #insert a point into the tree
    def insert(self,p):
        if not self.area.contains(p):
            return False
        if len(self.points) < self.capacity and not self.divided:
            self.points.append(p)
        else:
            if not self.divided:
                self.split()
                for point in self.points:
                    self.insert(point)
                self.points = []
            return self.nw.insert(p) or self.ne.insert(p) or self.sw.insert(p) or self.se.insert(p)
        return True

    #splits the tree into 4 regions
    def split(self):
        nw = Rectangle(self.area.x,self.area.y,self.area.w/2,self.area.h/2)
        ne = Rectangle(self.area.x+self.area.w/2,self.area.y,self.area.w/2,self.area.h/2)
        sw = Rectangle(self.area.x,self.area.y+self.area.h/2,self.area.w/2,self.area.h/2)
        se = Rectangle(self.area.x+self.area.w/2,self.area.y+self.area.h/2,self.area.w/2,self.area.h/2)
        self.nw = QuadTree(nw,self.capacity)
        self.ne = QuadTree(ne,self.capacity)
        self.sw = QuadTree(sw,self.capacity)
        self.se = QuadTree(se,self.capacity)
        self.divided = True

    #returns the data stored in a point at coords ('x','y')
    def pointQuery(self,x,y):
        dummyPoint = Point(x,y)
        if not self.nw is None:
            if self.nw.area.contains(dummyPoint):
                return self.nw.pointQuery(x,y)
            elif self.ne.area.contains(dummyPoint):
                return self.ne.pointQuery(x,y)
            elif self.sw.area.contains(dummyPoint):
                return self.sw.pointQuery(x,y)
            elif self.se.area.contains(dummyPoint):
                return self.se.pointQuery(x,y)
        else:
            return dummyPoint.dataFromlist(self.points)

    #function wrapper for getting all points in a region
    def regionQuery(self,region):
        points = self.regQuery(region,[])
        pointsToRem = []
        if points is None:
            return []
        for point in points:
            if not region.contains(point):
                pointsToRem.append(point)
        for point in pointsToRem:
            points.remove(point)
        return points

    #returns potential points in a region, which can be a square or circle
    def regQuery(self,region,points):
        if not region.intersects(self.area):
            return []
        elif not self.divided:
            points.extend(self.points)
        else:
            self.nw.regQuery(region,points)
            self.ne.regQuery(region,points)
            self.sw.regQuery(region,points)
            self.se.regQuery(region,points)
        return points

    def __repr__(self):
        return "(%s, NW: %s, NE: %s, SW: %s, SE: %s)" %(str(self.points),str(self.nw),str(self.ne),str(self.sw),str(self.se))

#point class stores x,y and some data
class Point:
    def __init__(self,x,y,data=None):
        self.x = x
        self.y = y
        if data is None:
            self.data = (x,y)
        else :
            self.data = data

    #return the data stored in the point with matching coords to the current point from a
    #list of points
    def dataFromlist(self,plist):
        for point in plist:
            if point == self:
                return point.data
        return None

    def __eq__(self,other):
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        return "Point at (%s,%s)" %(self.x,self.y)

#rectangle used as a boundary for the qtree and a query region
class Rectangle:
    def __init__(self,x,y,w,h):
        self.x = x
        self.y = y
        self.w = w
        self.h = h

    #check if region contains a point
    def contains(self,p):
        return p.x >= self.x and p.x <= self.x + self.w \
            and p.y >= self.y and p.y <= self.y + self.h

    def intersects(self,other):
        if(self.x >= other.x +other.w or other.x >= self.x + self.w):
            return False
        
        if(self.y >= other.y +other.h or other.y >= self.y + self.h):
            return False
        return True

    def __repr__(self):
        return "Rectangle at (%s,%s) w: %s, h: %s" %(self.x,self.y,self.w,self.h)

class Circle:
    def __init__(self,x,y,r):
        self.x = x
        self.y = y
        self.r = r

    def distToSqrd(self,p):
        return (self.x - p.x)**2 + (self.y - p.y)**2

    def contains(self,p):
        return (self.distToSqrd(p) <= self.r**2)

    def intersects(self,rect):
        if(self.x + self.r < rect.x or self.x - self.r > rect.x + rect.w):
            return False
        
        if(self.y + self.r < rect.y or self.y - self.r > rect.y + rect.h):
            return False

        return True