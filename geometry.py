###############
#
# Here json gets converted to polygons (Lists of Points) and vice versa
#
###########

import json, sys

offset = [566300.0, 5932300.0]
zoom = 2

class Geometry:
    minx=miny=sys.maxsize
    maxx=maxy=-sys.maxsize

    def __init__(self, points = []):
        self.points = points
        for newp in points:
            if(newp[0] < self.minx) : self.minx = newp[0]
            if(newp[0] > self.maxx) : self.maxx = newp[0]
            if(newp[1] < self.miny) : self.miny = newp[1]
            if(newp[1] > self.maxy) : self.maxy = newp[1]

    def getRect(self):
        return self.minx, self.miny, self.maxx-self.minx, self.maxy-self.miny

    @staticmethod
    def fromjson(filepath):
        print(filepath)
        ret = []
        with open(filepath) as file:
            data = json.load(file)
            for feature in data["features"]:
                for point in feature["geometry"]["coordinates"][0][0]:
                    newp = ((point[0]-offset[0])/zoom,-(point[1]-offset[1])/zoom)

                    print(newp)
                    ret.append(newp)
        
        return Geometry(ret)


    @staticmethod
    def createTest():
        return Geometry([(10,10), (20,10), (30,15), (20,20), (10,20)])
