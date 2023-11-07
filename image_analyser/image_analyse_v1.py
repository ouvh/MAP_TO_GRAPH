from PIL import Image,ImageDraw
import cv2
import pygame
from math import cos,sin,pi
import numpy as np
image = Image.open("map.png").convert("RGB")
drawing_tool = ImageDraw.Draw(image,"RGB")

def get_pixel(z):
    return image.getpixel((z.real,z.imag))


def raycaste(start,vec,threshold) :
    points =[]
    lengths = []
    n = 1000
    ray_step = 0.01
    angle_step = (2*pi)/n

    for k in range(n) :
        i=1
        init_vec= vec
       
        while( 0<(vec+start).real<image.size[0] and 0<(vec+start).imag<image.size[1] and get_pixel(vec+start)!=(255,255,255) ) :
            prev = vec+start
            vec = init_vec*(i*ray_step)
            i+=1
        if i>1:
            points.append(prev)
            lengths.append(np.abs(prev))

        vec = init_vec
        vec *= (cos(angle_step)+sin(angle_step)*1j)


   
    differences = np.diff(lengths)

    significant_change_indices = list(np.where(np.abs(differences) >= threshold)[0])

    return [points[i] for i in range(len(points)) if i in significant_change_indices]
       


class POINT:
    def __init__(self,x,y,previous) -> None:
        self.previous = previous
        self.coor = x + y*1j
        self.direction = 0 + 1j
    
def normalize(v):
    return (v)/abs(v)

def distance(z1,z2):
    return abs(z1 - z2)



def analyser(point:POINT):
    ARC = pi/10   #20 point on a circle of radius 1

    radius_of_scan = 0.1 - 0.4
    rotation_angle =  abs(ARC/radius_of_scan)            #((2*pi*radius_of_scan)/ARC)
    direction =  radius_of_scan * normalize(point.coor - point.previous.coor)

    accurate = 0

    while not accurate:
        radius_of_scan += 1
        rotation_angle = ARC/radius_of_scan
        direction =  radius_of_scan * normalize(point.coor - point.previous.coor)

        

        right_scanner = [(point.coor + (cos(rotation_angle*i) + sin(rotation_angle*i)*1j)*(direction),rotation_angle*i)     for i in range(int(((2*pi*radius_of_scan)/ARC)//2))]
        left_scanner =   [(point.coor + (cos(-1*rotation_angle*i) + sin(-1*rotation_angle*i)*1j)*(direction),rotation_angle*i)    for i in range(int(((2*pi*radius_of_scan)/ARC)//2))]
        
        
        
        right_scanner = list(map(lambda x: x if (0<x[0].real<image.size[0] and 0<x[0].imag<image.size[1] and image.getpixel((x[0].real,x[0].imag)) != (255,255,255) ) else "out",right_scanner))
        left_scanner = list(map(lambda x: x if (0<x[0].real<image.size[0] and 0<x[0].imag<image.size[1] and image.getpixel((x[0].real,x[0].imag)) != (255,255,255) ) else "out",left_scanner))



        right_scanner = list(map(lambda x: x if (type(x)== str) or (distance(x[0],point.previous.coor) > distance(point.coor,point.previous.coor)) else "illegal",right_scanner))
        left_scanner = list(map(lambda x: x if (type(x)== str) or (distance(x[0],point.previous.coor) > distance(point.coor,point.previous.coor)) else "illegal",left_scanner))


        if right_scanner.count("out") +  right_scanner.count("illegal") > 0.75 * len(right_scanner):
            accurate = 1
        if left_scanner.count("out")  + left_scanner.count("illegal")> 0.75 * len(left_scanner):
            accurate = 1
        
    if right_scanner.count("out") +  right_scanner.count("illegal")== len(right_scanner) and left_scanner.count("out")  + left_scanner.count("illegal") == len(left_scanner):
        return ("end",)

    if right_scanner.count("illegal") + left_scanner.count("illegal") >= right_scanner.count("out") + left_scanner.count("out"):
        #return (right_scanner,left_scanner,"intersection")
        return (point,"intersection")
    
    else:
        return (right_scanner,left_scanner,"normal")


def chooser(decision):
    if decision[0]=="end":
        return [tuple(),[]]
 
    
    if decision[1] == "intersection":
        edges = raycaste(decision[0].coor,normalize(decision[0].coor - decision[0].previous.coor),1)
        center = sum(edges) / len(edges)
        points = [(edges[i] + edges[i+1])/2 for i in range(len(edges) - 1)]
        return [(center.real,center.imag) , list(map(lambda x:(x.real,x.imag),points))]
    else:
        ll = list(filter(lambda y: y!= "illegal" and y!= "out",decision[0])) + list(filter(lambda y: y!= "illegal" and y!= "out",decision[1]))
        average_angle = sum(list(map(lambda x:x[1],ll))) / len(ll)
        resu = min(ll,key=lambda x: abs(average_angle - x[1]))[0]
        return [tuple(),[(resu.real,resu.imag)] ]




    


        



def get_path():
    pre_start = (390, 204)

    start = (388, 200)
    queue = [(pre_start,start)]
    ready = [pre_start]
    cou = 0
    while len(queue) != 0 and cou <200:
        print(cou)
        target = queue.pop()
        ready.append(target[1])
        next_points =  chooser(analyser(POINT(target[1][0],target[1][1],POINT(target[0][0],target[0][1],None))))
        if len(next_points[0]) != 0:
            ready.append(next_points[0])
        eee = list(map(lambda x:(target[1],x),next_points[1]))
        for i in eee:
            for j in ready:
                if ( (i[1][0] - j[0])**2 + (i[1][1] - j[1])**2 )**0.5 < 2:
                    break
            else:
                queue.append(i)
        cou += 1
    
    return ready
    






L = get_path()
print(L)

run = True
display = pygame.display.set_mode(image.size)
imagg = pygame.image.load("map.png")






while run:
    pygame.time.delay(166)
    display.blit(imagg,(0,0))
    

    for i in L:
       pygame.draw.circle(display,"red",i,2)

    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())



