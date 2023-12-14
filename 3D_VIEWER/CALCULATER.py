import vertex_provider
import pickle
import random

a = 1
META = {}
with open("EEEE.txt","rb") as file:
    graph = pickle.load(file)

o = 0
SPHERESSS = []
EDGESSSS = []

for i in graph:
    #SPHERESSS.append(vertex_provider.get_sphere_vertex((i[0]/a,0,i[1]/a),0.5,5,5))
    SPHERESSS.append(vertex_provider.get_icosahedron(0.5,(i[0]/a,0,i[1]/a)))
    o += 1
    for j in graph[i]:
        if META.get((i,j)) or META.get((j,i)):
            pass
        else:
            META[(i,j)] = 1
            EDGESSSS.append(vertex_provider.get_tunnel((i[0]/a,0,i[1]/a),(j[0]/a,0,j[1]/a),0.1))

WWW = []
UUU = []

for i in range(0,len(SPHERESSS)//1000):
    WWW.append(SPHERESSS[i:1000*(i+1)])


for i in range(0,len(EDGESSSS)//1000):
    UUU.append(EDGESSSS[i:1000*(i+1)])


with open("WWW.txt","wb") as file:
    pickle.dump(WWW,file)

with open("UUU.txt","wb") as file:
    pickle.dump(UUU,file)

print("done")