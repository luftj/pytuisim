import sys, pygame
import json
import os
import argparse

import tuio
from CSL_Hamburg_Noise import noisemap
import geometry
import convert

screenwidth = 1000
screenheight = 800
scale = 1/500

def pygame_init():
    size = screenwidth, screenheight
    return pygame.display.set_mode(size, pygame.DOUBLEBUF, depth=32)

def writeFile(filepath, data):
    f= open(filepath,"w+")
    f.write(data)

def saveObjects(trackingobjects,cam):
    ret = []
    for obj in trackingobjects():
        center = (obj.xpos*screenwidth+cam[0],-(obj.ypos*screenheight+cam[1])) # position of object in world coords
        geom = geometry.Geometry.createObject("geometry.json", obj.id, center, obj.angle)
        if geom:
            ret.append(geom)

    data = (geometry.Geometry.writeGeometriesToFile(ret))

    # debug
    #writeFile("output.json",data)

    # output
    writeFile(os.path.dirname(os.path.abspath(noisemap.__file__))+"\\input_geojson\\design\\buildings" + "\\buildings.json",data)

def makeSomeNoise():
    shapefile = noisemap.main()
    convert.convert(shapefile,"conversion.geojson")

class FileObserver(object):
    def __init__(self,file):
        self._cached_stamp = 0
        self.filename = file

    def ook(self):
        try:
            stamp = os.stat(self.filename).st_mtime
        except EnvironmentError:
            print("no file to observe")
            return False
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            return True
        return False

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert shape to geojson")
    parser.add_argument('--ip',type=str, default=json.load(open("config.json"))["tuio_host"],help="the IP address of the tuio host.")
    parser.add_argument('--port',type=int, default=int(json.load(open("config.json"))["tuio_port"]))
    args = parser.parse_args()
    tracking = tuio.Tracking(args.ip,args.port)
    print("loaded profiles:", tracking.profiles.keys())
    print("list functions to access tracked objects:", tracking.get_helpers())
    
    screen = pygame_init()
    isFullscreen = False

    black = 0, 0, 0

    mapgeoms = geometry.Geometry.fromjson(json.load(open("config.json"))["map_path"])
    h = geometry.Geometry.fromjson("conversion.geojson")

    fo = FileObserver("conversion.geojson")

    cam = (566300,-5932300)
    camspeed = 50

    while 1:
        if fo.ook():
            print("noise changed")
            h = geometry.Geometry.fromjson("conversion.geojson") # reload noise output geometry, when file changed

        keys = []   # reset input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

        if(keys != [] and keys[pygame.K_ESCAPE]):
            sys.exit()


        if(keys != [] and keys[pygame.K_w]):
            cam = (cam[0],cam[1]-camspeed)
        if(keys != [] and keys[pygame.K_a]):
            cam = (cam[0]-camspeed,cam[1])
        if(keys != [] and keys[pygame.K_s]):
            cam = (cam[0],cam[1]+camspeed)
        if(keys != [] and keys[pygame.K_d]):
            cam = (cam[0]+camspeed,cam[1])

        screen.fill(black)
        for mapgeom in mapgeoms:
            screencoords = [ (x[0]-cam[0],x[1]-cam[1]) for x in mapgeom.points]
            pygame.draw.polygon(screen, (255,255,255), screencoords, 0 )


        noisecolourdict = {
            0:(140,255,  0,128), # <45 dB(A)
            1:(225,255,186,128), # 45-50
            2:(245,255,101,128), # 50-55
            3:(219,254,  0,128), # 55-60
            4:(253,223,116,128), # 60-65
            5:(229,162,  0,128), # 65-70
            6:(255,  0,  0,128), # 70-75
            7:(171,  0,  0,128)  # >75 dB(A)
        }

        noisesurf= pygame.Surface((screenwidth,screenheight), pygame.SRCALPHA)
        noisesurf.fill((0,0,0,0))         
        # plot noise
        for gg in h:
            screencoords2 = [ (x[0]-cam[0],x[1]-cam[1]) for x in gg.points]
            pygame.draw.polygon(noisesurf, noisecolourdict[gg.properties["IDISO"]], screencoords2, 0 )
        screen.blit(noisesurf, (0,0))  

        surf = pygame.Surface((24,24))
        surf.fill((255,0,0))
        rect = surf.get_rect()  

        # handle objects
        tracking.update()
        for obj in tracking.objects():
            # print(obj.angle)
            rect.center = (obj.xpos*screenwidth,obj.ypos*screenheight)           # position of object
            surf.set_colorkey(black)                            # allows transparency while padding during rotate
            rotated = pygame.transform.rotate(surf,obj.angle)   # rotate objects
            rect = rotated.get_rect()                           # re-align (rotation resizes)
            rect.center = (obj.xpos*screenwidth,obj.ypos*screenheight)           # re-align
            screen.blit(rotated,rect)                           # draw object
            # pygame.draw.rect(screen,black, (obj.xpos*screenwidth-2,obj.ypos*screenheight-2,4,4)) # draw center of object

        
        if(keys != [] and keys[pygame.K_RETURN]):
            saveObjects(tracking.objects,cam)
            makeSomeNoise()

        if(keys != [] and keys[pygame.K_SPACE]):
            if not isFullscreen:
                screen = pygame.display.set_mode([0,0],flags=pygame.FULLSCREEN|pygame.HWSURFACE, depth=32)
            else:
                screen = pygame.display.set_mode([800,600],flags=pygame.FULLSCREEN,depth=32)
            isFullscreen = not isFullscreen

        pygame.display.flip()