from PIL import Image,ImageDraw
import math
import pygame
import random
image = Image.open("map.png").convert("RGB")
rayon = 2


def distance(a,b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def organise(l):
    if not l:
        return []
    
    s = []
    i = 0
    while i<len(l):
        if l[i] == None:
            i += 1
            continue
        j = i
        while  j<len(l) and l[j] != None:
            j += 1
        s.append(l[i:j+1])
        i = j

    
    for li in s:
        if len(li) > 10:
            s.append(li[:len(li)//2])
            s.append(li[len(li)//2:])

    s = list(map(lambda x:x[len(x)//2],s))
    return s 





def analyse(previous,r):
    l = [(r[0] + rayon*math.cos(i*(2*math.pi)/20),r[1] + rayon*math.sin(i*(2*math.pi)/20)) for i in range(20)]
    l = list(filter(lambda x: 0<x[0]<image.size[0] and 0<x[1]<image.size[1],l))
    l = list(map(lambda x: x if image.getpixel(x) != (255,255,255) else None,l))
    l = list(filter(lambda x:x if x!= None and distance(x,previous) > distance(r,previous) else None,l))
    return l

previous = (311, 260)
r = (309, 260)

L = []
C = [(previous,r)]
count = 0
while C != [] and count <1000:
    count += 1
    L.append(C[-1][1])
    H = list(map(lambda x: (C[-1][1],x),organise(analyse(*C[-1]))))
    C.pop()
    C = C + H
run = True
display = pygame.display.set_mode(image.size)
imagg = pygame.image.load("map.png")


print(count)





while run:
    pygame.time.delay(166)
    display.blit(imagg,(0,0))
    pygame.draw.circle(display,"red",r,2)
    pygame.draw.circle(display,"red",previous,2)

    for i in L:
       pygame.draw.circle(display,"red",i,1)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
