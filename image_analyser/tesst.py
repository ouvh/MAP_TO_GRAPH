import cv2,pygame
from PIL import Image,ImageDraw
dd = "map.png"
mage = Image.open(dd)

image = cv2.imread(dd, cv2.IMREAD_GRAYSCALE)

# Apply Canny edge detection
edges = cv2.Canny(image, 0, 90)




display = pygame.display.set_mode(mage.size,pygame.RESIZABLE)
imagg = pygame.image.load(dd)





run = True

display.fill('white')
for l in range(len(edges)):
    for i in range(len(edges[l])):  
        pygame.draw.circle(display,(255-edges[l][i],255-edges[l][i],255-edges[l][i]),(i,l),1)
pygame.display.flip()


while run:
    pygame.time.delay(166)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            print(pygame.mouse.get_pos())
