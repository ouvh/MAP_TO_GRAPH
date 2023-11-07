from collections import defaultdict
from queue import PriorityQueue
from Graph import Graph,Vertex

distances = defaultdict(lambda: float('inf'))
predecessors = {}


class Couple(tuple) :
    def __lt__(self, other) -> bool:
        return self[0] < other[0] 

def Dijkstra(g,source,target) :
    distances[source] = 0
    pqueue = PriorityQueue()
    pqueue.put(Couple((0,source)))

    while not pqueue.empty() :
        current = pqueue.get()[1]

        if current ==  target : 
             break

        for ver in g[current] :

            if distances[current] + g[current][ver] < distances[ver] : 

                distances[ver] = distances[current] + g[current][ver] 
                pqueue.put(Couple((distances[ver],ver)))
                predecessors[ver] = current

    path = []
    current = target

    while current != source  :
        
        path.append(current)  
        current = predecessors[current]
    path.append(source)
    
    return path