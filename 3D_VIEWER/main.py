import pygame as pg
import moderngl as mgl
import sys
from model import *
from camera import Camera
from light import Light
from scene import Scene
import random


class GraphicsEngine:
    def __init__(self, win_size=(720, 720)):
        pg.init()
        self.WIN_SIZE = win_size
        
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MAJOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_MINOR_VERSION, 3)
        pg.display.gl_set_attribute(pg.GL_CONTEXT_PROFILE_MASK, pg.GL_CONTEXT_PROFILE_CORE)
        # create opengl context
        pg.display.set_mode(self.WIN_SIZE,flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
        # mouse settings
        pg.event.set_grab(True)
        pg.mouse.set_visible(False)
        # detect and use existing opengl context
        self.context = mgl.create_context()
        #self.context.front_face = 'cw'
        self.context.enable(flags=mgl.DEPTH_TEST )  #| mgl.CULL_FACE
        # create an object to help track time
        self.clock = pg.time.Clock()
        self.time = 0
        self.delta_time = 0
        # light
        self.light = Light()
        # camera
        self.camera = Camera(self)
        # scene
        self.scene = Scene(self)


    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                self.scene.destroy()
                pg.quit()
                sys.exit()
            
            elif event.type == pg.VIDEORESIZE:
                pg.display.set_mode(event.size,flags=pg.OPENGL | pg.DOUBLEBUF | pg.RESIZABLE)
                self.WIN_SIZE = event.size
                self.camera.aspect_ratio = self.WIN_SIZE[0] / self.WIN_SIZE[1]
                self.camera.m_proj = self.camera.get_projection_matrix()
            
            elif event.type == pg.KEYDOWN and event.key == pg.K_p:

                pg.event.set_grab(True)
                pg.mouse.set_visible(False)
            
            elif event.type == pg.KEYDOWN and event.key == pg.K_o:

                pg.event.set_grab(False)
                pg.mouse.set_visible(True)
            


    def render(self):
        # clear framebuffer
        self.context.clear(color=(0.08, 0.16, 0.18))
        # render scene
        self.scene.render()
        # swap buffers
        pg.display.flip()

    def get_time(self):
        self.time = pg.time.get_ticks() * 0.001

    def run(self):
        while True:
            #self.scene.objects[0].model_matrix = glm.translate(glm.mat4() , (random.randint(0,2),random.randint(0,2),random.randint(0,2))) #glm.vec3([glm.radians(random.randint(0,100)),glm.radians(random.randint(0,100)),glm.radians(random.randint(0,100))])
            self.get_time()
            self.check_events()
            self.camera.update()
            self.render()
            self.delta_time = self.clock.tick(60)


if __name__ == '__main__':
    app = GraphicsEngine()
    app.run()































