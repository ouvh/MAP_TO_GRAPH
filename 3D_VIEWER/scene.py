from model import *
import shader_program
import numpy as np
import vertex_provider,pickle,Graph
import time,pickle




class Scene:
    def __init__(self, app):
        self.app = app

        # first attemp
        """self.gr = Graph.Graph()
        a = Graph.Vertex(*(6, 2, 0))
        b = Graph.Vertex(*(1, 0, 5))
        c = Graph.Vertex(* (2, 5, 10))
        self.gr.addVertex(a)
        self.gr.addVertex(b)
        self.gr.addVertex(c)

        self.gr.addEdge(a,b)
        self.gr.addEdge(b,c)
        self.gr.addEdge(c,a)

        self.objects = []

        for key in self.gr.GraphMap:
            print(1)
            self.objects.append(base_model_no_texturing(vertex_provider.get_sphere_vertex((key.m_x,key.m_y,key.m_z),1,10,10),shader_program.ShaderProgram(app.context,"default_no_texturing"),app,(1,0,0)))
            for edg in self.gr.GraphMap[key]:
                self.objects.append(base_model_no_texturing(vertex_provider.get_tunnel((key.m_x,key.m_y,key.m_z),(edg.m_destination.m_x,edg.m_destination.m_y,edg.m_destination.m_z),0.1),shader_program.ShaderProgram(app.context,"default_no_texturing"),app,(0,1,0)))
        """
        # normal behaviour
        """self.objects = []

        self.data_batch = []

        self.objects.append(base_model_no_texturing(vertex_provider.get_icosahedron(100,(0,0,0)),shader_program.ShaderProgram(app.context,"default_no_texturing"),app,(0.9,0.7,0.5)))
        
        with open("WWW.txt","rb") as file:
            WWW = pickle.load(file)

        with open("UUU.txt","rb") as file:
            UUU = pickle.load(file)
       

        
        for s in WWW:
            self.objects.append(base_model_no_texturing(np.array(s),shader_program.ShaderProgram(app.context,"default_no_texturing"),app,(1,0,0)))
        for s in UUU:
            self.objects.append(base_model_no_texturing(np.array(s),shader_program.ShaderProgram(app.context,"default_no_texturing"),app,(0,1,0)))
        
        
        """
        self.index = 1
        self.objects = []

        #new batcing algorithm 
        with open("META_3D_batches.txt","rb") as file:
            self.batches = pickle.load(file)
        

        for i in self.batches[self.index][0]:
            self.objects.append(base_model_no_texturing(np.array(i),shader_program.ShaderProgram(app.context,"default_no_texturing"),app,(0,1,0)))
        
        for i in self.batches[self.index][1]:
            self.objects.append(base_model_no_texturing(np.array(i),shader_program.ShaderProgram(app.context,"default_no_texturing"),app,(1,0,0)))
        

        for i in self.batches[self.index][2]:
            self.objects.append(base_model_no_texturing(np.array(i),shader_program.ShaderProgram(app.context,"default_no_texturing"),app,(0,1,0)))
        
        for i in self.batches[self.index][3]:
            self.objects.append(base_model_no_texturing(np.array(i),shader_program.ShaderProgram(app.context,"default_no_texturing"),app,(1,0,0)))
        


    def pass_new_batch(self):
        if self.index < len(self.batches):

            start = time.time()
            self.index += 1
            print(self.index)
            self.destroy()
            self.objects = []

            for i in self.batches[self.index][0]:
                self.objects.append(base_model_no_texturing(np.array(i),shader_program.ShaderProgram(self.app.context,"default_no_texturing"),self.app,(0,1,0)))
            
            for i in self.batches[self.index][1]:
                self.objects.append(base_model_no_texturing(np.array(i),shader_program.ShaderProgram(self.app.context,"default_no_texturing"),self.app,(1,0,0)))
            

            for i in self.batches[self.index][2]:
                self.objects.append(base_model_no_texturing(np.array(i),shader_program.ShaderProgram(self.app.context,"default_no_texturing"),self.app,(0,1,0)))
            
            for i in self.batches[self.index][3]:
                self.objects.append(base_model_no_texturing(np.array(i),shader_program.ShaderProgram(self.app.context,"default_no_texturing"),self.app,(1,0,0)))
            
            print(time.time()-start)



        
    @staticmethod
    def get_data(vertices, indices):
        data = [vertices[ind] for triangle in indices for ind in triangle]
        return np.array(data, dtype='f4')

    def get_vertex_data(self):
        vertices = [(-1, -1, 1), ( 1, -1,  1), (1,  1,  1), (-1, 1,  1),
                    (-1, 1, -1), (-1, -1, -1), (1, -1, -1), ( 1, 1, -1)]

        indices = [(0, 2, 3), (0, 1, 2),
                   (1, 7, 2), (1, 6, 7),
                   (6, 5, 4), (4, 7, 6),
                   (3, 4, 5), (3, 5, 0),
                   (3, 7, 4), (3, 2, 7),
                   (0, 6, 1), (0, 5, 6)]
        vertex_data = self.get_data(vertices, indices)

       
       

        normals = [( 0, 0, 1) * 6,
                   ( 1, 0, 0) * 6,
                   ( 0, 0,-1) * 6,
                   (-1, 0, 0) * 6,
                   ( 0, 1, 0) * 6,
                   ( 0,-1, 0) * 6,]
        normals = np.array(normals, dtype='f4').reshape(36, 3)

        vertex_data = np.hstack([normals, vertex_data])
        return vertex_data

    def add_object(self, obj):
        self.objects.append(obj)

    def render(self):
        for obj in self.objects:
            obj.render()
    
    def destroy(self):
        for obj in self.objects:
            obj.destroy()