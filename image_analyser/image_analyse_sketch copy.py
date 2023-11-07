from PIL import Image,ImageDraw
from math import cos,sin,pi
import pygame

image = Image.open("map.png").convert("RGB")


def analyser(pre,current):
    pre = pre[0] + pre[1]*1j
    current = current[0] + current[1]*1j

    scan_radius = 0.1
    arc_length = 0.1

    scanner = [current + (cos() + sin()*1j) for i in range()]







def get_path():
    pre_start = (0,0)
    start = (1,1)
    queue = [(pre_start,start)]
    ready = [pre_start]

    while len(queue) != 0:
        target = queue.pop()
        ready.append(target[1])
        next_point = analyser(target[0],target[1])
        queue = queue + list(map(lambda x:(target[1],x),next_point))
    
    return ready





def prepare(point,r):
    s = [(point[0] + r*math.cos(i*(2*math.pi)/20),point[1] + r*math.sin(i*(2*math.pi)/20)) for i in range(20)]
    s = list(filter(lambda x: 0<x[0]<image.size[0] and 0<x[1]<image.size[1],s))
    s = list(map(lambda x: x if image.getpixel(x) != (255,255,255) else None,s))
    count = 0
    if len(s) == 0:
        return 2
    
    i = 0
    while i<len(s):
        if s[i] == None:
            i += 1
            continue
        j = i
        while  j<len(s) and s[j] != None:
            j += 1
        count += 1
        i = j
    
    if count == 0:
        return 2
    return count

    






run = True
display = pygame.display.set_mode(image.size)
imagg = pygame.image.load("map.png")






while run:
    pygame.time.delay(166)
    display.blit(imagg,(0,0))
  
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
