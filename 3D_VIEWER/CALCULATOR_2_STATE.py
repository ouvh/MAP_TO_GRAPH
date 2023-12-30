import vertex_provider
import pickle
import random
from numba import jit


DIVISION = 5000
MEta_data_spheres = {}
MEta_data_edges = {}

a = 1/100
META = {}
with open("EEEE.txt","rb") as file:
    graph = pickle.load(file)

with open("states.txt","rb") as file:
    states = pickle.load(file)

print(len(states),'len of asefe')


def coordinate_calculation():
    for i in graph:
        MEta_data_spheres[i] = vertex_provider.get_icosahedron(50,(i[0]/a,i[2]/a,i[1]/a))

        for j in graph[i]:
            """if META.get((i,j)) or META.get((j,i)):
                pass
            else:
                META[(i,j)] = 1"""
            MEta_data_edges[(i,j)] = vertex_provider.get_tunnel((i[0]/a,i[2]/a,i[1]/a),(j[0]/a,j[2]/a,j[1]/a),0.5)
    


        
        
def calculate_a_state(state):
    local_meta = {}



    SPHERESSS_DISCOVERED = []
    SPHERESSS_NOT_DISCOVERED = []
    EDGESSSS_DISCOVERED = []
    EDGESSSS_NOT_DISCOVERED = []

    for i in graph:
        if state.get(i):
            SPHERESSS_DISCOVERED.append(MEta_data_spheres[i])
        else:
            SPHERESSS_NOT_DISCOVERED.append(MEta_data_spheres[i])


        for j in graph[i]:
            if local_meta.get((i,j)) or local_meta.get((j,i)):
                pass
            else:
                local_meta[(i,j)] = 1
                if state.get(j):
                    EDGESSSS_DISCOVERED.append(MEta_data_edges[(i,j)])
                    """
                    if MEta_data_edges.get((i,j)):
                        EDGESSSS_DISCOVERED.append(MEta_data_edges[(i,j)])
                    else:
                        EDGESSSS_DISCOVERED.append(MEta_data_edges[(j,i)])"""
                    

                else:
                    EDGESSSS_NOT_DISCOVERED.append(MEta_data_edges[(i,j)])
                    """
                    if MEta_data_edges.get((i,j)):
                        EDGESSSS_DISCOVERED.append(MEta_data_edges[(i,j)])
                    else:
                        EDGESSSS_DISCOVERED.append(MEta_data_edges[(j,i)])
                    """



    undiscovered_shere = []
    discovered_sphere = []

    discovered_edges = []
    undiscovered_edges = []





    if len(SPHERESSS_DISCOVERED) < DIVISION:
        discovered_sphere.append(SPHERESSS_DISCOVERED[:])
    else:
        for i in range(0,len(SPHERESSS_DISCOVERED)//DIVISION):
            discovered_sphere.append(SPHERESSS_DISCOVERED[i:DIVISION*(i+1)])

    

##########################################
            

    if len(SPHERESSS_NOT_DISCOVERED) < DIVISION:
        undiscovered_shere.append(SPHERESSS_NOT_DISCOVERED[:])
    else:
        for i in range(0,len(SPHERESSS_NOT_DISCOVERED)//DIVISION):
            undiscovered_shere.append(SPHERESSS_NOT_DISCOVERED[i:DIVISION*(i+1)])




##########################################
            

    if len(EDGESSSS_DISCOVERED) < DIVISION:
        discovered_edges.append(EDGESSSS_DISCOVERED[:])
    else:
        for i in range(0,len(EDGESSSS_DISCOVERED)//DIVISION):
            discovered_edges.append(EDGESSSS_DISCOVERED[i:DIVISION*(i+1)])



##########################################
            




    if len(EDGESSSS_NOT_DISCOVERED) < DIVISION:
        undiscovered_edges.append(EDGESSSS_NOT_DISCOVERED[:])
    else:
        for i in range(0,len(EDGESSSS_NOT_DISCOVERED)//DIVISION):
            undiscovered_edges.append(EDGESSSS_NOT_DISCOVERED[i:DIVISION*(i+1)])





    return [discovered_sphere,undiscovered_shere,discovered_edges,undiscovered_edges]

META_3D_batches = []

coordinate_calculation()

for i in states:
    META_3D_batches.append(calculate_a_state(i))



with open("META_3D_batches.txt","wb") as file:
    pickle.dump(META_3D_batches,file)

print("done")

