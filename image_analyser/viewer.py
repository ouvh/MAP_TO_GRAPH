import pygame
import pickle
from PIL import Image


image = Image.open("map.png").convert("RGB")
current = 0
with open("points.txt","rb") as file:
            DDD = pickle.load(file)

class DrawObject:
    def __init__(self) -> None:
        self.L = []
        self.main = 0
        self.main_color = "red"
        self.L_color = "green"

    def pass_complexe(self,K):
        self.L = list(map(lambda x:(x.real,x.imag) if x != None else None,K))
        

def lauch_window():
    global current

    run = True
    display = pygame.display.set_mode(image.size)
    imagg = pygame.image.load("map.png")



    while run:
        pygame.time.delay(166)
        display.blit(imagg,(0,0))
        
       


        for i in DDD[current][1]:
            if i != None:
                pygame.draw.circle(display,"green",i,2)
        
        for i in DDD[current][0]:
             pygame.draw.circle(display,"red",i,2)
        

        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                print(pygame.mouse.get_pos())
                if current != len(DDD):
                    current += 1

lauch_window()
