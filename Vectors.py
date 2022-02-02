class Vector:
    def __init__(self,x,y):
        self.x = x
        self.y = y

    def __add__(self,other):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self,other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self,num):
        return Vector(self.x * num, self.y * num)
    
    def __repr__(self):
        return "(%s,%s)" %(self.x,self.y)
    
    def __eq__(self,other):
        return (self.x == other.x and self.y == other.y)
