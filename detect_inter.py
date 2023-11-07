import pygame 
from PIL import Image
import cv2,numpy
import time
imagee = pygame.image.load("map2.png")

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

    s = list(map(lambda x:x[len(x)//2],s))
    return s 

def norme(e):
    return ( (e[0])**2 + (e[1])**2 )**0.5

def vector(A,B):
    dis = distance(A,B)
    return ((B[0]-A[0])/dis,(B[1]-A[1])/dis)

def distance(x,y):
    return ((x[0] - y[0])**2 + (x[1] - y[1])**2)**0.5

def produit_scalaire(x,y):
    return x[0]*y[0] + x[1]*y[1]

def somme(x,y):
    return (x[0]+y[0],x[1]+y[1])

def somme_int(x,y):
    return (int(x[0]+y[0]),int(x[1]+y[1]))

def normale(x):
    return (-x[1],x[0])

def produit(a,x):
    return (a*x[0],a*x[1])

img = Image.open("map2.png")

image = cv2.imread('map2.png')
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

def find_closest(point,direction):
    children = {}
    r = {1:[],0:[]}
    old_generation = {point:1}
    new_generation = {}
    first_black = None
    first_white = None
    swap = False
    while True:
        for child in old_generation:
            new_childs = dict(map(lambda x: (x,1),list(filter(lambda t:not children.get(t) and not new_generation.get(t) and not old_generation.get(t),[somme_int(child,direction),somme_int(child,produit(-1,child))]))))
            new_generation.update(new_childs)

        for child in new_generation:
            r[gray[child[1]][child[0]]//150].append(child)

        if not swap:
            if  r[0]:
                r[0].sort(key=lambda x:distance(x,point))
                first_black =  r[0][0]
                swap = True
                r = {1:[],0:[]}
                children.update(old_generation)
                old_generation = {first_black:1}
                new_generation = {}
            else:
                r = {1:[],0:[]}
                children.update(old_generation)
                old_generation = new_generation
                new_generation = {}
        else:
            if  r[1]:
                r[1].sort(key=lambda x:distance(x,point))
                first_white =  r[1][0]
                break
            else:
                r = {1:[],0:[]}
                children.update(old_generation)
                old_generation = new_generation
                new_generation = {}

    return somme_int(produit(0.5,first_white),produit(0.5,first_black))

def skeletonizer(point1,point2):
    star = time.time()
    old_sections = [[point1,point2,0]]
    new_sections = []
    while old_sections:
        for section in old_sections:
            center = somme_int(produit(0.5,section[0]),produit(0.5,section[1]))
            if gray[center[1]][center[0]] > 150:
                join = find_closest(center,normale(vector(section[0],section[1])))
                new_sections.append([section[0],join,0])
                new_sections.append([join,section[1],0])
            else:
                if not section[2]:
                    new_sections.append([section[0],center,1])
                    new_sections.append([center,section[1],1])
        if new_sections:
            old_sections = new_sections
            new_sections = []
        else:
            break
    

    result = dict()
    joins = sum(old_sections,start=[])
    result[joins[0]] = [joins[1]]
    result[joins[-1]] = [joins[-2]]
    for i in range(1,len(joins)-1):
        result[joins[i]] = [joins[i-1],joins[i+1]]
    

    print(time.time()-star)
    return result
        


gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)

MAP = [[[gradient_x[i][j]/norme([gradient_x[i][j],gradient_y[i][j]]),gradient_y[i][j]/norme([gradient_x[i][j],gradient_y[i][j]]),0] if norme([gradient_x[i][j],gradient_y[i][j]]) > 10000 else [0,0,0]for j in range(len(gradient_x[0]))] for i in range(len(gradient_x))]

for y in range(img.size[1]):
    for x in range(img.size[0]):
        if norme(MAP[y][x]) !=0:
            neighbour = list(filter(lambda t:0<=t[0]<img.size[0] and 0<=t[1]<img.size[1] and norme(MAP[t[1]][t[0]]) != 0,[(x-1,y),(x+1,y),(x-1,y-1),(x,y-1),(x+1,y-1),(x-1,y+1),(x,y+1),(x+1,y+1)]))
            neighbour = list(map(lambda o:produit_scalaire(MAP[o[1]][o[0]],MAP[y][x]),neighbour))

            MAP[y][x][2] = 10 * numpy.std(neighbour)
            

intersections = {}
for y in range(img.size[1]):
    for x in range(img.size[0]):
        if MAP[y][x][2]>0.1:
            intersections[(x,y)] = 1

for point in organise(list(map(lambda x:None if gray[x[1]][x[0]]>150 else x,[(i,0) for i in range(img.size[0])]))):
    intersections[point] = 1
for point in organise(list(map(lambda x:None if gray[x[1]][x[0]]>150 else x,[(i,img.size[1] - 1) for i in range(img.size[0])]))):
    intersections[point] = 1
for point in organise(list(map(lambda x:None if gray[x[1]][x[0]]>150 else x,[(0,i) for i in range(img.size[1])]))):
    intersections[point] = 1
for point in organise(list(map(lambda x:None if gray[x[1]][x[0]]>150 else x,[(img.size[0]-1,i) for i in range(img.size[1])]))):
    intersections[point] = 1

def is_neighbour(A,B):
    return ((A[1] == B[1]) and (A[0]==B[0]+1 or A[0]==B[0]-1)) or ((A[1] == B[1]+1) and (A[0]==B[0]+1 or A[0]==B[0]-1 or A[0]==B[0])) or ((A[1] == B[1]-1) and (A[0]==B[0]+1 or A[0]==B[0]-1 or A[0]==B[0]))

def are_neighbour(L1,L2):
    for i in L1:
        for j in L2:
            if is_neighbour(i,j):
                return True
    return False

def assemble(L):
    assemble = list(map(lambda x:[x],L))
    new = []
    arranged = 0
    while not arranged:
        arranged = 1
        while assemble:
            for j in range(len(assemble)-1):
                if are_neighbour(assemble[-1],assemble[j]):
                    arranged = 0
                    new.append(assemble[-1] + assemble[j])
                    assemble.pop()
                    assemble.pop(j)
                    break
            else:
                new.append(assemble[-1])
                assemble.pop()
        if arranged == 1:
            return new
        
        assemble = new
        new = []
    

def agent_parcoureur(point,children={}):
    start = time.time()
    Result = []
    children[point] = 1
    old_chidren  = [point]
    new_children = {}
    next = []
    while  old_chidren:
        for POINT in old_chidren:
            new_generation =  list(filter(lambda t:0<=t[0]<img.size[0] and 0<=t[1]<img.size[1] and 0<=gray[t[1]][t[0]]<155 and not children.get(t) and not new_children.get(t),[(POINT[0]-1,POINT[1]),(POINT[0]+1,POINT[1]),(POINT[0]-1,POINT[1]-1),(POINT[0],POINT[1]-1),(POINT[0]+1,POINT[1]-1),(POINT[0]-1,POINT[1]+1),(POINT[0],POINT[1]+1),(POINT[0]+1,POINT[1]+1)]))
            new_children.update(dict().fromkeys(new_generation,1))

        for neighborhood in assemble(list(new_children.keys())):
            for child in neighborhood:
                if intersections.get(child):
                    Result.append(child)
                    break
            else:
                next.extend(neighborhood)
        
        children.update(dict().fromkeys(next,1))
        old_chidren = next
        next = []
        new_children = {}

    print(time.time() - start)
    return Result

#old algorithm that uses direction to find potential neighbour
"""
for point in intersections:
    closest = [(o,distance(o,point)) for o in intersections if o != point]
    closest.sort(key=lambda t:t[1])
    start = time.time()

    for k in closest:


        v = vector(point,k[0])

        for p in relations[point]: 
            PP = produit_scalaire(vector(point,p),v)
            if  PP > 0.5:
                break
        else:
            relations[point][k[0]] = 0
    
"""

relations = dict(map(lambda x:(x,agent_parcoureur(x)),intersections))

graph = {}

for point in relations:
    for adjacent in relations[point]:
        graph.update(skeletonizer(point,adjacent))

    
display = pygame.display.set_mode(img.size)
run = True
display.blit(imagee,(0,0))
for x in graph:
    pygame.draw.circle(display,"red",x,5)
    for y in graph[x]:
        pygame.draw.line(display,"green",x,y,2)
  


pygame.display.flip()
while run:
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
