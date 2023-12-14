import cv2
import numpy as np

def edge_and_contour_detection(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

    # Apply Canny edge detection
    edges = cv2.Canny(blurred_image, threshold1=30, threshold2=100)

    # Find contours
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the contours on a copy of the original image
    contour_image = image.copy()
    cv2.drawContours(contour_image, contours, -1, (0, 255, 0), 1)

    # Display the original image, edges, and contours
    cv2.imshow('Original Image', image)
    cv2.imshow('Edges', edges)
    cv2.imshow('Contours', contour_image)

    # Wait for a key press and then close the windows
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Test the function with an example image
edge_and_contour_detection('map2.png')

from Graph  import Graph,Vertex
import cv2
import numpy as np 
import time
import pygame
from math import cos,sin,pi,sqrt
import numpy as np
from PIL import Image,ImageDraw 


image = cv2.imread("map2.png")

# Convert the image to grayscale
gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# Apply Gaussian blur to reduce noise
blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)

# Apply Canny edge detection
edges = cv2.Canny(blurred_image, threshold1=30, threshold2=100)

# Find contours
contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)



road_coordinates = []
step = 3          
for contour in contours:
    print(contour)
    for i in range(0,len(contour),step) :
        road_coordinates.append(tuple(contour[i][0]))


# Create a graph
road_graph = Graph()

# Add road nodes


for coord in road_coordinates:
    road_graph.addVertex(coord[0],coord[1],0)
   

print(len(road_coordinates))
# Connect road nodes to form edges

count = 2
for i in range(len(road_coordinates)):

    for j in range(len(road_coordinates)):

        if i==j : 
            continue


        if sqrt((road_coordinates[i][0] - road_coordinates[j][0]) ** 2 + (road_coordinates[i][1] - road_coordinates[j][1]) ** 2 ) < 10:

        
            v1 = Vertex(road_coordinates[i][0],road_coordinates[i][1],0)
            v2 = Vertex(road_coordinates[j][0],road_coordinates[j][1],0)
            road_graph.addEdge(v1, v2)

           
    

print(count)


run = True
image = Image.open("map2.png").convert("RGB")

display = pygame.display.set_mode(image.size)
imagg = pygame.image.load("map2.png")




while run:
    pygame.time.delay(166)
    display.blit(imagg,(0,0))
   

    for vertex in road_graph.GraphMap:
       pygame.draw.circle(display,"red",(vertex.m_x,vertex.m_y),2)
       
       for edge in road_graph.GraphMap[vertex]:
           pygame.draw.line(display,"green",(vertex.m_x,vertex.m_y),(edge.m_destination.m_x,edge.m_destination.m_y))
           





    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
       
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
   
