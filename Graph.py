import math

class Vertex(tuple):
    def __hash__(self):
        return hash((self[0],self[1],self[2]))

class Graph(dict):



    def addVertex(self,*args):
        if (len(args)==1) :
            self[args[0]] = {}
        elif (len(args)==3) :
            vertex = Vertex((args[0], args[1], args[2]))
            self[vertex] = {}


    def deleteVertex(self, *args):
        if (len(args)==1) :

            if self.get(args[0]) is not None :
                del self[args[0]]
            
                for v in self :
                    if self[v].get(args[0]) :  del self[v][args[0]]
            else:
                raise KeyError("Vertex is not in the graph.")
        elif (len(args)==3) :
            vertex = Vertex((args[0],args[1],args[2]))
            if self.get(vertex) is not None :
                del self[vertex]
            
                for v in self :
                    if self[v].get(vertex) :  del self[v][vertex]
            else:
                raise KeyError("Vertex is not in the graph.")
            
    def deleteVertices(self,l:list) :
            for a in l :
                 self.deleteVertex(a)

    def addEdge(self, start, dest):
        if start == dest:
            return 
        if    self.get(start) is None  or  self.get(dest) is None :
            raise ValueError("One or both vertices do not exist in the graph.")

        if self[start].get(dest)  is not None:
            return
            
        weight = round(math.sqrt((start[0] - dest[0]) ** 2 + (start[1] - dest[1]) ** 2 + (start[2] - dest[2]) ** 2), 2)
        self[start][dest]= weight
        self[dest][start]= weight


    def printNeighboors(self, v):
        if v  in self:
            output = v.__str__() +':'
            for ve in self[v]:
                output += ve.__str__() +', '
            output +='\n'
   
        else : raise ValueError("Vertix do not exist in the graph.")

    def __str__(self):
            output = "{"
            for vertex, neighbor in self.items():
                output+= str(vertex) + ': '
                output += str(neighbor)
                output +='\n'

            return output + '}\n'
    
    def getVertex(self, x, y):
        closest_ver = None
        if self.get(Vertex((x,y,0))) is not None : return Vertex((x,y,0)) 
        for vertex in self:
            if closest_ver is None:
                closest_ver = vertex
            else:
                current_distance = ((vertex[0] - x) ** 2 + (vertex[1] - y) ** 2) ** 0.5
                closest_distance = ((closest_ver[0] - x) ** 2 + (closest_ver[1] - y) ** 2) ** 0.5

                if current_distance < closest_distance:
                    closest_ver = vertex

        return closest_ver
    
    def getVerWithoutNei(self) :
        #print ([str(v) for v in self.GraphMap if len(self.GraphMap[v])==1 ])
        return [v for v in self if len(self[v])<=1 ]