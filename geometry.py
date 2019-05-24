###############
#
# Here json gets converted to polygons (Lists of Points) and vice versa
#
###########

import json, sys
import math

def parsePolygon(feature):
    pass

def rotatePointAroundOrigin(point, angle):
    # point to rotate nad angle in degrees
    #
    #     / cos t   -sin t  \
    # M = |                 |
    #     \ sin t   cos t   /
    #
    # r = M * p

    m11 = math.cos(math.radians(angle))
    m12 = -math.sin(math.radians(angle))
    m21 = math.sin(math.radians(angle))
    m22 = math.cos(math.radians(angle))
    
    ret = (point[0] * m11 + point [1] * m12,
           point[0] * m21 + point [1] * m22)

    return ret

class Geometry:
    minx=miny=sys.maxsize
    maxx=maxy=-sys.maxsize

    defaultid = 0

    def __init__(self, points = []):
        self.id = "0"
        self.points = points
        for newp in points:
            if(newp[0] < self.minx) : self.minx = newp[0]
            if(newp[0] > self.maxx) : self.maxx = newp[0]
            if(newp[1] < self.miny) : self.miny = newp[1]
            if(newp[1] > self.maxy) : self.maxy = newp[1]

        self.properties = {}

    def getRect(self):
        return self.minx, self.miny, self.maxx-self.minx, self.maxy-self.miny

    def toGeoJSON(self):
        ret = "{\"type\": \"Feature\",\"id\": \"" 
        ret += str(self.id) 
        ret += "\",\"geometry\": {\"type\": \"Polygon\",\"coordinates\": [["

        for p in self.points:
            ret+="["+str(p[0])+","+str(p[1])+"],"
        ret+="["+str(self.points[0][0])+","+str(self.points[0][1])+"]" # closed ring, last one without trailing comma

        ret += "]]}}"
        return ret

    @staticmethod
    def fromjson(filepath):
        geoms = []
        try:
            with open(filepath) as file:
                try:
                    data = json.load(file)
                except ValueError:
                    print("No JSON found!")
                    return []
                idx = 1
                for feature in data["features"]:
                    points = []
                    #print(feature)
                    if feature["geometry"]["type"] == "MultiPolygon":
                        for point in feature["geometry"]["coordinates"][0][0]:
                            newp = (point[0],-point[1])
                            points.append(newp)
                    elif feature["geometry"]["type"] == "Polygon":
                        for point in feature["geometry"]["coordinates"][0]:
                            newp = (point[0],-point[1])
                            points.append(newp)
                    g = Geometry(points)
                    g.id = filepath + str(idx)
                    idx += 1
                    g.properties = feature["properties"]
                    geoms.append(g)
        except EnvironmentError:
            print("GeoJSON file not found!")
            return []
        
        return geoms

    @staticmethod
    def createObject(filepath, id, position, orientation):
        ret = []

        with open(filepath) as file:
            data = json.load(file)
            for obj in data["objects"]:
                if(obj["id"] == id):
                    for point in obj["coordinates"]:
                        newp = rotatePointAroundOrigin(point, orientation) # rotate
                        newp = (newp[0]+position[0],newp[1]+position[1])   # translate
                        ret.append(newp)
                    break
        if(ret == []):
            #print("no geometry for given ID found! Use default")
            return Geometry.createObject(filepath,Geometry.defaultid,position,orientation)
        #print(ret)
        g = Geometry(ret)
        g.id = id
        return g

    @staticmethod
    def createObjectFromString(json, id, position, orientation):
        ret = []

        data = json
        for obj in data["objects"]:
            if(obj["id"] == id):
                for point in obj["coordinates"]:
                    newp = rotatePointAroundOrigin(point, orientation) # rotate
                    newp = (newp[0]+position[0],newp[1]+position[1])   # translate
                    ret.append(newp)
                break
        if(ret == []):
            #print("no geometry for given ID found! Use default")
            return Geometry.createObjectFromString(json,Geometry.defaultid,position,orientation)
        #print(ret)
        g = Geometry(ret)
        g.id = id
        return g

    @staticmethod
    def createTest():
        return Geometry([(10,10), (20,10), (30,15), (20,20), (10,20)])

    @staticmethod
    def writeGeometriesToFile(geoms):
        ret = "{\"type\": \"FeatureCollection\",\"features\": ["
        for feature in geoms[:-1]:
            ret += feature.toGeoJSON() + ","
        if len(geoms) > 0:
            ret += geoms[-1].toGeoJSON() # last one without trailing comma
        
        ret+= "]}"
        return ret