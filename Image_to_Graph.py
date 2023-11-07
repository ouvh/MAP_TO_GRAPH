import cv2

import numpy as np
from PIL import Image
from Graph import Vertex, Graph
import pickle


def Build_Graph(image_link) :
    
    def interpolate_line(P):

        X = list(map(lambda t:t[0],P))
        Y = list(map(lambda t:t[1],P))


        n = len(X)
        sum_x = sum(X)
        sum_y = sum(Y)
        sum_xy = sum(x_i * y_i for x_i, y_i in zip(X, Y))
        sum_x_squared = sum(x_i**2 for x_i in X)

        if (n * sum_x_squared - sum_x**2) == 0:
            return 0
        m = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x**2)
        b = (sum_y - m * sum_x) / n

        return m

    
    from PIL import Image
    import cv2,numpy
    import time,pickle,random
    import Graph

    image_file = image_link




    img = Image.open(image_file)
    image = cv2.imread(image_file)
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) 


    for i in range(len(gray)):
        for j in range(len(gray[0])):
            if  0<= gray[i][j] <= 150:
                gray[i][j] = 0
            else:
                gray[i][j] = 1


        


    def is_neighbour(A,B):
        return ((A[1] == B[1]) and (A[0]==B[0]+1 or A[0]==B[0]-1)) or ((A[1] == B[1]+1) and (A[0]==B[0]+1 or A[0]==B[0]-1 or A[0]==B[0])) or ((A[1] == B[1]-1) and (A[0]==B[0]+1 or A[0]==B[0]-1 or A[0]==B[0]))

    def are_neighbour(L1,L2):
        for i in L1:
            for j in L2:
                if is_neighbour(i,j):
                    return True
        return False

    def organize_neighbour(L):
        m =  interpolate_line(L)
        if m > 1:
            return sorted(L,key=lambda p:p[1])
        else:
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
        
        def __hash__(self) -> int:
            return hash(self.children[0])



    class NEIGHBORHOOD:
        def __init__(self) -> None:
            self.generations = list()
            self.frontiere = {}
        
        def copy(self):
            S = NEIGHBORHOOD()
            S.generations = self.generations.copy()
            return S
        

    def skeletonize(neighboor:NEIGHBORHOOD):
        K = []
        for generation in range(0,len(neighboor.generations)-1,10):
            aligned = organize_neighbour(neighboor.generations[generation].children)
            K.append(aligned[len(aligned)//2])
        
        aligned = organize_neighbour(neighboor.generations[-1].children)
        K.append(aligned[len(aligned)//2])
    
        neighbour.generations = K


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

                    new_chidren = list(filter(lambda t:0<=t[0]<img.size[0] and 0<=t[1]<img.size[1] and gray[t[1]][t[0]]==0 and (not ALL_CHILDREN.get(t)) and not new_generation.get(t),[(child[0]-1,child[1]),(child[0]+1,child[1]),(child[0]-1,child[1]-1),(child[0],child[1]-1),(child[0]+1,child[1]-1),(child[0]-1,child[1]+1),(child[0],child[1]+1),(child[0]+1,child[1]+1)]))
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
                    neighbourhood.generations.append(GENERATION(neighbouhoods_derived.pop()))
                

                #check the arrival
                

                ALL_CHILDREN.update(new_generation)




        """
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
            
        """
        print(time.time() - start)

        return neighbouhoods["Arrived"]

    BIJECTION = {}
    MAP = {}

    for i in range(len(gray)):
        for j in range(len(gray[0])):
            if gray[i][j] == 0:
                if not leader_agent.__defaults__[0].get((j,i)):
                    MAP[(j,i)] = leader_agent((j,i))
                    for neighbour in MAP[(j,i)]:
                        for generation in neighbour.generations:
                            for child in generation.children:
                                BIJECTION[child] = generation


    #determine the frontiere of each neighbour


    for i in MAP:
        for neighbour in MAP[i]:
            for child in neighbour.generations[-1].children:
                potential_frontiere =  list(filter(lambda t:0<=t[0]<img.size[0] and 0<=t[1]<img.size[1] and gray[t[1]][t[0]]==0 ,[(child[0]-1,child[1]),(child[0]+1,child[1]),(child[0]-1,child[1]-1),(child[0],child[1]-1),(child[0]+1,child[1]-1),(child[0]-1,child[1]+1),(child[0],child[1]+1),(child[0]+1,child[1]+1)]))
                for point in potential_frontiere:
                    neighbour.frontiere[BIJECTION[point]] = 1
            if neighbour.frontiere.get(neighbour.generations[-1]):
                del neighbour.frontiere[neighbour.generations[-1]]

    # replace each generation with one point
    for i in MAP:
        for neighbour in MAP[i]:
            skeletonize(neighbour)
            



    GRAPH = {}

    for i in MAP:
        for neighbour in MAP[i]:
            if len(neighbour.generations) == 2:
                if not GRAPH.get(neighbour.generations[0]):
                    GRAPH[neighbour.generations[0]] = {neighbour.generations[1]:1}
                else:
                    GRAPH[neighbour.generations[0]].update({neighbour.generations[1]:1})
                
                if not GRAPH.get(neighbour.generations[1]):
                    GRAPH[neighbour.generations[1]] = {neighbour.generations[0]:1}
                else:
                    GRAPH[neighbour.generations[1]].update({neighbour.generations[0]:1})
            
            elif len(neighbour.generations) == 1:
                if not GRAPH.get(neighbour.generations[0]):
                    GRAPH[neighbour.generations[0]] = {}
            
            else:
                if not GRAPH.get(neighbour.generations[0]):
                    GRAPH[neighbour.generations[0]] = {neighbour.generations[1]:1}
                else:
                    GRAPH[neighbour.generations[0]].update({neighbour.generations[1]:1})
                
                if not GRAPH.get(neighbour.generations[-1]):
                    GRAPH[neighbour.generations[-1]] = {neighbour.generations[-2]:1}
                else:
                    GRAPH[neighbour.generations[-1]].update({neighbour.generations[-2]:1})
                    
                for join in range(1,len(neighbour.generations) - 1):
                    if not GRAPH.get(neighbour.generations[join]):
                        GRAPH[neighbour.generations[join]] = {neighbour.generations[join - 1]:1,neighbour.generations[join + 1]:1}
                    else:
                        GRAPH[neighbour.generations[join]].update({neighbour.generations[join - 1]:1,neighbour.generations[join + 1]:1})

            
            
            for frontiere in neighbour.frontiere:
                aligned = organize_neighbour(frontiere.children)
                aligned = aligned[len(aligned)//2]

                GRAPH[neighbour.generations[-1]][aligned] = 1

                if not GRAPH.get(aligned):
                    GRAPH[aligned] = {neighbour.generations[-1]:1}
                else:
                    GRAPH[aligned].update({neighbour.generations[-1]:1})
            
            


    graph = Graph.Graph()

    for i in GRAPH:
        graph.addVertex((i[0],i[1],0))


    for i in GRAPH:
        for j in GRAPH[i]:
            graph.addEdge(Graph.Vertex((i[0],i[1],0)),(j[0],j[1],0))


    return graph




