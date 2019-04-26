import sys, pygame
import geometry
import json

import tuio
tracking = tuio.Tracking()
print "loaded profiles:", tracking.profiles.keys()
print "list functions to access tracked objects:", tracking.get_helpers()

def pygame_init():
    pygame.init()

    size = width, height = 800, 600
    return pygame.display.set_mode(size)



if __name__ == "__main__":
    screen = pygame_init()

    black = 0, 0, 0

    g = geometry.Geometry.fromjson(json.load(open("config.json"))["map_path"])

    print(g.points)

    cam = (0,0)


    while 1:
        keys = []   # reset input
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

        if(keys != [] and keys[pygame.K_ESCAPE]):
            sys.exit()

        if(keys != [] and keys[pygame.K_w]):
            cam = (cam[0],cam[1]+10)
        if(keys != [] and keys[pygame.K_a]):
            cam = (cam[0]+10,cam[1])
        if(keys != [] and keys[pygame.K_s]):
            cam = (cam[0],cam[1]-10)
        if(keys != [] and keys[pygame.K_d]):
            cam = (cam[0]-10,cam[1])

        screen.fill(black)

        pygame.draw.polygon(screen, (255,255,255), [ (x[0]+cam[0],x[1]+cam[1]) for x in g.points], 0 )

        surf = pygame.Surface((24,24))
        surf.fill((255,0,0))
        rect = surf.get_rect()  

        tracking.update()
        for obj in tracking.objects():
            # print(obj.angle)
            rect.center = (obj.xpos*800,obj.ypos*600)           # position of object
            surf.set_colorkey(black)                            # allows transparency while padding during rotate
            rotated = pygame.transform.rotate(surf,obj.angle)   # rotate objects
            rect = rotated.get_rect()                           # re-align (rotation resizes)
            rect.center = (obj.xpos*800,obj.ypos*600)           # re-align
            screen.blit(rotated,rect)                           # draw object
            # pygame.draw.rect(screen,black, (obj.xpos*800-2,obj.ypos*600-2,4,4)) # draw center of object



        pygame.display.flip()