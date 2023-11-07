import random
import pygame
import math
from PIL import Image
import numpy
pygame.init()
font = pygame.font.SysFont('arial', 25)
font_menu = pygame.font.SysFont('arial', 50)
font_Gameover = pygame.font.SysFont('arial', 90)
nom_carte = "bg.png"
nom_carte_final_boss = "bg_final_boss.png"
nom_carte_menu = "menu.png"
carte = Image.open(nom_carte).convert('RGB')
##################   Partie fonction
def border_organiser(new,old):
    inf = 0
    sup = 0
    p = []
    for i in range(len(old)):
        if not old[i] in new:
            inf = i
            break
    for i in range(inf,len(old)):
        if old[i] in new:
            sup = i
            break
    
    for i in range(sup,len(old)):
        if old[i] in new:
            p.append(old[i])
    for i in range(inf):
        if old[i] in new:
            p.append(old[i])
    return p



################################### classe des objets
class game():
    def __init__(self):
        self.height = 720
        self.width = 1080
        self.bg = pygame.image.load(nom_carte)
        self.bg_final_boss = pygame.image.load(nom_carte_final_boss)
        self.bg_menu = pygame.image.load(nom_carte_menu)
        self.display = None
        self.running = True

    def run(self):
        self.display = pygame.display.set_mode((1080, 720))
    def stop(self):
        self.running = False
    def quit(self):
        pygame.quit()
    def get_events(self):
        return pygame.event.get()
    def update_display(self):
        pygame.display.flip()
    def get_pressed_keys(self):
        return pygame.key.get_pressed()

class player():
    def __init__(self):
        self.bullet = []
        self.max_enemy = 1
        self.max_bullet = 0
        self.heart_color = "crimson"
        self.heart = 3
        self.alive = True
        self.wallet = 6
        self.x = 81
        self.y = 54
        self.x_speed = 8
        self.y_speed = 8
        self.radius = 10
        self.color = "blue"
        self.score = 1000
        self.food_range = 10
        self.enemy_range = 10
    def move_right(self):
        self.x+= self.x_speed
    def move_left(self):
        self.x-= self.x_speed
    def move_up(self):
        self.y-= self.y_speed
    def move_down(self):
        self.y+= self.y_speed
    def check(self,x0,y0):
        if ((self.x-x0)**2+(self.y-y0)**2)**0.5 <= self.enemy_range:
            self.heart -= 1
            if self.heart <= 0:
                self.alive = False
            else:
                self.teleport_home()
                
    def check_piece(self,xx,yy):
        if ((self.x-xx)**2+(self.y-yy)**2)**0.5 <=self.food_range:
            self.score += 1
            return True
        else:
            return False
    def teleport_home(self):
        self.x = 81
        self.y = 54


class enemy():
    def __init__(self,game_height,game_width):
        self.health = 100
        self.rad = 100
        self.attack_counter = 0
        self.color = "red"
        self.bullet = []
        self.initial = list(filter(lambda r: carte.getpixel(r)==(0,0,0) and carte.getpixel((r[0]+10,r[1]))==(0,0,0)and carte.getpixel((r[0],r[1]+10))==(0,0,0) and carte.getpixel((r[0]-10,r[1]))==(0,0,0)and carte.getpixel((r[0],r[1]-10))==(0,0,0),[(random.randint(0,game_width-10),random.randint(0,game_height-10)) for _ in range(50)]))[0]
        self.x0 = self.initial[0]
        self.y0 = self.initial[1]
        self.ene_speed = 5
        self.l_x = [10,99]
        self.l_y = [10,99]
        self.block_x = [50,20]
        self.block_y = [50,20]
        self.radius = 20
        self.number = 20
        self.after = 0
        self.rr = 10
        self.risk = False
        self.len_risk = 0
        self.counter = 0
        self.comeback = True
    def check(self,x,y):
        if ((self.x0-x)**2+(self.y0-y)**2)**0.5 <= self.rr:
            return True
    
            
      
    def Move(self,x,y):
        L = [(self.x0+self.radius*math.cos(((2*math.pi)/self.number)*i),self.y0 - self.radius*math.sin(((2*math.pi)/self.number)*i))   for i in range(self.number)]
        L0 = [(carte.getpixel((e[0], e[1])),e[0],e[1])   for e in L]
        L_filtered = list(filter(lambda x: x[0] == (0,0,0),L0))
        L00 = [  (((x-e[1])**2 + (y-e[2])**2)**0.5,e[1],e[2])   for e in L_filtered]
        if self.risk:
            mi = border_organiser(L_filtered,L0)[0]
        else:
            mi = sorted(L00,key=lambda e: e[0])[0]
        nor = ((mi[1]-self.x0)**2 + (mi[2]-self.y0)**2)**0.5
        vector = ((mi[1] - self.x0)*(1/nor),(mi[2] - self.y0)*(1/nor))
        self.x0 += vector[0] * self.ene_speed
        self.y0 += vector[1] *  self.ene_speed
        self.l_x.append(self.x0)
        self.l_y.append(self.y0)
        self.block_x.append(vector[0])
        self.block_y.append(vector[1])
        if len(self.l_x) > 10:
            self.l_x.pop(0)
        if len(self.l_y) > 10:
            self.l_y.pop(0)
        if len(self.block_x) > 3:
            self.block_x.pop(0)
        if len(self.block_y) > 3:
            self.block_y.pop(0)
        self.counter +=1
        if (numpy.std(self.l_y)**2 + numpy.std(self.l_x)**2 )**0.5 < 1.5 * self.ene_speed + 0.1 :
            self.risk = True
            self.comeback = False
            self.len_risk = len(L_filtered)
            self.l_x = [10,99]
            self.l_y = [10,99]
            self.counter = 0
        else:
            if (numpy.std(self.block_x)**2 + numpy.std(self.block_y)**2 )**0.5 > 0.1 and self.counter > 3:
                self.comeback = True
        if self.comeback:
            self.after += 1
        if self.after > 3:
            self.risk = False
            self.comeback = False
            self.after = 0
    def evacuate(self):
        for i in range(40):
            self.bullet.append(bullet(self.x0+50*math.cos(((2*math.pi)/40)*i),self.y0 - 50*math.sin(((2*math.pi)/40)*i),self.x0+100*math.cos(((2*math.pi)/40)*i),self.y0 - 100*math.sin(((2*math.pi)/40)*i),Game.height,Game.width))  
    def shoot(self,x,y):
        self.bullet.append(bullet(self.x0,self.y0,x,y,Game.height,Game.width))

    def sniper(self,x,y):
        a = bullet(self.x0,self.y0,x,y,Game.height,Game.width)
        a.speed = 20
        self.bullet.append(a)
    def attack(self,x,y):
        choi = random.choice([self.shoot,self.sniper,self.evacuate])
        if choi != self.evacuate: 
            choi(x,y)
        else:
            choi()
        
        



    

class piece():
    def __init__(self,height,width):
        self.color = "yellow"
        self.radius = 5
        self.game_height = height
        self.game_width = width
        self.position = list(filter(lambda r: carte.getpixel(r)==(0,0,0) and carte.getpixel((r[0]+10,r[1]))==(0,0,0)and carte.getpixel((r[0],r[1]+10))==(0,0,0) and carte.getpixel((r[0]-10,r[1]))==(0,0,0)and carte.getpixel((r[0],r[1]-10))==(0,0,0),[(random.randint(0,self.game_width-10),random.randint(0,self.game_height-10)) for _ in range(50)]))[0]
class projectile():
    def __init__(self,height,width):
        self.x = random.randint(10,width)
        self.y = 0
        self.color = "aqua"
        self.x_speed = random.randint(0,10)
        self.y_speed = random.randint(0,10)
    def out_of_range(self,height,width):
        return  self.x >=width or self.y >= height or self.x <=0 
    def move(self):
        self.x += self.x_speed
        self.y += self.y_speed
        
class bullet():
    def __init__(self,xpl,ypl,target_x,target_y,height,width):
        self.x = xpl
        self.y = ypl
        self.count = 0
        self.speed = 15
        self.friction = 0.01
        self.vector_nor = ((target_x-self.x)**2+(target_y-self.y)**2)**0.5
        self.vector = [(target_x-self.x)/self.vector_nor,(target_y-self.y)/self.vector_nor]
    def out_of_range(self,height,width):
        return  self.x >=width or self.y >= height or self.x <=0 or self.y <=0
    def move(self):
        self.vector[1] += self.friction 
        self.x += self.speed * self.vector[0] 
        self.y += self.speed * self.vector[1] 



###### mainloop
cursor = pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR )
Game = game()
Player = player()
Enemy_list = []
piece_list = []
proj_list = []
Game.run()
pygame.mouse.set_cursor(cursor)


    

      
   #"winter"
   ##"Summer"
   #"shoot_Game"
   #" forget everything and run"


def winter():
    pygame.time.delay(23)
    Game.display.blit(Game.bg, (0, 0))
    pygame.draw.circle(Game.display, Player.color, (Player.x,Player.y),Player.radius)
    
    for ene in Enemy_list: 
        pygame.draw.circle(Game.display, ene.color, (ene.x0,ene.y0),Player.radius)
    for food in piece_list:
        pygame.draw.circle(Game.display, food.color, food.position,food.radius)
    for n_heart in range(Player.heart):
        pygame.draw.circle(Game.display, Player.heart_color, (Game.width//2 -250 + 40*n_heart,25),15)
    for proj in proj_list:
        pygame.draw.circle(Game.display, proj.color, (proj.x,proj.y),10)

        
        
    text = font.render("Score: " + str(Player.score), True, "black")
    textt = font.render("Winter", True, "black")
    Game.display.blit(textt, [Game.width//2 + 70, 10])
    Game.display.blit(text, [Game.width//2 - 50, 10])
    Game.update_display()

    
    key = Game.get_pressed_keys()
    if key[pygame.K_d]:
        Player.move_right()
    if key[pygame.K_a]:
        Player.move_left()
    if key[pygame.K_w]:
        Player.move_up()
    if key[pygame.K_s]:
        Player.move_down()
    
    
        
    for ene in Enemy_list: 
        Player.check(ene.x0,ene.y0)
        ene.Move(Player.x,Player.y)
    for proj in proj_list:
        Player.check(proj.x,proj.y)
        proj.move()
    for proj in proj_list:
        if proj.out_of_range(Game.height,Game.width):
            proj_list.remove(proj)

    if 0<= Player.score and 30>= Player.score:
        for ene in Enemy_list:
            ene.ene_speed = 2
        Player.max_enemy = 1
    elif 31<= Player.score and 40>= Player.score:
        for ene in Enemy_list:
            ene.ene_speed = 3
        Player.max_enemy = 1
    elif 41<= Player.score and 80>= Player.score:
        for ene in Enemy_list:
            ene.ene_speed = 4
        Player.max_enemy = 2
    elif 81<= Player.score and 200>= Player.score:
        for ene in Enemy_list:
            ene.ene_speed = 5
        Player.max_enemy = 2
    elif 300<= Player.score:
        for ene in Enemy_list:
            ene.ene_speed = 5
        Player.max_enemy = 5
        

    for food in piece_list:
        if Player.check_piece(food.position[0],food.position[1]):
            piece_list.remove(food)

    
    if len(piece_list)< Player.wallet:
        piece_list.append(piece(Game.height,Game.width))

    if len(Enemy_list)< Player.max_enemy:
        Enemy_list.append(enemy(Game.height,Game.width))
        
    if len(proj_list)< 5:
        proj_list.append(projectile(Game.height,Game.width))

    if carte.getpixel((Player.x, Player.y)) == (255, 255, 255):
        Player.heart -= 1
        Player.teleport_home()
        Enemy_list.clear()
    if Player.heart <=0:
        Player.alive = False


    for event in Game.get_events():
        if event.type == pygame.QUIT:
            Player.alive = False
            mainnn = False
            Game.quit()
            quit()
    

def normale():
    pygame.time.delay(23)
    Game.display.blit(Game.bg, (0, 0))
    pygame.draw.circle(Game.display, Player.color, (Player.x,Player.y),Player.radius)
    
    for ene in Enemy_list: 
        pygame.draw.circle(Game.display, ene.color, (ene.x0,ene.y0),Player.radius)
    for food in piece_list:
        pygame.draw.circle(Game.display, food.color, food.position,food.radius)
    for n_heart in range(Player.heart):
        pygame.draw.circle(Game.display, Player.heart_color, (Game.width//2 -250 + 40*n_heart,25),15)

        
    text = font.render("Score: " + str(Player.score), True, "black")
    textt = font.render("yawm sa3id", True, "black")
    Game.display.blit(textt, [Game.width//2 + 70, 10])
    Game.display.blit(text, [Game.width//2 - 50, 10])
    Game.update_display()

    
    key = Game.get_pressed_keys()
    if key[pygame.K_d]:
        Player.move_right()
    if key[pygame.K_a]:
        Player.move_left()
    if key[pygame.K_w]:
        Player.move_up()
    if key[pygame.K_s]:
        Player.move_down()
    
    
        
    for ene in Enemy_list: 
        Player.check(ene.x0,ene.y0)
        ene.Move(Player.x,Player.y)

    if 0<= Player.score and 30>= Player.score:
        for ene in Enemy_list:
            ene.ene_speed = 2
        Player.max_enemy = 1
    elif 31<= Player.score and 40>= Player.score:
        for ene in Enemy_list:
            ene.ene_speed = 3
        Player.max_enemy = 1
    elif 41<= Player.score and 80>= Player.score:
        for ene in Enemy_list:
            ene.ene_speed = 4
        Player.max_enemy = 2
    elif 81<= Player.score and 200>= Player.score:
        for ene in Enemy_list:
            ene.ene_speed = 5
        Player.max_enemy = 2
    elif 300<= Player.score:
        for ene in Enemy_list:
            ene.ene_speed = 5
        Player.max_enemy = 5
        

    for food in piece_list:
        if Player.check_piece(food.position[0],food.position[1]):
            piece_list.remove(food)

    
    if len(piece_list)< Player.wallet:
        piece_list.append(piece(Game.height,Game.width))

    if len(Enemy_list)< Player.max_enemy:
        Enemy_list.append(enemy(Game.height,Game.width))

    if carte.getpixel((Player.x, Player.y)) == (255, 255, 255):
        pygame.time.delay(1000)
        Player.heart -= 1
        Player.teleport_home()
        Enemy_list.clear()
    if Player.heart <=0:
        Player.alive = False


    for event in Game.get_events():
        if event.type == pygame.QUIT:
            Player.alive = False
            mainnn = False
            Game.quit()
            quit()



def shooter():
    pygame.time.delay(23)
    Game.display.blit(Game.bg, (0, 0))
    pygame.draw.circle(Game.display, Player.color, (Player.x,Player.y),Player.radius)

    for n_heart in range(Player.heart):
        pygame.draw.circle(Game.display, Player.heart_color, (Game.width//2 -250 + 40*n_heart,25),15)
    for bull in Player.bullet:
        pygame.draw.circle(Game.display, "orange", (bull.x,bull.y),10)
    for ene in Enemy_list: 
        pygame.draw.circle(Game.display, ene.color, (ene.x0,ene.y0),Player.radius)

        
        
    text = font.render("Score: " + str(Player.score), True, "black")
    textt = font.render("motli9", True, "black")
    Game.display.blit(textt, [Game.width//2 + 70, 10])
    Game.display.blit(text, [Game.width//2 - 50, 10])
    Game.update_display()

    
    
    
        
    for bull in Player.bullet[:]: 
        for ene in Enemy_list[:]:
            if ene.check(bull.x,bull.y):
                Enemy_list.remove(ene)
                Player.bullet.remove(bull)
                Player.score += 10
                break
    
    for bull in Player.bullet[:]:
        if bull.out_of_range(Game.height,Game.width):
            Player.bullet.remove(bull)
        else:
            bull.move()
            

    if len(Enemy_list)< 15:
        Enemy_list.append(enemy(Game.height,Game.width))
        

    for food in piece_list[:]:
        if Player.check_piece(food.position[0],food.position[1]):
            piece_list.remove(food)

    
    if len(piece_list)< Player.wallet:
        piece_list.append(piece(Game.height,Game.width))

        
    

    if carte.getpixel((Player.x, Player.y)) == (255, 255, 255):
        Player.heart -= 1
        Player.teleport_home()
        Enemy_list.clear()
    if Player.heart <=0:
        Player.alive = False


    for event in Game.get_events():
        if event.type == pygame.QUIT:
            Player.alive = False
            Game.quit()
            quit()
            
        if event.type == pygame.MOUSEBUTTONDOWN:
            if len(Player.bullet) < 5:
                    p = pygame.mouse.get_pos()
                    Player.bullet.append(bullet(Player.x,Player.y,p[0],p[1],Game.height,Game.width))

                



def final_boss():
    pygame.time.delay(23)
    Game.display.blit(Game.bg_final_boss, (0, 0))
    pygame.draw.circle(Game.display, Player.color, (Player.x,Player.y),Player.radius)

    for food in piece_list:
        pygame.draw.circle(Game.display, food.color, food.position,food.radius)
        
    for ene in Enemy_list: 
        pygame.draw.circle(Game.display, ene.color, (ene.x0,ene.y0),ene.rad)
        
    for n_heart in range(Player.heart):
        pygame.draw.circle(Game.display, Player.heart_color, (Game.width//2 -250 + 40*n_heart,30),15)

    for i in range(100):
        pygame.draw.circle(Game.display, "grey", (Game.width//2 -250 + 5*i,700),15)

    for i in range(Enemy_list[0].health):
        pygame.draw.circle(Game.display, "red", (Game.width//2 -250 + 5*i,700),15)

        
    for bull in Player.bullet:
        pygame.draw.circle(Game.display, "orange", (bull.x,bull.y),10)

    for ene in Enemy_list:
        for bull in ene.bullet:
            pygame.draw.circle(Game.display, "red", (bull.x,bull.y),10)

        
        
    text = font.render("Score: " + str(Player.score), True, "black")
    textt = font.render("Final Fight", True, "black")
    texttt = font.render("bullet left:" + str(Player.max_bullet), True, "black")
    Game.display.blit(texttt, [Game.width//2 + 200, 20])
    Game.display.blit(textt, [Game.width//2 + 70, 20])
    Game.display.blit(text, [Game.width//2 - 50, 20])
    Game.update_display()


    key = Game.get_pressed_keys()
    if key[pygame.K_d]:
        Player.move_right()
    if key[pygame.K_a]:
        Player.move_left()
    if key[pygame.K_w]:
        Player.move_up()
    if key[pygame.K_s]:
        Player.move_down()
    
    

    for ene in Enemy_list:
        Player.enemy_range = 100
        Player.check(ene.x0,ene.y0)
        Player.enemy_range = 10
        ene.Move(Player.x,Player.y)
    
    for ene in Enemy_list:
        ene.attack_counter += 1
        if ene.attack_counter > 50:
            ene.attack(Player.x,Player.y)
            ene.attack_counter = 0
     
    for bull in Player.bullet[:]:
        if bull.count > 10:      
            Player.check(bull.x,bull.y)
        for ene in Enemy_list[:]:
            if ene.check(bull.x,bull.y):
                ene.health -= 2
                Player.bullet.remove(bull)
                break
    
    for bull in Player.bullet[:]:
        if bull.out_of_range(Game.height,Game.width):
            Player.bullet.remove(bull)
        else:
            bull.move()
            bull.count += 1

            
    for ene in Enemy_list:
        for bull in ene.bullet[:]:
            Player.check(bull.x,bull.y)
            if bull.out_of_range(Game.height,Game.width):
                ene.bullet.remove(bull)
            else:
                bull.move()
                bull.count += 1
    
        

    for food in piece_list[:]:
        if Player.check_piece(food.position[0],food.position[1]):
            Player.max_bullet += 1
            piece_list.remove(food)

           
    if len(piece_list)< Player.wallet:
        e = piece(Game.height,Game.width)
        e.color = "brown"
        piece_list.append(e)
    

    if carte.getpixel((Player.x, Player.y)) == (255, 255, 255):
        Player.heart -= 1
        Player.teleport_home()
        
    if Player.heart <=0:
        Player.alive = False


    for event in Game.get_events():
        if event.type == pygame.QUIT:
            Player.alive = False
            Game.quit()
            quit()
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if Player.max_bullet > 0 :
                    p = pygame.mouse.get_pos()
                    Player.bullet.append(bullet(Player.x,Player.y,p[0],p[1],Game.height,Game.width))
                    Player.max_bullet -= 1
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if Player.max_bullet > 0 :
                    p = pygame.mouse.get_pos()
                    Player.bullet.append(bullet(Player.x,Player.y,p[0],p[1],Game.height,Game.width))
                    Player.max_bullet -= 1



















def Gameover_screen():
    gameover = True
    s = pygame.Surface((1080,720))
    s.set_alpha(130)
    s.fill("grey")
    Game.display.blit(s, (0,0))
    pygame.draw.rect(Game.display,"cyan",(540-115,50+360-(70+10),230,70))
    pygame.draw.rect(Game.display,"cyan",(540-115,50+360+(10),230,70))
            
    text_replay = font_menu.render("Replay", True, "black")
    text_menu = font_menu.render("Menu", True, "black")
    text_gameover = font_Gameover.render("Game Over" ,True ,"black")
    Game.display.blit(text_replay, [540-60, 50+360-70-10])
    Game.display.blit(text_menu, [540-50, 50+360+10])
    Game.display.blit(text_gameover,[350,170])     
    pygame.display.flip()
    while gameover:
        for event in Game.get_events():
            if event.type == pygame.QUIT:
                Game.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                p = pygame.mouse.get_pos()
                if  425 < p[0] < 655  and  280+50 < p[1] < 350+50:
                    Player.alive = True
                    Player.teleport_home()
                    Player.heart = 3
                    Player.score = 0
                    carte = Image.open(nom_carte).convert('RGB')
                    Mainloop()
                elif 425 < p[0] < 655 and 370+50 < p[1] < 440+50:
                    gameover = False
                    
        
    
    
        














def Mainloop():
    Enemy_list.clear()
    Player.bullet.clear()
    piece_list.clear()
    Gamemode = [winter,normale,shooter]
    counter = 0
    current = shooter
    while Player.alive:
        counter += 1
        current()
        if counter > 300:
            if current == shooter:
                Player.bullet.clear()
                Enemy_list.clear()
            elif current== winter:
                proj_list.clear()
                Enemy_list.clear()
            
            current = random.choice(Gamemode)
            counter = 0
    Gameover_screen()
    
def boss_fight():  
    Enemy_list.clear()
    Player.bullet.clear()
    piece_list.clear()
    boss = enemy(Game.height,Game.width)
    boss.radius = 50
    boss.rr = 100
    boss.ene_speed = 0.5
    Enemy_list.append(boss)
    while boss.health >0 and Player.alive:
        final_boss()
        if not Player.alive:
            print("next time")
        elif boss.health <= 0:
            print("Well Played")


            
def menu():
    pygame.time.delay(23)
    Game.display.fill("grey")
    #Game.display.blit(Game.bg_menu, (0, 0))
    pygame.draw.rect(Game.display,"cyan",(540-115,360-(70+10),230,70))
    pygame.draw.rect(Game.display,"cyan",(540-115,360+(10),230,70))
 
    text_start = font_menu.render("Play", True, "black")
    text_quit = font_menu.render("Quit", True, "black")
    Game.display.blit(text_start, [540-40, 360-70-10])
    Game.display.blit(text_quit, [540-40, 360+10])
    
    pygame.display.flip()



    
    




#Mainloop()

while True:
    menu()



    for event in Game.get_events():
        if event.type == pygame.QUIT:
            Game.quit()
            quit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            p = pygame.mouse.get_pos()
            if  425 < p[0] < 655  and  280 < p[1] < 350:
                Player.alive = True
                Player.teleport_home()
                Player.heart = 3
                Player.score = 0
                carte = Image.open(nom_carte).convert('RGB')
                Mainloop()
            elif 425 < p[0] < 655 and 370 < p[1] < 440:
                Game.quit()
                quit()
            elif 425 < p[0] < 655 and 0 < p[1] < 20:
                Player.alive = True
                Player.teleport_home()
                Player.heart = 3
                carte = Image.open(nom_carte_final_boss).convert('RGB')
                boss_fight()
                
                

    
Game.quit()





    

    
    



    
