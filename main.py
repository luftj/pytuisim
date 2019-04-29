import sys, pygame
import json

import geometry

import tuio
tracking = tuio.Tracking()
print("loaded profiles:", tracking.profiles.keys())
print("list functions to access tracked objects:", tracking.get_helpers())


screenwidth = 800
screenheight = 600
scale = 1/500

def pygame_init():
    pygame.init()

    size = screenwidth, screenheight
    return pygame.display.set_mode(size)

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
    writeFile("testoutput.json",data)

if __name__ == "__main__":
    screen = pygame_init()

    black = 0, 0, 0

    mapgeoms = geometry.Geometry.fromjson(json.load(open("config.json"))["map_path"])
    h = geometry.Geometry.fromjson("testoutput.json")

    cam = (566300,-5932300)

    while 1:
        keys = []   # reset input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

        if(keys != [] and keys[pygame.K_ESCAPE]):
            sys.exit()

        if(keys != [] and keys[pygame.K_w]):
            cam = (cam[0],cam[1]-10)
        if(keys != [] and keys[pygame.K_a]):
            cam = (cam[0]-10,cam[1])
        if(keys != [] and keys[pygame.K_s]):
            cam = (cam[0],cam[1]+10)
        if(keys != [] and keys[pygame.K_d]):
            cam = (cam[0]+10,cam[1])

        screen.fill(black)
        for mapgeom in mapgeoms:
            screencoords = [ (x[0]-cam[0],x[1]-cam[1]) for x in mapgeom.points]
            pygame.draw.polygon(screen, (255,255,255), screencoords, 0 )

        # debug: putput json
        for gg in h:
            screencoords2 = [ (x[0]-cam[0],x[1]-cam[1]) for x in gg.points]
            pygame.draw.polygon(screen, (0,0,255), screencoords2, 0 )

        surf = pygame.Surface((24,24))
        surf.fill((255,0,0))
        rect = surf.get_rect()  

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



        pygame.display.flip()