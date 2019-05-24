import sys, pygame
import json
import os
import argparse
from thread import start_new_thread

import tuio
from CSL_Hamburg_Noise import noisemap
import geometry
import convert

screenwidth = 800
screenheight = 800
fullscreen_width = 0
fullscreen_height = 0
config = json.load(open("config.json"))
putputfilepath = "data/conversion.geojson"
scale = config["pxpm"]

file = open("geometry.json")
geometriesjson = json.load(file)

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
    pygame.display.init()
    global fullscreen_width
    fullscreen_width = pygame.display.Info().current_w
    global fullscreen_height
    fullscreen_height = pygame.display.Info().current_h
    
    size = screenwidth, screenheight
    return pygame.display.set_mode(size)

def init_tuio(args):
    tracking = tuio.Tracking(args.ip,args.port)
    print("loaded profiles:", tracking.profiles.keys())
    print("list functions to access tracked objects:", tracking.get_helpers())
    return tracking

def writeFile(filepath, data):
    f= open(filepath,"w+")
    f.write(data)

def noisethread():
    shapefile = noisemap.main()
    convert.convert(shapefile, putputfilepath)

def makeSomeNoise():
    start_new_thread(noisethread,())

def drawObjects(trackingobjects, cam, screen):
    objectgeoms = makeObjects(trackingobjects,cam)
    for geom in objectgeoms:
        screencoords = [ map_to_screen(x[0],-x[1],cam) for x in geom.points]
        pygame.draw.polygon(screen, (255,0,0), screencoords, 0 )

def makeObjects(trackingobjects, cam):
    ret = []
    for obj in trackingobjects:
        # obj.xpos,ypos is in [0,1]
        center = screen_to_map(obj.xpos, obj.ypos, cam) # position of object in world coords
        #geom = geometry.Geometry.createObject("geometry.json", obj.id, center, -obj.angle)
        geom = geometry.Geometry.createObjectFromString(geometriesjson, obj.id, center, -obj.angle)
        if geom:
            ret.append(geom)
    return ret

def saveObjects(trackingobjects, cam):
    data = (geometry.Geometry.writeGeometriesToFile(makeObjects(trackingobjects, cam)))

    # debug
    #writeFile("data/output.geojson",data)

    # output
    writeFile(os.path.dirname(os.path.abspath(noisemap.__file__))+"\\input_geojson\\design\\buildings" + "\\buildings.json",data)

def handle_object(obj, obj_surface):
    screensize = pygame.display.get_surface().get_size()
    rect = obj_surface.get_rect()  
    rect.center = (obj.xpos*screensize[0], obj.ypos*screensize[1])   # position of object
    obj_surface.set_colorkey(black)                                 # allows transparency while padding during rotate
    rotated = pygame.transform.rotate(obj_surface, -obj.angle)       # rotate objects
    rect = rotated.get_rect()                                       # re-align (rotation resizes)
    rect.center = (obj.xpos*screensize[0], obj.ypos*screensize[1])   # re-align
    pygame.display.get_surface().blit(rotated, rect)   

def map_to_screen(x, y, cam):
    sc = scale # depends on ppi of display!
    return ((x-cam[0])*sc,(y-cam[1])*sc)

def screen_to_map(x, y, cam):
    w,h = pygame.display.get_surface().get_size()
    sc = 1.0/scale # depends on ppi of display!
    return ((x * w * sc + cam[0]), -(y * h * sc + cam[1]))

def draw_noise(noise_surface, noise_polys):
    noise_surface.fill((0,0,0,0))
    for noise_poly in noise_polys:
        screencoords2 = [ map_to_screen(x[0], x[1], cam) for x in noise_poly.points]
        if len(screencoords2) <= 2:
            continue 
        col = config["colourkey"][str(noise_poly.properties["IDISO"])]
        pygame.draw.polygon(noise_surface, col, screencoords2, 0 )

def draw_map(surface, mapgeoms):
    surface.fill((0,0,0))
    for mapgeom in mapgeoms:
        screencoords = [ map_to_screen(x[0],x[1],cam) for x in mapgeom.points]
        pygame.draw.polygon(surface, (255,255,255), screencoords, 0 )

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="convert shape to geojson")
    parser.add_argument('--ip', type=str, default=config["tuio_host"],help="the IP address of the tuio host. If omitted, read from config.json")
    parser.add_argument('--port', type=int, default=int(config["tuio_port"]),help="the port of the tuio host. If omitted, read from config.json")
    args = parser.parse_args()

    # initialise
    tracking = init_tuio(args)
    screen = pygame_init()
    isFullscreen = False
    black = 0, 0, 0

    # load geo files
    mapgeoms = geometry.Geometry.fromjson(config["map_path"])
    noise_polys = geometry.Geometry.fromjson(putputfilepath)
    if not noise_polys == []:
        fo = FileObserver(putputfilepath)

    cam = config["mapcenter"]
    camspeed = 70

    scaleimg = pygame.image.load("scale_100m_325px.png")
    scaleimg = pygame.transform.scale(scaleimg,(int(100*config["pxpm"]),scaleimg.get_size()[1]))

    map_surface = pygame.Surface(screen.get_size()) # rendertarget for noise output with transpaency
    map_surface.fill(black)
    noise_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA) # rendertarget for noise output with transpaency
    noise_surface.fill((0,0,0,0))
    obj_surface = pygame.Surface((24,24)) # rendertarget for objects
    obj_surface.fill((255,0,0))
    # draw background map
    draw_map(map_surface,mapgeoms)
    # draw noise
    draw_noise(noise_surface, noise_polys)
    screen.blit(noise_surface, (0,0))
    redraw = False

    fo = FileObserver(putputfilepath)


    while 1:
        if fo.ook():
            print("noise changed")
            new_noise_polys = geometry.Geometry.fromjson(putputfilepath) # reload noise output geometry, when file changed
            if not new_noise_polys == []:
                noise_polys = new_noise_polys
                redraw = True
                    
  
        # update screen
        screen.fill(black)
        screen.blit(map_surface, (0,0))
        screen.blit(noise_surface, (0,0))
        if redraw:
            # draw background map
            draw_map(map_surface,mapgeoms)
            # draw noise
            draw_noise(noise_surface, noise_polys)
            redraw = False

        # handle objects
        tracking.update()
        drawObjects(tracking.objects(), cam, screen)

        # draw legend
        screen.blit(scaleimg, (0,screen.get_size()[1]-40))
        

        # Keyboard input
        keys = []   # reset input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

        if(keys != [] and keys[pygame.K_ESCAPE]):
            sys.exit()

        # cam navigation
        if(keys != [] and keys[pygame.K_w]):
            cam = (cam[0], cam[1]-camspeed)
            redraw = True
        if(keys != [] and keys[pygame.K_a]):
            cam = (cam[0]-camspeed, cam[1])
            redraw = True
        if(keys != [] and keys[pygame.K_s]):
            cam = (cam[0], cam[1]+camspeed)
            redraw = True
        if(keys != [] and keys[pygame.K_d]):
            cam = (cam[0]+camspeed, cam[1])
            redraw = True

        if(keys != [] and keys[pygame.K_RETURN]):
            saveObjects(tracking.objects(),cam)
            makeSomeNoise()

        # toggle fullscreen mode
        if(keys != [] and keys[pygame.K_SPACE]):
            if not isFullscreen:
                screen = pygame.display.set_mode([fullscreen_width,fullscreen_height],flags=pygame.FULLSCREEN)
            else:
                screen = pygame.display.set_mode([screenwidth,screenheight])
            isFullscreen = not isFullscreen

            map_surface = pygame.Surface(screen.get_size()) # rendertarget for noise output with transpaency
            noise_surface = pygame.Surface(screen.get_size(), pygame.SRCALPHA) # rendertarget for noise output with transpaency
            redraw = True

        if(keys != [] and keys[pygame.K_h]): # debug output
            print(fullscreen_width, fullscreen_height)
            print(pygame.display.Info())
            print(pygame.display.get_surface().get_size())

        pygame.display.flip()