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
config = json.load(open("config.json"))
putputfilepath = "data/conversion.geojson"

class FileObserver(object):
    def __init__(self,file):
        self._cached_stamp = 0
        self.filename = file

    def ook(self): # poll file for changes. returns True, if file was changed
        try:
            stamp = os.stat(self.filename).st_mtime
        except EnvironmentError:
            print("no file to observe")
            return False
        if stamp != self._cached_stamp:
            self._cached_stamp = stamp
            return True
        return False

def pygame_init():
    size = screenwidth, screenheight
    return pygame.display.set_mode(size, pygame.DOUBLEBUF, depth=32)

def init_tuio(args):
    tracking = tuio.Tracking(args.ip,args.port)
    print("loaded profiles:", tracking.profiles.keys())
    print("list functions to access tracked objects:", tracking.get_helpers())
    return tracking

def writeFile(filepath, data):
    f= open(filepath,"w+")
    f.write(data)

def saveObjects(trackingobjects, cam):
    ret = []
    for obj in trackingobjects():
        center = (obj.xpos*screenwidth+cam[0],-(obj.ypos*screenheight+cam[1])) # position of object in world coords
        geom = geometry.Geometry.createObject("geometry.json", obj.id, center, -obj.angle)
        if geom:
            ret.append(geom)

    data = (geometry.Geometry.writeGeometriesToFile(ret))

    # debug
    #writeFile("data/output.geojson",data)

    # output
    writeFile(os.path.dirname(os.path.abspath(noisemap.__file__))+"\\input_geojson\\design\\buildings" + "\\buildings.json",data)

from thread import start_new_thread

def noisethread():
    shapefile = noisemap.main()
    convert.convert(shapefile, putputfilepath)

def makeSomeNoise():
    start_new_thread(noisethread,())


def handle_object(obj, obj_surface):
    rect = obj_surface.get_rect()  
    rect.center = (obj.xpos*screenwidth,obj.ypos*screenheight)           # position of object
    obj_surface.set_colorkey(black)                            # allows transparency while padding during rotate
    rotated = pygame.transform.rotate(obj_surface,-obj.angle)   # rotate objects
    rect = rotated.get_rect()                           # re-align (rotation resizes)
    rect.center = (obj.xpos*screenwidth,obj.ypos*screenheight)           # re-align
    screen.blit(rotated,rect)   

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert shape to geojson")
    parser.add_argument('--ip', type=str, default=config["tuio_host"],help="the IP address of the tuio host. If omitted, read from config.json")
    parser.add_argument('--port', type=int, default=int(config["tuio_port"]),help="the port of the tuio host. If omitted, read from config.json")
    args = parser.parse_args()

    tracking = init_tuio(args)
    
    screen = pygame_init()
    isFullscreen = False

    black = 0, 0, 0

    mapgeoms = geometry.Geometry.fromjson(config["map_path"])
    noise_polys = geometry.Geometry.fromjson(putputfilepath)

    fo = FileObserver(putputfilepath)

    cam = (566300,-5932300)
    camspeed = 50

    while 1:
        if fo.ook():
            print("noise changed")
            new_noise_polys = geometry.Geometry.fromjson(putputfilepath) # reload noise output geometry, when file changed
            if not new_noise_polys == []:
                noise_polys = new_noise_polys

        screen.fill(black)
        # draw background map
        for mapgeom in mapgeoms:
            screencoords = [ (x[0]-cam[0],x[1]-cam[1]) for x in mapgeom.points]
            pygame.draw.polygon(screen, (255,255,255), screencoords, 0 )

        noise_surface = pygame.Surface((screenwidth, screenheight), pygame.SRCALPHA) # rendertarget for noise output with transpaency
        noise_surface.fill((0,0,0,0))         
        # draw noise
        for noise_poly in noise_polys:
            screencoords2 = [ (x[0]-cam[0],x[1]-cam[1]) for x in noise_poly.points]
            col = config["colourkey"][str(noise_poly.properties["IDISO"])]
            pygame.draw.polygon(noise_surface, col, screencoords2, 0 )
        screen.blit(noise_surface, (0,0))  


        obj_surface = pygame.Surface((24,24)) # rendertarget for objects
        obj_surface.fill((255,0,0))
        rect = obj_surface.get_rect()  

        # handle objects
        tracking.update()
        for obj in tracking.objects():
            handle_object(obj, obj_surface)
            # pygame.draw.rect(screen,black, (obj.xpos*screenwidth-2,obj.ypos*screenheight-2,4,4)) # draw center of object

        # Keyboard input
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