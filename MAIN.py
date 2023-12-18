import numpy as np
from PIL import Image
from Graph import Vertex, Graph
import pygame
from shortest_path import Dijkstra
from Image_to_Graph import Build_Graph

import pickle

image_link = "map.png"
image = Image.open(image_link)

run = True

"""
roads_graph = Build_Graph(image_link)
"""
with open("EEEE.txt","rb") as file:
    roads_graph = pickle.load(file)



display = pygame.display.set_mode(image.size)
imagg = pygame.image.load(image_link)
display.blit(imagg,(0,0))
pygame.display.flip()


# Initialize source and target vertices
source_vertex = None
target_vertex = None
vertex_selection_mode = "source"


while run:
    display.blit(imagg, (0, 0))



    if vertex_selection_mode == "source":
        pygame.display.set_caption("Select Source Vertex")
    elif vertex_selection_mode == "target":
        pygame.display.set_caption("Select Target Vertex")



    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if vertex_selection_mode == "source" and source_vertex is None:
                source_vertex = roads_graph.getVertex(*pygame.mouse.get_pos())
                vertex_selection_mode = "target"
            elif vertex_selection_mode == "target" and target_vertex is None:
                target_vertex = roads_graph.getVertex(*pygame.mouse.get_pos())
                vertex_selection_mode = "done"

    if vertex_selection_mode == "done":
        print('====', source_vertex)
        print('====', target_vertex)
        shortest_path = Dijkstra(roads_graph, source_vertex, target_vertex)
        print(shortest_path)
        vertex_selection_mode = 'did'
        pygame.draw.circle(display, (255,10,10), (source_vertex[0], source_vertex[1]), 5)
        pygame.draw.circle(display, (255,10,10), (target_vertex[0], target_vertex[1]), 5)
        pygame.display.flip()
        for i in range(len(shortest_path)-1,-1,-1):
                pygame.draw.circle(display, (40,10,255), (shortest_path[i][0], shortest_path[i][1]), 2)
                pygame.display.flip()
pygame.quit()