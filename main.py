import sys, pygame
import geometry


def pygame_init():
    pygame.init()

    size = width, height = 800, 600
    return pygame.display.set_mode(size)


if __name__ == "__main__":
    screen = pygame_init()

    black = 0, 0, 0

    g = geometry.Geometry.fromjson("SiedlungsflaechenGrasbrook.json")

    print(g.points)

    cam = (0,0)

    while 1:
        keys = []
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                keys = pygame.key.get_pressed()

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


        pygame.display.flip()