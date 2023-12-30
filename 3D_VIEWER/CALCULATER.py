import vertex_provider
import pickle
import random


DIVISION = 5000
a = 1
META = {}
with open("EEEE.txt","rb") as file:
    graph = pickle.load(file)

print(len(graph))
o = 0
SPHERESSS = []
EDGESSSS = []

for i in graph:
    #SPHERESSS.append(vertex_provider.get_sphere_vertex((i[0]/a,0,i[1]/a),0.5,5,5))
    SPHERESSS.append(vertex_provider.get_icosahedron(0.5,(i[0]/a,i[2]/a,i[1]/a)))
    o += 1
    for j in graph[i]:
        if META.get((i,j)) or META.get((j,i)):
            pass
        else:
            META[(i,j)] = 1
            EDGESSSS.append(vertex_provider.get_tunnel((i[0]/a,i[2]/a,i[1]/a),(j[0]/a,j[2]/a,j[1]/a),0.1))

WWW = []
UUU = []



for i in range(0,len(SPHERESSS)//DIVISION):
    WWW.append(SPHERESSS[i:DIVISION*(i+1)])


for i in range(0,len(EDGESSSS)//DIVISION):
    UUU.append(EDGESSSS[i:DIVISION*(i+1)])


with open("WWW.txt","wb") as file:
    pickle.dump(WWW,file)

with open("UUU.txt","wb") as file:
    pickle.dump(UUU,file)


print("done")