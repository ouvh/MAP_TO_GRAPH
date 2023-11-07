import pygame 
from PIL import Image
import cv2,numpy
import time,pickle

image_file = "map2.png"
imagee = pygame.image.load(image_file)

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
        s.append(l[i:j])
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

def normale(u):
    return (-u[1],u[0])

def produit(a,x):
    return (a*x[0],a*x[1])


img = Image.open(image_file)
image = cv2.imread(image_file)
image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) 
gradient_x = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=5)
gradient_y = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=5)

MAP = [[[gradient_x[i][j]/norme([gradient_x[i][j],gradient_y[i][j]]),gradient_y[i][j]/norme([gradient_x[i][j],gradient_y[i][j]]),0] if norme([gradient_x[i][j],gradient_y[i][j]]) > 9000   else [0,0,0]for j in range(len(gradient_x[0]))] for i in range(len(gradient_x))]

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

def organize_neighbour(L):
    return sorted(L,key=lambda p:p[0])

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
            return list(map(lambda i: organize_neighbour(i),new))
        
        assemble = new
        new = []





class GENERATION:
    def __init__(self,children:list[tuple]) -> None:
        self.children = children
    

class NEIGHBORHOOD:
    def __init__(self) -> None:
        self.generations = list()
        self.end = None
    
    def copy(self):
        S = NEIGHBORHOOD()
        S.generations = self.generations.copy()
        return S




for i in intersections:
    gray[i[1]][i[0]] = 0



def skeletonize(neighboor:NEIGHBORHOOD):
    K = []
    if len(neighboor.generations)>=2:
        for generation in range(0,len(neighboor.generations) - 1,10):
            aligned = organize_neighbour(neighboor.generations[generation].children)
            K.append(aligned[len(aligned)//2])
        
        if neighboor.end== None:
            aligned = organize_neighbour(neighboor.generations[-1].children)
            K.append( aligned[len(aligned)//2])

        else:
            K.append(neighboor.end)


    else:
        
        if  neighboor.end== None:
            aligned = organize_neighbour(neighboor.generations[0].children)
            K.append( aligned[len(aligned)//2])
        else:
            K.append(neighboor.end)


    return K


display = pygame.display.set_mode(img.size)


def leader_agent(point,ALL_CHILDREN={}):
    start = time.time()
    ALL_CHILDREN[point] = 1
    starting_neibghour = NEIGHBORHOOD()
    first_generation = GENERATION([])
    first_generation.children.append(point)
    starting_neibghour.generations.append(first_generation)
    
    neighbouhoods = {"Arrived":list(),"On going":[starting_neibghour]}

    while neighbouhoods["On going"]:


        for neighbourhood in neighbouhoods["On going"]:
            new_generation = {}

            # Getting the newest generation
            for child in neighbourhood.generations[-1].children:

                new_chidren = list(filter(lambda t:0<=t[0]<img.size[0] and 0<=t[1]<img.size[1] and 0<=gray[t[1]][t[0]]<155 and (not ALL_CHILDREN.get(t)) and not new_generation.get(t),[(child[0]-1,child[1]),(child[0]+1,child[1]),(child[0]-1,child[1]-1),(child[0],child[1]-1),(child[0]+1,child[1]-1),(child[0]-1,child[1]+1),(child[0],child[1]+1),(child[0]+1,child[1]+1)]))
                new_generation.update(dict().fromkeys(new_chidren,1))
        
            
            #Check if there are any derived children
            neighbouhoods_derived = assemble(list(new_generation.keys()))
            if len(neighbouhoods_derived) > 1:
                for new_neighboorhood in neighbouhoods_derived[:len(neighbouhoods_derived)-1]:
                    temp = neighbourhood.copy()
                    temp.generations.append(GENERATION(new_neighboorhood))
                    neighbouhoods["On going"].append(temp)
                neighbourhood.generations.append(GENERATION(neighbouhoods_derived[-1]))

            elif len(neighbouhoods_derived) == 0:
                neighbouhoods["Arrived"].append(neighbourhood)
                neighbouhoods["On going"].remove(neighbourhood)
                continue


            else:
                if  (numpy.std(list(map(lambda x:x[0],neighbouhoods_derived[0])))**2 + numpy.std(list(map(lambda x:x[1],neighbouhoods_derived[0])))**2)**0.5>3:
                    temp = organize_neighbour(neighbouhoods_derived[0])
                    temp1 =  neighbourhood.copy()
                    temp1.generations.append(GENERATION(temp[:len(temp)//2]))
                    neighbourhood.generations.append(GENERATION(temp[len(temp)//2:]))
                    neighbouhoods["On going"].append(temp1)



                else:
                    neighbourhood.generations.append(GENERATION(neighbouhoods_derived.pop()))
            

            #check the arrival
            
            for child in neighbourhood.generations[-1].children:
                if intersections.get(child) or graph.get(child):
                    neighbourhood.end = child
                    neighbouhoods["Arrived"].append(neighbourhood)
                    neighbouhoods["On going"].remove(neighbourhood)
                    break


            ALL_CHILDREN.update(new_generation)


    



    skeletons = list(map(lambda x:skeletonize(x),neighbouhoods["Arrived"]))

    Graph = {}

    for skeleton in skeletons:
        if len(skeleton) == 2:
            Graph[skeleton[0]] = {skeleton[1]}
            Graph[skeleton[1]] = {skeleton[0]}
        elif len(skeleton) == 1:
            Graph[skeleton[0]] = {}
        else:
            Graph[skeleton[0]] = {skeleton[1]}
            Graph[skeleton[-1]] = {skeleton[-2]}
            for join in range(1,len(skeleton)-1):
                Graph[skeleton[join]] = {skeleton[join+1],skeleton[join-1]}
    
    print(time.time() - start)

    for nei in neighbouhoods["Arrived"]:
        for gene in nei.generations:
            for i in gene.children:
                pygame.draw.circle(display,"red",i,1)
    pygame.display.flip()
    return Graph



         





 




graph = dict(map(lambda x: (x,{}),intersections))

display.blit(imagee,(0,0))

for i in intersections:
    new_update = leader_agent(i)
    graph.update(new_update)

print(len(graph))

display = pygame.display.set_mode(img.size)
run = True

with open("GGG.txt","wb") as file:
    pickle.dump(graph,file)

display.blit(imagee,(0,0))
for x in graph:
    pygame.draw.circle(display,"red",x,1)
    for y in graph[x]:
        pygame.draw.line(display,"green",x,y,1)
pygame.display.flip()



while run:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            break
